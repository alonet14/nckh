import serial
import time
import schedule
import pathlib

def read_data_temp():
    def main_func():
        # collect
        arduino = serial.Serial('COM5', 9600)
        print('Established serial connection to Arduino')
        arduino_data = arduino.readline()
        decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
        print(f'Collected readings from Arduino: {decoded_values}')
        parent_path = str(pathlib.Path(__file__).parent.parent.parent) + "\\data\\temp"
        file_path = parent_path + '\\temp.txt'
        with open(file_path, 'w', newline='') as file_temp:
            file_temp.write(decoded_values)
            file_temp.close()
        arduino.close()
        print('Connection closed')
        print('<----------------------------->')


    # ----------------------------------------Main Code------------------------------------
    print('Program started')

    # Setting up the Arduino
    schedule.every(5).seconds.do(main_func)

    while True:
        schedule.run_pending()
        time.sleep(1)