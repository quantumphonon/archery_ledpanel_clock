from PIL import Image, ImageDraw, ImageFont
import numpy

def main():
    # screen parameters
    size = [96, 192]

    # fonts loading
    font_time_small = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 60)
    font_time_big = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 90)
    font_line = ImageFont.truetype("./bindings/python/samples/ARIALBD.TTF", 30)

    # example data
    line_code = 6
    time = "10"
    background_code = 2

    # program
    

    background_color, text_color = color_code_to_color(background_code)
    print(background_color, text_color)

    image = Image.fromarray(numpy.full((size[0], size[1], 3), background_color, dtype=numpy.uint8))
    image_with_text = ImageDraw.Draw(image)

    line_text = line_code_to_text(line_code)
    print(line_text)
    if line_text:
        font_time = font_time_small
        line_text_width = image_with_text.textlength(line_text, font=font_line)
        image_with_text.text((int((size[1]-line_text_width)/2),66), line_text, font=font_line, fill=text_color)
    else:
        font_time = font_time_big
    time = str(time)
    time_width = image_with_text.textlength(time, font=font_time)
    image_with_text.text((int((size[1]-time_width)/2),2), time, font=font_time, fill=text_color)
    image.show()


def line_code_to_text(line_code):
    if line_code == 5:
        return "AB"
    elif line_code == 6:
        return "CD"
    return ""


def color_code_to_color(color_code):
    if color_code == 2:
        yellow = (255, 255, 0)
        black = (0,0,0)
        return yellow, black
    elif color_code == 3:
        green = (0,128,0)
        white = (255,255,255)
        return green, white
    red = (255,0,0)
    white = (255,255,255)
    return red, white
    

if __name__ == "__main__":
    main()