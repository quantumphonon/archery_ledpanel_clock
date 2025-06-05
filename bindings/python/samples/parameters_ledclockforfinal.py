from PIL import ImageFont, ImageDraw, Image

# definition of parameters
# colors for display
blue = (255, 0, 0)
red = (0, 0, 255)
green = (0, 127, 0)
yellow = (0, 255, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# screen size
screen_height = 32*3
screen_width = 64*3*4

# fonts for dispaly
font_size_clock = 50
font_size_score = 30
font_size_arrows = 30
font_size = 30
font_clock = ImageFont.truetype("./ARIALBD.TTF"  , font_size_clock)
font_default = ImageFont.truetype("./ARIALBD.TTF", font_size)
font_arrows = ImageFont.truetype("./ARIAL.TTF", font_size_arrows)
font_score = ImageFont.truetype("./ARIALBD.TTF"  , font_size_score)