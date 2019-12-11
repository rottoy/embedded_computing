

#import FarmControl
from flask import Flask, render_template ,request, jsonify
import datetime

app = Flask(__name__)

current_th_list =[0,0] #첫번째는 현재 온도, 두번째는 현재 습도
setting_th_list =[0,0] #첫번째는 설정 온도, 두번째는 설정 습도
isTempSensorOn = False # 온도 비교를 통해 킬지 안킬지 정하는 값
isHumidSensorOn = False # 습도 비교를 통해 킬지 안킬지 정하는 값
@app.route("/")
def initialize():
    global current_th_list
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'temperature' : current_th_list[0],
        'humidity': current_th_list[1]
    }
    return render_template('main.html', **templateData)


@app.route('/post', methods=['POST'])
def post():

    global setting_th_list

    temperature = request.form['action_temp'] # main.html의 post를 통해서 사용자 온도 설정 입력값을 받아오게 됨
    humidity = request.form['action_humid'] #main.html의 post 를 통해서 사용자 습도 설정 입력값을 받아오게 됨

    #BACK (설정 온습도 와 현재 온습도 비교를 통한 결과 값 반환)
    setting_th_list[0] =int(temperature)
    setting_th_list[1] =int(humidity)
    compare(current_th_list,setting_th_list) #값 비교 함수 호출


    #FRONT (html에 결과 출력)
    str_temp = "온도 센서가 켜지지 않았습니다."
    str_humid = "습도 센서가 켜지지 않았습니다."
    if isTempSensorOn:
        str_temp ="온도 센서가 켜졌습니다!"
    if isHumidSensorOn:
        str_humid ="습도 센서가 켜졌습니다!"
    templateData = {
        'temperature' : temperature,
        'humidity': humidity,
        'str_temp' : str_temp,
        'str_humid' : str_humid
    }

    return render_template('set_status.html',**templateData)

def compare(current, settings):
    print("compare activated")
    global isTempSensorOn,isHumidSensorOn
    if current[0] > settings[0]: #현재 온도가 설정 온도보다 높으므로 키지 않는다.
        isTempSensorOn = False
    else:
        isTempSensorOn = True

    if current[1] > settings[1]: #현재 습도가 설정 습도보다 높으므로 키지 않는다.
        isHumidSensorOn = False
    else:
        isHumidSensorOn = True

        
@app.route('/thermoReport', methods=['POST'])
def report():
    global current_th_list
    global setting_th_list
    global isTempSensorOn
    global isHumidSensorOn
    temperFlag=0
    humidFlag=0
    data = request.get_json(force=True)
    print(data)
    current_th_list[0]=(int)(data["temper"])
    current_th_list[1]=(int)(data["humid"])
    if current_th_list[0]<=setting_th_list[0]:
        temperFlag=1
        isTempSensorOn=True
    else :
        temperflag=0
        isTempSensorOn=False
    if current_th_list[1]<=setting_th_list[1]:
        humidFlag=1
        isHumidSensorOn=True
    else:
        humidFlag=0
        isHumidSensorOn=False
    return jsonify(light = temperFlag, humid = humidFlag, setTemper = setting_th_list[0], setHumid= setting_th_list[1])
   


@app.route('/getTH')
def getTempHumid():
    global current_th_list
    return jsonify(temperature = current_th_list[0], humidity=current_th_list[1])

@app.route('/getStatusTH')
def getSensor():
    global isTempSensorOn
    global isHumidSensorOn
    print("server : "+str(isTempSensorOn))
    print("server : "+str(isHumidSensorOn))
    return jsonify(isTemp=isTempSensorOn, isHumid=isHumidSensorOn)

@app.route('/sendServerFromUI', methods=['GET','POST'])
def setStatus():
    #print("sadas")
    data = request.get_json(force=True)
    print(format(data))
    print(data)
    
    setting_th_list[0] = int(data["ui_temperature"])
    setting_th_list[1] = int(data["ui_humidity"])
    
    print("settings temperature changed : "+str(setting_th_list[0]))
    print("settings humidity changed : "+str(setting_th_list[1]))
    return jsonify(statusMessage="Success")
@app.route('/putBulbOff')
def setBulbOff():
    global isTempSensorOn
    isTempSensorOn=False
    return jsonify(statusMessage="Bulb Turned Off")

@app.route('/putHumidOff')
def setHumidOff():
    global isHumidSensorOn
    isHumidSensorOn=False
    return jsonify(statusMessage="Humid Turned Off")
def main():
    
    app.run(host='172.30.1.55', port=4321, debug=True)

if(__name__=="__main__"):
    main()
