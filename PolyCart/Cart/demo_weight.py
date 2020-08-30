from hx711 import HX711
from RPi import GPIO


class Weight:
    zero_weight = 10000
    five_hundred_weight = 50000

    @classmethod
    def get_weight(cls, print_raw=False):
        return 800.0
        try:
            hx711 = HX711(
                dout_pin=5,
                pd_sck_pin=6,
                channel='A',
                gain=64
            )

            hx711.reset()
            times = 3
            raw_weights = hx711.get_raw_data(times)
            raw_weight = sum(raw_weights) / times
            if (print_raw):
                print('raw_weight: %i' % raw_weight)
            return cls._calc_weight_in_gram(raw_weight)
        except Exception as e:
            print('重量读取失败: ', e)
            return None
        finally:
            GPIO.cleanup()

    @classmethod
    def _calc_weight_in_gram(cls, weight):
        return (weight - cls.zero_weight) / (cls.five_hundred_weight - cls.zero_weight) * 500

if __name__ == '__main__':
    import time
    while True:
        print(Weight.get_weight(print_raw=True))
        # time.sleep(0.5)