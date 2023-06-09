# trig functions in degrees instead of radians
import math


def sin_d(angle_deg):
    ans = math.sin(math.radians(angle_deg))
    return ans


def cos_d(angle_deg):
    ans = math.cos(math.radians(angle_deg))
    return ans


def asin_d(input_num):
    ans = math.degrees(math.asin(input_num))
    return ans


def acos_d(input_num):
    ans = math.degrees(math.acos(input_num))
    return ans
