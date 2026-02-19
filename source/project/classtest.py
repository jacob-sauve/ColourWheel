"""
Color classification script.
Uses 'omega value' calculated according to our formula and checks against saved
standard values.
v 2.0
2026-02-19
"""

# imports
import math


# constants
OMEGA_THRESHOLDS = [        # max omega values at which colors are classified
        (0.75, "orange"),
        (1.05, "yellow"),
        (1.4, "blue"),
        (math.inf, "green") # i.e., all omega values above 1.4 are green
        ]


def classify(rgb, debugging=False):
    """Classify rgb value as one of the four saved colours
    Keyword arguments:
        rgb         -- list of (R,G,B) values to be classified
        debugging   -- flag to toggle informative print statements on/off when True/False (default False)
    Outputs:
        color       -- string indicating which colour the (R,G,B) corresponds to
    """
    # 1) normalise RGB values
    mag = math.sqrt(rgb[0]**2 + rgb[1]**2 + rgb[2]**2)
    for i in range(3):
        rgb[i] = rgb[i] / mag

    # 2) calculate color's 'omega' value
    omega = math.atan(math.asin(rgb[2]) / math.atan(rgb[0] * rgb[2] / rgb[1]))

    # 3) classify color
    for threshold, color in OMEGA_THRESHOLDS:
        if (omega <= threshold):
            if debugging:
                print(omega)
                print(color)
            return color
