from MPU.mpu9250_i2c import *
from linear_test import *
from MPU.gyro_integrate import *

def get_gyro():
    _,_,_,wx,wy,wz = mpu6050_conv() # read and convert gyro data
    return wx,wy,wz

def gyro_cal(cal_size):
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    [get_gyro() for ii in range(0,cal_size)] # clear buffer before calibration
    mpu_array = []
    gyro_offsets = [0.0,0.0,0.0]
    while True:
        try:
            wx,wy,wz = get_gyro() # get gyro vals
        except:
            continue

        mpu_array.append([wx,wy,wz])

        if np.shape(mpu_array)[0]==cal_size:
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # average
            break
    print('Gyro Calibration Complete')
    return gyro_offsets
    
def mpu6050_conv():
    # raw acceleration bits
    acc_x = read_raw_bits(ACCEL_XOUT_H)
    acc_y = read_raw_bits(ACCEL_YOUT_H)
    acc_z = read_raw_bits(ACCEL_ZOUT_H)

    # raw temp bits
##    t_val = read_raw_bits(TEMP_OUT_H) # uncomment to read temp
    
    # raw gyroscope bits
    gyro_x = read_raw_bits(GYRO_XOUT_H)
    gyro_y = read_raw_bits(GYRO_YOUT_H)
    gyro_z = read_raw_bits(GYRO_ZOUT_H)

    #convert to acceleration in g and gyro dps
    a_x = (acc_x/(2.0**15.0))*accel_sens
    a_y = (acc_y/(2.0**15.0))*accel_sens
    a_z = (acc_z/(2.0**15.0))*accel_sens

    w_x = (gyro_x/(2.0**15.0))*gyro_sens
    w_y = (gyro_y/(2.0**15.0))*gyro_sens
    w_z = (gyro_z/(2.0**15.0))*gyro_sens

##    temp = ((t_val)/333.87)+21.0 # uncomment and add below in return
    return a_x,a_y,a_z,w_x,w_y,w_z

    

def main():

    print("Initializing... ")
    
    ###################################
    # Gyroscope Offset Calculation
    ###################################
    
    gyro_labels = ['\omega_x','\omega_y','\omega_z'] # gyro labels for plots
    cal_size = 500 # points to use for calibration
    gyro_offsets = gyro_cal(cal_size) # calculate gyro offsets

    # Turning
    
    stop()
    angle = 0
    rot_axis = 2 # axis being rotated (2 = z-axis)
    
    input("Press Enter to start turning left.")
    

    data,t_vec = [],[]
    t0 = time.time()
    while angle<85.0:
        left()
        data.append(get_gyro())
        t_vec.append(time.time()-t0)
        data_offseted = np.array(data)[:,rot_axis]-gyro_offsets[rot_axis]
        integ1_array = cumtrapz(data_offseted,x=t_vec) # integrate once in time
        try:
            angle = integ1_array[-1]
        except:
            pass
    stop()
    print("Turn completed")

    print("Angle turned: {0:2.2f} degrees".format(angle))


        
        
if __name__ == '__main__':
    main()
