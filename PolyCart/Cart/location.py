from ctypes import CDLL, Structure, c_double, c_int, byref

from serial import Serial


class Location:
    serial: Serial = None
    calc = None
    # anchor_location = ((0.0, 0.0, 0.0),
    #                    (4.0, 7.8, 0.0),
    #                    (0.8, 10.2, 0.0))
    anchor_location = ((0.0, 0.0, 0.0),
                       (2.25, 0.0, 0.0),
                       (0.0, 2.25, 0.0))
    SO_PATH = './trilateration.so'
    SERIAL_PATH = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

    @classmethod
    def get_pos(cls):
        """
        @return: a float tuple (x, y, z) in meter.
            If an error occurred, return None.
        """
        try:
            if cls.serial is None:
                try:
                    cls.serial = Serial(cls.SERIAL_PATH, 115200)
                except Exception as e:
                    print(e)
                    return None
            else:
                cls.serial.close()
                cls.serial.open()

            anchor_distance: tuple = cls._get_anchor_distance()
            if anchor_distance is None:
                return None

            if cls.calc is None:
                cls.calc = CDLL(cls.SO_PATH)

                class vec3d(Structure):
                    _fields_ = [('x', c_double),
                                ('y', c_double),
                                ('z', c_double)]

                cls.vec3d = vec3d
                cls.vec3d4 = vec3d * 4
                cls.int4 = c_int * 4
                cls.anchorArray = cls.vec3d4()
                for i in range(3):
                    cls.anchorArray[i].x = cls.anchor_location[i][0]
                    cls.anchorArray[i].y = cls.anchor_location[i][1]
                    cls.anchorArray[i].z = cls.anchor_location[i][2]
                cls.report = cls.vec3d()
                cls.Range_deca = cls.int4()

            for i in range(3):
                cls.Range_deca[i] = anchor_distance[i]
            result = cls.calc.GetLocation(byref(cls.report), 0, cls.anchorArray, cls.Range_deca)
            if result == -1:
                print('result == -1')
                return None
            return cls.report.x, cls.report.y, cls.report.z
        except Exception as e:
            print(e)
            return None

    @classmethod
    def _get_anchor_distance(cls):
        """
        @return: a int tuple (x, y, z). If an error occurred, return None.
        """
        cls.serial.read_until(b'\r\n')
        mc_messages = ''
        while 'mc' not in mc_messages:
            mc_messages = cls.serial.readline().decode().strip()

        '''The “mr” message consists of tag to anchor raw ranges, “mc” tag to anchor range bias corrected
        ranges – used for tag location and “ma” anchor to anchor range bias corrected ranges – used for
        anchor auto-positioning.

        MID MASK RANGE0 RANGE1 RANGE2 RANGE3 NRANGES RSEQ DEBUG aT:A
        MID this is the message ID, as described above: mr, mc and ma
        MASK this states which RANGEs are valid, if MASK=7 then only RANGE0, RANGE1 and RANGE2
        are valid (in hex, 8-bit number)
        RANGE0 this is tag to anchor ID 0 range if MID = mc/mr (in mm, 32-bit hex number)
        RANGE1 this is tag to anchor ID 1 range if MID = mc/mr or anchor 0 to anchor 1 range if MID =
        ma (in mm, 32-bit hex number)
        RANGE2 this is tag to anchor ID 2 range if MID = mc/mr or anchor 0 to anchor 2 range if MID =
        ma (in mm, 32-bit hex number)
        RANGE3 this is tag to anchor ID 3 range if MID = mc/mr or anchor 1 to anchor 2 range if MID =
        ma (in mm, 32-bit hex number)
        NRANGES this is a number of ranges completed by reporting unit raw range (16-bit hex number)
        RSEQ this is the range sequence number (8-bit hex number)
        DEBUG this is the TX/RX antenna delays (if MID = ma) – two 16-bit numbers or time of last
        range reported – if MID = mc/mr (32 bit hex number)
        aT:A the T is the tag ID and A id the anchor ID
        '''
        entry_items = mc_messages.split()
        mask = int(entry_items[1], 16)
        if mask != 7:
            print('mask != 7, mask = %i' % mask)
            return None
        x = int(entry_items[2], 16)
        y = int(entry_items[3], 16)
        z = int(entry_items[4], 16)
        return x, y, z


if __name__ == '__main__':
    while True:
        print(Location.get_pos())
