import math


from pywebio.input import *
from pywebio.output import *


def bmi():
    height = input("Your height is (cm)", type=FLOAT)
    weight = input("Your weight is (kg)", type=FLOAT)

    BMI = weight / math.pow(height / 100, 2)

    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'),
                  (22.9, '正常'), (27.5, '过重'),
                  (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    for top, status in zip(top_status):
        if BMI <= top:
            put_text(f"Your BMI is {BMI}, body status is{status}")
            break


if __name__ == '__main__':
    bmi()
