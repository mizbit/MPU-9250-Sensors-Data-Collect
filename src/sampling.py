import csv
import datetime
import os
import sys
import time
from threading import Thread
from mpu_9250 import MPU9250

class Sampling(Thread):

    running = False
    sampling_rate = 0.1 # 100 Hz
    sleepStartSeconds = 5

    mpu = None

    folder = "../../data"
    file = None

    def __init__(self, address_ak, address_mpu_master, address_mpu_slave, bus):
        Thread.__init__(self)
        self.mpu = MPU9250(address_ak, address_mpu_master, address_mpu_slave, bus)
    
    def configure(self, gfs, afs, mfs, mode):
        self.mpu.configure(gfs, afs, mfs, mode)

    def reset(self):
        self.mpu.reset()

    def startSampling(self, timeSync):

        self.file = self.folder + "/mpu-data-set-" + str(hex(self.mpu.address_mpu_master)) + " " + datetime.datetime.fromtimestamp(timeSync).strftime('%d-%m-%Y %H-%M-%S') + ".csv"

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.timeSync = timeSync
        self.running = True
        self.start()

    def stopSampling(self):
        self.running = False
        self.join()

    def run(self):

        with open(self.file, "w+") as csvfile:
            
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            row = self.getLabels()
            spamwriter.writerow(row)

            # Faz com que as threads iniciem ao mesmo tempo
            sleepTime = self.sleepStartSeconds + (self.timeSync - int(self.timeSync))
            time.sleep(sleepTime)

            lastTime = time.time()

            while self.running:

                row = self.mpu.getAllData()
                spamwriter.writerow(row)
                sleepTime = self.sampling_rate - (time.time() - lastTime)
                
                if(sleepTime > 0):
                    time.sleep(sleepTime)

                lastTime = time.time()

    def getLabels(self):
    
        return [
            "timestamp", 
            "master_acc_x", 
            "master_acc_y", 
            "master_acc_z", 
            "master_gyro_x", 
            "master_gyro_y", 
            "master_gyro_z", 
            "slave_acc_x", 
            "slave_acc_y", 
            "slave_acc_z", 
            "slave_gyro_x", 
            "slave_gyro_y", 
            "slave_gyro_z", 
            "mag_x"
            "mag_y"
            "mag_z"
        ]