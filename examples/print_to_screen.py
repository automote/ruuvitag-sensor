'''
Print sensor data to the screen. Update interval 2 sec.

Press Ctrl+C to quit.

2017-02-02 13:45:25.233400
Sensor - F4:A5:74:89:16:57
Temperature: 10
Humidity:    28
Pressure:    689
'''

import time
import os
from datetime import datetime
import requests as rq
from ruuvitag_sensor.ruuvitag import RuuviTag

# Change here your own device's mac-address
mac = 'EE:A1:C8:AF:34:5D'

print('Starting')

sensor = RuuviTag(mac)

while True:
    data = sensor.update()

    line_sen = str.format('Sensor - {0}', mac)
    line_tem = str.format('Temperature: {0} C', data['temperature'])
    line_hum = str.format('Humidity:    {0}', data['humidity'])
    line_pre = str.format('Pressure:    {0}', data['pressure'])
    line_batt = str.format('Battery:    {0}', data['battery'])
    line_acc_x = str.format('Acc X:     {0}', data['acceleration_x'])
    line_acc_y = str.format('Acc Y:    {0}', data['acceleration_y'])
    line_acc_z = str.format('Acc Z:    {0}', data['acceleration_z'])
    line_measure_seq_no = str.format('Measure Seq No:    {0}', data['measurement_sequence_number'])
    line_counter = str.format('Counter:    {0}', data['movement_counter'])
    line_tx_pwr = str.format('TX POWER:    {0}', data['tx_power'])
    
    thingSpeak_URL = "https://api.thingspeak.com/update?api_key=NA5VJLXAKT647NCC&field1="+str(data['temperature'])+"&field2="+str(data['humidity'])+\
    "&field3="+str(data['pressure'])+"&field4="+str(data['battery'])+"&field5="+str(data['acceleration_x'])+"&field6="+str(data['acceleration_y'])+\
    "&field7="+str(data['acceleration_z'])+"&field8="+str(data['measurement_sequence_number'])
    try:
    	rs = rq.get(thingSpeak_URL)
    	print("sent successfully")
    except:
    	print("sending failed to thingspeak")
    
    # Clear screen and print sensor data
    #os.system('clear')
    print('Press Ctrl+C to quit.\n\r\n\r')
    print(str(datetime.now()))
    print(line_sen)
    print(line_tem)
    print(line_hum)
    print(line_pre)
    print(line_batt)
    print(line_acc_x)
    print(line_acc_y)
    print(line_acc_z)
    print(line_measure_seq_no)
    print(line_counter)
    print(line_tx_pwr)
    print('\n\r\n\r.......')

    # Wait for 2 seconds and start over again
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        # When Ctrl+C is pressed execution of the while loop is stopped
        print('Exit')
        break
