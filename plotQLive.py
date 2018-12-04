#! /usr/bin/env python3
import os
from glob import glob
import time
import datetime
import serial
import sys
import math        #import needed modules
import pyaudio
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.dates as mdates


style.use('fivethirtyeight')
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
xs=[]
ys=[]







PyAudio = pyaudio.PyAudio

def openSerialPort(port):
    ser = serial.Serial()
    ser.baudrate = 57600
    ser.port = port
    while not ser.is_open:
        time.sleep(1)
        print("Opening serial connection to %s at %d baud"%(ser.port,ser.baudrate))
        try:
            ser.open()
        except Exception as e:
            print(e)
            continue
    print("Successfully connected to %s"%(ser.port))
    return ser




def main(port):
    ser = openSerialPort(port)
    ID1 = "Q" + os.path.split(port)[-1][-8:-4]
    print("Starting data collection...")
    ser.reset_input_buffer()
    #plt.ion()


    while True:
        try:
            packet = ser.readline().rstrip(b"\n").rstrip(b"\r")
            #Format: Sample #,Z-axis,Y-axis,X-axis,Battery,Temperature(C),EDA(uS)
            (Z, Y, X, vBat, Temp, EDA) = [float(x) for x in packet.split(b",")[1:]]
            #print("EDA = %0.3f | Accelerometer = [%0.3f,%0.3f,%0.3f] | Temperature (F) = %0.1f"%(EDA, X,Y,Z, (Temp*(9.0/5.0) + 32) ))
            #good_EDA=int(float(((0.2-EDA)*100)))
            #good_EDA=format (float(((EDA-.1)*10)+1),'.3f')
            #good_EDA=int(100(((EDA-(.1)*10)+1))
            currenteda= []
            currenteda.append(EDA)
            print (currenteda)

            def animate(i, xs, ys):
                xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
                ys.append(currenteda[0])
                xs = xs[-20:]
                ys = ys[-20:]
                ax.clear()
                ax.plot(xs, ys)
                plt.xticks(rotation=45, ha='right')
                plt.subplots_adjust(bottom=0.30)
                plt.title('TMP102 Temperature over Time')
                plt.ylabel('Temperature (deg C)')
            ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
            plt.show()


            #ax.xaxis.set_major_formatter(myFmt)
            #x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
            #print (x)
##			plt.plot(EDA, EDA)
##			plt.title(str(EDA))
##			plt.draw()
##			plt.pause(0.1)
            #plt.show(block=True)
##			y = [float(n) for n in s[0].split()]
##
##			plt.plot(y, x)
##			#plt.title(str(i))
##			plt.draw()
##			plt.pause(0.1)
##			plt.show(block=True)

        except KeyboardInterrupt:
            ser.close()
            print("Closing stream and exiting...")
            sys.exit()





if __name__ == '__main__':
    print("Welcome to Q Live!")
    print("The following Q Sensors are paired to your computer:")
    sensors = glob("/dev/tty.AffectivaQ-v2*")
    for sensor in sensors:
        print("\t[%d] %s"%(sensors.index(sensor), sensor.replace("/dev/tty.AffectivaQ-v2-","").replace("-SPP","")))
    s1 = int(input("Type the number of the sensor you want to use: " ))
    main(sensors[s1])

