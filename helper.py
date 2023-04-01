import math

def distance_calc(array1, array2):
    distance = 0 
    for value in zip(array1, array2):
        distance += (value[0] - value[1])**2
    return round(math.sqrt(distance))

def distance_Metric(input_RGB):
    """
    input_RGB: array of RGB values
    """
    hsv = True
    face_colour = ["U - Blue", "B - Yellow", "L - Orange", "R - Red", "D - Green", "F - White"]
    colour_values = [[103,  49,   8],
    [ 41, 168, 176],
    [ 63,  93, 226],
    [ 30,  21, 134],
    [ 6, 108,   0],
    [146, 160, 179]
    ]
    if hsv:
        colour_values = [[113,195,132],
        [ 10, 135, 189],
        [ 66, 109, 212],
        [ 30,  37, 152],
        [ 16, 67,   1],
        [200, 209, 191]
        ]

    distances = []
    for colour in colour_values:
        distances.append(distance_calc(colour, input_RGB))
    return face_colour[distances.index(min(distances))], distances

def getPixelColour(square):
    # print(square)
    if square[0] >= 200:
        return "F - White" # White
    elif square[0] >= 100:
        return "U - Blue" # Blue
    elif square[2] <= 100:
        return "D - Green" # Green
    elif square[2] <= 175:
        return "R - Red" # Red
    elif square[1] <= 140:
        return "L - Orange" # Orange
    else:
        return "B - Yellow" # Yellow