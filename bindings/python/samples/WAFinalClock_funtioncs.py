import parameters_ledclockforfinal as parameters
import WAFinalClock_funtioncs as finaloutput
import numpy
from PIL import Image, ImageDraw, ImageFont

class ClockForFinals():
    def __init__(self, width, height, matrix, clock_id):
        self.image = Image.fromarray(numpy.full((height, width, 3), parameters.blue, dtype=numpy.uint8))
        self.width = width
        self.height = height
        self.time = {"time1": 0,
                     "light1": 0,
                     "time2": 0,
                     "light2": 0
                    }
        self.score = {"live": 0}
        self.matrix = matrix
        self.clock_id = int(clock_id)

    def update_timing(self, time_data):
        left_time_image = finaloutput.generate_time_image(self.height, time_data['time1'], time_data['light1'])
        self.image.paste(left_time_image, (0, 0))
        right_time_image = finaloutput.generate_time_image(self.height, time_data['time2'], time_data['light2'])
        self.image.paste(right_time_image, (self.width-self.height, 0))
        self.time = time_data
        black_bar = Image.fromarray(numpy.full((96, 4, 3), parameters.black, dtype=numpy.uint8))
        if(self.clock_id % 2 == 1):
            self.image.paste(black_bar, (0, 0))
        self.matrix.SetImage(self.image.crop(((self.clock_id-1)*192,0,self.clock_id*192,95)).convert('RGB'))

    def update_scores(self, scores):
        scores_image = finaloutput.generate_score_image(self.height, self.width-2*self.height, scores)
        self.image.paste(scores_image, (self.height, 0))
        self.score = scores
        black_bar = Image.fromarray(numpy.full((96, 4, 3), parameters.black, dtype=numpy.uint8))
        if(self.clock_id % 2 == 1):
            self.image.paste(black_bar, (0, 0))
        self.matrix.SetImage(self.image.crop(((self.clock_id-1)*192,0,self.clock_id*192,95)).convert('RGB'))

def light_signal_to_color(light_signal):
    match light_signal:
        case 0:
            return parameters.red
        case 2:
            return parameters.yellow
        case 3:
            return parameters.green
    return parameters.red

def light_signal_to_font_color(light_signal):
    match light_signal:
        case 0:
            return parameters.white
        case 2:
            return parameters.black
        case 3:
            return parameters.white
    return parameters.white

def generate_time_image(size, time, light_signal):
    background_color = light_signal_to_color(light_signal)
    text_color = light_signal_to_font_color(light_signal)
    time_image = Image.fromarray(numpy.full((size, size, 3), background_color, dtype=numpy.uint8))
    time_image_with_text = ImageDraw.Draw(time_image)
    time_text_width = time_image_with_text.textlength(str(time), font=parameters.font_clock)
    time_image_with_text.text((int((size-time_text_width)/2),int((size-parameters.font_size_clock)/2)), str(time), font=parameters.font_clock, fill=text_color)
    return time_image

def generate_score_image(height, width, scores):
    scores_image = Image.fromarray(numpy.full((height, width, 3), parameters.blue, dtype=numpy.uint8))
    # separation_bar = Image.fromarray(numpy.full((height, 4, 3), parameters.black, dtype=numpy.uint8))
    # scores_image.paste(separation_bar, (int(width/2-2),0))
    if not scores['live']:
        return scores_image
    names_to_display  = reduce_team_name_size(scores['archer'], scores['team'])
    add_archers_names(scores_image, height, width, names_to_display)
    if not scores['tiebreak']:
        add_total_scores(scores_image, height, width, scores['match_mode'], scores['setscore'], scores['score'])
        add_arrows(scores_image, height, width, scores['arrows'], int(scores['fin_arrows']))
    if scores['tiebreak'] and not scores['team']:
        add_total_scores(scores_image, height, width, scores['match_mode'], [0, 0], scores['score'])
        add_individual_tiebreak(scores_image, height, width, scores['tiebreak_result'])
    if scores['tiebreak'] and scores['team']:
        last_shootoff_result = get_last_shootoff_result(scores['tiebreak_result'])
        add_total_scores(scores_image, height, width, scores['match_mode'], last_shootoff_result, scores['score'])
        add_arrows(scores_image, height, width, scores['tiebreak_arrows'], int(scores['fin_so_arrows']))
    return scores_image


def reduce_team_name_size(archers_name, team_match):
    if team_match:
        reduce_names=[]
        for name in archers_name:
            upper_word_list = []
            for word in name.split(" "):
                if word.isupper():
                    upper_word_list.append(word)
            reduce_names.append(" ".join(upper_word_list))
        return reduce_names


    return archers_name


def add_archers_names(image, height, width, archers_names):
    scores_image_with_text = ImageDraw.Draw(image)
    font_to_use = adjust_given_font_so_names_fit(scores_image_with_text, archers_names, width, parameters.font_default, parameters.font_size)
    scores_image_with_text.text((10,0), archers_names[0], font=font_to_use, fill=parameters.white)
    text_length = scores_image_with_text.textlength(archers_names[1], font=font_to_use)
    scores_image_with_text.text((width-text_length-10,0), archers_names[1], font=font_to_use, fill=parameters.white)


def adjust_given_font_so_names_fit(scores_image_with_text, archers_names, width, given_font, font_size):
    max_name_length = 0
    for name in archers_names:
        name_length = scores_image_with_text.textlength(name, font=given_font)
        if name_length>max_name_length:
            max_name_length = name_length
    available_space = width/2 - 20
    if max_name_length > available_space:
        return ImageFont.truetype("./ARIALBD.TTF", numpy.floor(font_size/max_name_length*available_space))
    return given_font

def add_individual_tiebreak(image, height, width, tiebreak):
    scores_image_with_text = ImageDraw.Draw(image)
    text_length = scores_image_with_text.textlength(tiebreak[0], font=parameters.font_arrows)
    scores_image_with_text.text((int(width/4-text_length/2),int(height*1/3)), tiebreak[0], font=parameters.font_arrows, fill=parameters.white)

    text_length = scores_image_with_text.textlength(tiebreak[1], font=parameters.font_arrows)
    scores_image_with_text.text((int(width*3/4-text_length/2),int(height*1/3)), tiebreak[1], font=parameters.font_arrows, fill=parameters.white)


def add_total_scores(image, height, width, match_mode, setscores, totalscores):
    scores_image_with_text = ImageDraw.Draw(image)

    #add description text for set/end sum
    scores_image_with_text.text((10,int(height*2/3)), "Sum", font=parameters.font_arrows, fill=parameters.white)
    text_length = scores_image_with_text.textlength("Sum 88", font=parameters.font_default)
    scores_image_with_text.text((width-text_length-10,int(height*2/3)), "Sum", font=parameters.font_arrows, fill=parameters.white)

    #add set/end sum
    text_length = scores_image_with_text.textlength("Sum ", font=parameters.font_default)
    scores_image_with_text.text((10+text_length,int(height*2/3)), str(setscores[0]), font=parameters.font_default, fill=parameters.white)
    text_length = scores_image_with_text.textlength("88", font=parameters.font_default)
    scores_image_with_text.text((width-text_length-10,int(height*2/3)), str(setscores[1]), font=parameters.font_default, fill=parameters.white)

    #add description text for total
    text_length = scores_image_with_text.textlength("Total 188", font=parameters.font_default)
    scores_image_with_text.text((int(width/2-text_length),int(height*2/3)), "Total", font=parameters.font_arrows, fill=parameters.white)
    scores_image_with_text.text((int(width/2+10),int(height*2/3)), "Total", font=parameters.font_arrows, fill=parameters.white)

    #add total match 
    text_length = scores_image_with_text.textlength("188", font=parameters.font_default)
    scores_image_with_text.text((int(width/2-text_length),int(height*2/3)), str(totalscores[0]), font=parameters.font_default, fill=parameters.white)
    text_length = scores_image_with_text.textlength("Total ", font=parameters.font_default)
    scores_image_with_text.text((int(width/2+10+text_length),int(height*2/3)), str(totalscores[1]), font=parameters.font_default, fill=parameters.white)


def add_arrows(image, height, width, arrows, number_of_arrows_per_end):
    scores_image_with_text = ImageDraw.Draw(image)
    arrow_box_width = int(width/2/6)

    arrows_left = arrows[0].split(" ")
    for i, arrow in enumerate(arrows_left):
        text_length = scores_image_with_text.textlength(arrow, font=parameters.font_arrows)
        scores_image_with_text.text((int((i+0.5)*arrow_box_width-text_length/2),int(height*1/3)), arrow, font=parameters.font_default, fill=parameters.white)

    arrows_right = arrows[1].split(" ")
    for i, arrow in enumerate(arrows_right):
        text_length = scores_image_with_text.textlength(arrow, font=parameters.font_arrows)
        scores_image_with_text.text((int(width-arrow_box_width*number_of_arrows_per_end+(i+0.5)*arrow_box_width-text_length/2),int(height*1/3)), arrow, font=parameters.font_default, fill=parameters.white)

def get_last_shootoff_result(shootoffs_results):
    number_of_shootoffs = max(len(shootoffs_results[0].split(",")), len(shootoffs_results[1].split(",")))
    if len(shootoffs_results[0].split(","))==number_of_shootoffs:
        shootoff_left = shootoffs_results[0].split(",")[-1]
    else:
        shootoff_left = "0"

    if len(shootoffs_results[1].split(","))==number_of_shootoffs:
        shootoff_right = shootoffs_results[1].split(",")[-1]
    else:
        shootoff_right = "0"

    return [shootoff_left, shootoff_right]