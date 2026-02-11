import math
def classify(rgb):
    mag = math.sqrt(rgb[0]**2 + rgb[1]**2 + rgb[2]**2)
    for i in range(3):
        rgb[i] = rgb[i] / mag
    omega = math.atan(math.asin(rgb[2]) / math.atan(rgb[0] * rgb[2] / rgb[1]))
    color = ""
    if (omega <= 0.23):
        color = "red"
    elif (omega <= 0.5):
        color = "orange"
    elif (omega <= 0.9):
        color = "purple"
    elif (omega <= 1.5):
        color = "green"
    return color
