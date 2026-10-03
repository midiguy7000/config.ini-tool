import moviepy
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import sys
import os
import time
import subprocess
import math
from Extra import common

def make_input_display(raw_input_text, config_id, font, recolored_images, w, ow):
    args = raw_input_text.split(',')
    A = int(args[0])
    B = int(args[1])
    L = int(args[2])
    X = int(args[5])
    Y = int(args[6])
    T = int(args[7])

    color_stick_text_tmp = common.get_color(config_id.get('color_stick_text'))
    color_stick_text = tuple(color_stick_text_tmp[:3])

    if config_id.getboolean('draw_box'):
        output = recolored_images['background'].copy()
    else:
        output = Image.new('RGBA', (400,250), (255, 0, 0, 0))

    if A == 0:
        recolored_key = f'button_{w}_{ow}|color_a_button'
        output.alpha_composite(recolored_images[recolored_key], (267,114))
    elif A ==1 :
        recolored_key = f'button_filled_{w}_{ow}|color_a_button'
        output.alpha_composite(recolored_images[recolored_key], (267,114))

    if B == 0:
        recolored_key = f'shoulder_{w}_{ow}|color_shoulder_right'
        output.alpha_composite(recolored_images[recolored_key], (236, 46))
    elif B ==1 :
        recolored_key = f'shoulder_filled_{w}_{ow}|color_shoulder_right'
        output.alpha_composite(recolored_images[recolored_key], (236,46))
        
    if L == 0:
        recolored_key = f'shoulder_{w}_{ow}|color_shoulder_left'
        output.alpha_composite(recolored_images[recolored_key], (56,46))
    elif L ==1 :
        recolored_key = f'shoulder_filled_{w}_{ow}|color_shoulder_left'
        output.alpha_composite(recolored_images[recolored_key], (56,46))

    recolored_key = f'dpad_fill_{T}'
    output.alpha_composite(recolored_images[recolored_key], (57,107))

    recolored_key = f'dpad_{w}_{ow}|color_dpad'
    output.alpha_composite(recolored_images[recolored_key], (47,97))      


    recolored_key = f'analog_base_{w}_{ow}|color_analog'
    output.alpha_composite(recolored_images[recolored_key], (152,94)) 

    recolored_key = f'analog_outer_{w}_{ow}|color_analog'
    output.alpha_composite(recolored_images[recolored_key], (155 + X * 3,97 - Y * 3))

    if config_id.getboolean('draw_box'):
        recolored_key = f'analog_bg_part1_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 34 + X * 3,97 + 20 - Y * 3))
        recolored_key = f'analog_bg_part2_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 27 + X * 3,97 + 25 - Y * 3))
        recolored_key = f'analog_bg_part3_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 21 + X * 3,97 + 31 - Y * 3))
        recolored_key = f'analog_bg_part4_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 27 + X * 3,97 + 64 - Y * 3))
        recolored_key = f'analog_bg_part5_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 34 + X * 3,97 + 70 - Y * 3))

    else:
        recolored_key = f'analog_part1_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 34 + X * 3,97 + 20 - Y * 3))
        recolored_key = f'analog_part2_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 27 + X * 3,97 + 25 - Y * 3))
        recolored_key = f'analog_part3_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 21 + X * 3,97 + 31 - Y * 3))
        recolored_key = f'analog_part4_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 27 + X * 3,97 + 64 - Y * 3))
        recolored_key = f'analog_part5_{w}_{ow}|color_analog'
        output.paste(recolored_images[recolored_key], (155 + 34 + X * 3,97 + 70 - Y * 3))

    scaling = config_id.getfloat('scaling')
    if config_id.getboolean('draw_stick_text'):
        stick_text_size = config_id.getint('stick_text_size')
        ID = ImageDraw.Draw(output)
        text = f'({"+" if X>0 else ("+" if X==0 else '')}{X},{"+" if Y>0 else ("+" if Y==0 else '')}{Y})'
        ID.text((132 + round(36 - stick_text_size)*scaling, 198 + (36 - stick_text_size)//scaling), text, font = font, fill = color_stick_text, stroke_width = 3 if ow >= 3 else 2, stroke_fill = (0,0,0))

    if scaling != 1.0:
        resample_filter = common.get_resampler(config_id.get('scaling_option'))
        output = output.resize((round(400*scaling), round(250*scaling)), resample_filter)

    for filtre in common.get_filter_list(config_id.get('special_effects')):
        output = output.filter(filtre)

    return output

def add_input_display(image, frame_dict, config, font_folder, recolored_images, w, ow):
    state, state_counter = int(frame_dict['state']), int(frame_dict['state_counter'])
    stick_text_size = config['Input display'].getint('stick_text_size')
    font = ImageFont.truetype(os.path.join(font_folder, 'FOT-Rodin Pro EB.otf'), stick_text_size)
    input_display = make_input_display(frame_dict['input'], config['Input display'], font, recolored_images, w, ow)
    top_left_text = config['Input display'].get('top_left').split(',')
    top_left = round(float(top_left_text[0])*image.width), round(float(top_left_text[1])*image.height)


    if config['Input display'].getboolean('fade_animation'):
        input_display = common.fade_image_manually(input_display, frame_dict)
        

    if config['Input display'].getboolean('fly_animation'):

        if state == 1 and state_counter <= 10:
            return None
        
        offset = common.fly_in(frame_dict, image.height)

        if state == 4 and 192 < state_counter < 202:
            image.alpha_composite(input_display, (round(top_left[0] - image.width*offset), top_left[1]))
            return None

        ITEM_POSITION = 381/1440
        INPUT_DISPLAY_POSITION = (1 - float(top_left_text[1]))
        height_correction =  round((INPUT_DISPLAY_POSITION - ITEM_POSITION)*image.height)
        
        if offset is not None:
            if config['Input display'].get('fly_in_direction') == 'bottom':
                image.alpha_composite(input_display, (top_left[0], image.height - height_correction - offset))
            else: 
                image.alpha_composite(input_display, (top_left[0], top_left[1] - round(ITEM_POSITION*image.height) + offset))
        else:
            image.alpha_composite(input_display, top_left)
    else:
        image.alpha_composite(input_display, top_left)
        
