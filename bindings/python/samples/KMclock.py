#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time


class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/10x20.bdf")
        red = graphics.Color(150, 0, 0)
        graphics.DrawLine(canvas, 5, 5, 22, 13, red)
        
        green = graphics.Color(0, 255, 0)


        white = graphics.Color(255, 255, 255)
        for i in range(100):
        
            for i in range(32):
                graphics.DrawLine(canvas, 0, i, 63, i, green)
            

            graphics.DrawText(canvas, font, 2, 30, white, "ABCDEF")
        time.sleep(10)   # show display for 10 seconds before exit


# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
