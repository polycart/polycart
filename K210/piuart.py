# Untitled - By: leylee - 周四 7月 2 2020

from machine import UART
from utime import sleep_ms
from ujson import dumps

class PiUART(UART):
    fm.register(board_info.PIN10,fm.fpioa.UART2_TX)
    fm.register(board_info.PIN11,fm.fpioa.UART2_RX)
    count = 0
    instance = None

    def __init__(self):
        self.products = [{'abc': 123}];
        super().__init__(UART.UART2, 115200)

    @classmethod
    def get_instance(cls):
        if cls.instance:
            cls.instance.init(115200)
        else:
            cls.instance = cls()
        return cls.instance

    def wait_for_get(self):
        while True:
            self.read(self.any())
            sleep_ms(400)
            if self.any():
                byte_data = self.read(self.any())
                print('Recieved data:', byte_data)
                if b'GET' in byte_data:
                    print('GET command in data')
                    return
                else:
                    print('No Get command in data')

    def start_daemon(self):
        while True:
            self.wait_for_get()
            self.write(b'OK\r\n')
            sleep_ms(5000) #TODO: update self.products
            byte_response = dumps(self.products).encode() + b'\r\n'
            self.write(byte_response)
            print('Response:', byte_response)

if __name__ == '__main__':
    PiUART.get_instance().start_daemon()
