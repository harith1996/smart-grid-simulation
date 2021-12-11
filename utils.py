def color_mapper(charge):
    rgbcolor = None
    if (charge < 0.07):
        rgbcolor = 'rgb(232, 44, 44)'
    elif (charge < 0.14):
        rgbcolor = 'rgb(227, 57, 44)'
    elif (charge < 0.21):
        rgbcolor = 'rgb(222, 70, 44)'
    elif (charge < 0.28):
        rgbcolor = 'rgb(217, 84, 44)'
    elif (charge < 0.35):
        rgbcolor = 'rgb(213, 97, 44)'
    elif (charge < 0.42):
        rgbcolor = 'rgb(208, 111, 44)'
    elif (charge < 0.49):
        rgbcolor = 'rgb(203, 124, 44)'
    elif (charge < 0.56):
        rgbcolor = 'rgb(199, 138, 44)'
    elif (charge < 0.63):
        rgbcolor = 'rgb(194, 151, 44)'
    elif (charge < 0.7):
        rgbcolor = 'rgb(189, 164, 44)'
    elif (charge < 0.77):
        rgbcolor = 'rgb(184, 178, 44)'
    elif (charge < 0.84):
        rgbcolor = 'rgb(180, 191, 44)'
    elif (charge < 0.91):
        rgbcolor = 'rgb(175, 205, 44)'
    elif (charge < 0.98):
        rgbcolor = 'rgb(170, 218, 44)'
    else:
        rgbcolor = 'rgb(166, 232, 44)'
    return rgbcolor


def convert_price( price):
    return round(price * 3600 * 1000, 2)