import serial, json

class UARTTimeoutError(TimeoutError):
    def __init__(self, *arg):
        self.args = arg


class K210UART(serial.Serial):
    def __init__(self, port_path: str = '/dev/ttyS0', bits=115200):
        """
        port_path 为串口号 (Windows) 或串口文件 (*nix), bits 为比特率
        """
        super().__init__(port_path, bits)

    def get_products(self):
        """
        阻塞式获取商品信息.
        若连接 K210 失败, 将抛出 UARTTimeoutError.
        """
        if not self.is_open:
            self.open()
        self.flushInput()
        self.write(b'GET\r\n')

        self.timeout = 0.7
        response = self.read_until(b'\r\n')
        if not response.endswith(b'OK\r\n'):
            raise UARTTimeoutError('K210 no response')

        self.timeout = None
        byte_data = self.read_until(b'\r\n')
        return json.loads(byte_data.decode())

if __name__ == '__main__':
    uart = K210UART()
    print('K210 UART 测试')
    print('端口:', uart.port)
    print('波特率', uart.baudrate)
    print('开始获取产品信息...')
    print(uart.get_products())
    print('测试结束')
