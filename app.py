import math as maths

import app

from power import BatteryLevel
from events.input import Buttons, BUTTON_TYPES


MAX_BATTERY = 106.25
SCREEN_RADIUS = 120

def battery_level():
    return BatteryLevel() / MAX_BATTERY


def bar_area(height: float):
    """
    Finds the area of the circle of radius 0.5
    taken up by a bar of the given height

    segment = sector - triangle

    triangle = sin(a) / 2
    sector = a / 2

    he = 1 - h

    a = arccos(he)

    so segment = arccos(1 - h) - sin(arccos(1 - h)) / 2
    """
    # calculations are simpler for a circle of radius 1
    height *= 2

    if height == 1:
        return 0.5
    elif height > 1:
        return 1 - bar_area(1 - height / 2)

    angle = 2 * maths.acos(1 - height)
    triangle_area = maths.sin(angle) / 2
    sector_area = angle / 2
    segment_area = sector_area - triangle_area
    return segment_area / maths.pi


N_LUT = 101
heights = [i / (N_LUT - 1) for i in range(N_LUT)]
areas = [bar_area(h) for h in heights]


def bar_height(fraction: float):
    """
    Finds the height such that a bar takes up the appropriate area.
    """
    for h, a in zip(heights, areas):
        if a > fraction:
            return h
    else:
        return h

class BlaineApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        ctx.save()

        h = bar_height(battery_level())

        ctx.rgb(0,0,0).rectangle(-120,-120,240,240).fill()
        ctx.rgb(1,1,1).rectangle(-120,-120+(1-h)*240,240,h*240).fill()

        label = f"battery: {battery_level()*100:.1f}%"
        ctx.rgb(1,0,0).move_to(-80,0).text(label)
        ctx.restore()


__app_export__ = BlaineApp
