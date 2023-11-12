import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline

from filtro import Filtro


def add_noise(input, stddev):
    noise = np.zeros(input.shape, input.dtype)
    cv2.randn(noise, (0, 0, 0), stddev)
    output = cv2.add(input, noise)
    return output


def adjust_brightness(input, intensity=20):
    output = cv2.convertScaleAbs(input, alpha=1, beta=intensity)
    return output


def increase_color_temperature(input):
    increase_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 80, 155, 255])(range(256))

    decrease_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 50, 100, 255])(range(256))

    blue_channel, green_channel, red_channel = cv2.split(input)

    red_channel = cv2.LUT(red_channel, increase_table).astype(np.uint8)

    blue_channel = cv2.LUT(blue_channel, decrease_table).astype(np.uint8)

    return cv2.merge((blue_channel, green_channel, red_channel))


def adjust_color_temperature(input, red, blue):
    red_table = UnivariateSpline(x=[0, 64, 128, 255], y=red)(range(256))

    blue_table = UnivariateSpline(x=[0, 64, 128, 255], y=blue)(range(256))

    blue_channel, green_channel, red_channel = cv2.split(input)

    red_channel = cv2.LUT(red_channel, red_table).astype(np.uint8)

    blue_channel = cv2.LUT(blue_channel, blue_table).astype(np.uint8)

    return cv2.merge((blue_channel, green_channel, red_channel))


def adjust_colors(input, red=[0, 64, 128, 255], blue=[0, 64, 128, 255], green=[0, 64, 128, 255]):
    red_table = UnivariateSpline(x=[0, 64, 128, 255], y=red)(range(256))

    blue_table = UnivariateSpline(x=[0, 64, 128, 255], y=blue)(range(256))

    green_table = UnivariateSpline(x=[0, 64, 128, 255], y=green)(range(256))

    blue_channel, green_channel, red_channel = cv2.split(input)

    red_channel = cv2.LUT(red_channel, red_table).astype(np.uint8)

    blue_channel = cv2.LUT(blue_channel, blue_table).astype(np.uint8)

    green_channel = cv2.LUT(green_channel, green_table).astype(np.uint8)

    return cv2.merge((blue_channel, green_channel, red_channel))


def adjust_red_tint(input, x, y):
    increase_table = UnivariateSpline(x, y)(range(256))

    blue_channel, green_channel, red_channel = cv2.split(input)

    red_channel = cv2.LUT(red_channel, increase_table).astype(np.uint8)

    return cv2.merge((blue_channel, green_channel, red_channel))


def apply_paris(input):
    output = adjust_brightness(input, 20)
    output = cv2.GaussianBlur(output, (1, 1), 0)
    return output


def apply_los_angeles(input):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    output = cv2.filter2D(input, ddepth=-1, kernel=kernel)
    return increase_color_temperature(output)


def apply_oslo(input):
    output = cv2.convertScaleAbs(input, alpha=0.9, beta=0)
    return output


def apply_lagos(input):
    output = adjust_brightness(input, 40)
    output = cv2.convertScaleAbs(output, alpha=0.8, beta=0)
    output = adjust_red_tint(output, [0, 25, 100, 255], [5, 35, 100, 255])
    return output


def apply_abu_dhabi(input):
    output = cv2.GaussianBlur(input, (3, 3), 0)
    output = adjust_brightness(output, 10)
    output = adjust_color_temperature(output, [0, 55, 130, 255], [0, 50, 130, 255])
    return output


def apply_buenos_aires(input):
    output = adjust_brightness(input, 10)
    output = adjust_color_temperature(output, [0, 55, 80, 255], [0, 70, 160, 255])
    return output


def apply_new_york(input):
    output = adjust_brightness(input, 10)
    output = adjust_color_temperature(output, [0, 50, 80, 255], [0, 70, 100, 255])
    return output


def apply_jaipur(input):
    output = adjust_brightness(input, 35)
    output = adjust_red_tint(output, [0, 50, 80, 255], [0, 70, 100, 255])
    return output


def apply_tokyo(input):
    output = adjust_brightness(input, -30)
    output = add_noise(output, (20, 20, 20))
    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    return output


def apply_sao_hell(input):
    red = [10, 120, 160, 255]
    blue = [10, 64, 180, 255]
    green = [10, 80, 128, 255]
    output = adjust_colors(input, red, blue, green)
    return output


nenhum = Filtro("Nenhum", lambda x: x)
sao_hell = Filtro("São Hell", apply_sao_hell)
tokyo = Filtro("Tokyo", apply_tokyo)
jaipur = Filtro("Jaipur", apply_jaipur)
new_york = Filtro("New York", apply_new_york)
buenos_aires = Filtro("Buenos Aires", apply_buenos_aires)
abu_dhabi = Filtro("Abu Dhabi", apply_abu_dhabi)
lagos = Filtro("Lagos", apply_lagos)
oslo = Filtro("Oslo", apply_oslo)
los_angeles = Filtro("Los Angeles", apply_los_angeles)
paris = Filtro("Paris", apply_paris)

filtros = [nenhum, paris, los_angeles, oslo, lagos, abu_dhabi, buenos_aires, new_york, jaipur, tokyo, sao_hell]
