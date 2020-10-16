# -*- coding: utf-8 -*-
import math
###
### 牛顿迭代法的一个案例：由周期和水深推算波长
###
class NewtonMethod():
    G = 9.810000
    DE = 0.0001
    ''' period 周期
        depth 水深
    '''

    def GetWaveLenth(self, period, depth):
        l = (self.G * period * period)/(2.00000 * math.pi)
        s = 1
        while s > self.DE:
            result = (( self.G * period * period)/(2.0000000 * math.pi)) * math.tanh((2.000000 * math.pi / l) * depth)
            s = math.fabs(result - l)
            l = result
        return result


if __name__ == '__main__':
    newtonmethod = NewtonMethod()
    print(newtonmethod.GetWaveLenth(11.1, 9.71))

