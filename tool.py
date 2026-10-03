import customtkinter as ctk
import configparser
import tkinter as tk
from tkinter import filedialog
import os
import shutil
import sys

ROOTDIR = 'FrameDumps'
EXTRADIR = 'FrameDumps\\Extra'

try:
    os.mkdir(ROOTDIR)
except FileExistsError:
    shutil.rmtree(ROOTDIR)
    os.mkdir(ROOTDIR)

os.mkdir(EXTRADIR)

VIDEO = 'Video'
AUDIO = 'Audio'
INFODISPLAY = 'IV/EV Display'
SPEEDOMETER = 'Speedometer'
INPUT = 'Input Display'
NAMEDISPLAY = 'Name Display (optional)'
SPEEDDISPLAY = 'Speed Display (optional, advanced)'
EXTRA = 'Extra Display (optional, advanced)'
SAVE = 'Save Config'
MKW_YELLOW = 'F2E622FF'
PURE_WHITE = 'FFFFFFFF'



class ConfigFile(configparser.ConfigParser):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        with open(self.file_path, 'w') as file:
            file.close()

    def create_section(self, section_name: str) -> None:
        self[section_name] = {}

    def create_variable(self, variable: tuple[str], section: str) -> None:
        self[section][variable[0]] = variable[1]

    def write_to_file(self) -> None:
        with open(self.file_path, 'w') as file:
            self.write(file)
            file.close()

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('framedump.ini Configurer')
        self.geometry('1075x500')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')

        self.mainmenu: MainMenu | None = MainMenu(master=self)
        self.mainmenu.grid(row=0, column=0)

class MainMenu(ctk.CTkTabview):
    def __init__(self, master):
        self.master: Window = master
        super().__init__(master, fg_color='transparent')
        self.add(VIDEO)
        self.add(AUDIO)
        self.add(INFODISPLAY)
        self.add(SPEEDOMETER)
        self.add(INPUT)
        self.add(NAMEDISPLAY)
        self.add(SPEEDDISPLAY)
        self.add(EXTRA)
        self.add(SAVE)

        self.flag = False
        self.namedisp_pos = None
        self.input_pos = None
        self.info_pos = None

        #Encoding Options
        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)

        self.encode_style = ctk.CTkComboBox(master=self.tab(VIDEO), values=['Encode style', 'YouTube', 'Discord', 'Standard'])
        self.encode_style.grid(row=0, column=0, pady=10)

        self.preset = ctk.CTkComboBox(master=self.tab(VIDEO), values=['Encode speed', 'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'])
        self.preset.grid(row=1, column=0, pady=10)

        self.resolution = ctk.CTkComboBox(master=self.tab(VIDEO), values=['Resolution', '4K UHD', '1440p', '1080p', '720p'])
        self.resolution.grid(row=2, column=0, pady=10)

        self.scaling = ctk.CTkComboBox(master=self.tab(VIDEO), values=['Scaling', 'Lanczos', 'Bicubic', 'Bilinear'])
        self.scaling.grid(row=3, column=0, pady=10)

        self.threads = ctk.CTkEntry(master=self.tab(VIDEO), placeholder_text='Threads')
        self.threads.grid(row=0, column=1, pady=10, padx=20)

        self.output = ctk.CTkEntry(master=self.tab(VIDEO), placeholder_text='Output file name')
        self.output.grid(row=1, column=1, pady=10, padx=20)

        self.fadein_video = ctk.CTkEntry(master=self.tab(VIDEO), placeholder_text='Fade in (seconds)')
        self.fadein_video.grid(row=2, column=1, pady=10, padx=20)

        self.fadeout_video = ctk.CTkEntry(master=self.tab(VIDEO), placeholder_text='Fade out (seconds)')
        self.fadeout_video.grid(row=3, column=1, pady=10, padx=20)

        #Audio Options
        self.play_audio = ctk.CTkCheckBox(master=self.tab(AUDIO), text='Play in-game audio')
        self.play_audio.grid(row=0, column=0, pady=10)

        self.fadein_audio = ctk.CTkEntry(master=self.tab(AUDIO), placeholder_text='Audio fade in (seconds)', width=162)
        self.fadein_audio.grid(row=1, column=0, pady=10)

        self.fadeout_audio = ctk.CTkEntry(master=self.tab(AUDIO), placeholder_text='Audio fade out (seconds)')
        self.fadeout_audio.grid(row=2, column=0, pady=10, sticky='ew')

        #Infodisplay (note that this section of the config file was split into 2 tabs)
        self.show_infodisplay = ctk.CTkCheckBox(master=self.tab(INFODISPLAY), text='Show IV/EV display')
        self.show_infodisplay.grid(row=0, column=0, pady=10)

        self.type_of_info = ctk.CTkComboBox(master=self.tab(INFODISPLAY), values=['Display Type', 'IV only', 'EV only', 'IV & EV'])
        self.type_of_info.grid(row=1, column=0, pady=10)

        self.infodisplay_btn = ctk.CTkButton(master=self.tab(INFODISPLAY), text='Set position', command=lambda: self.infodisplay_pygame())
        self.infodisplay_btn.grid(row=2, column=0, pady=10)

        #Speedometer
        self.show_speedometer = ctk.CTkCheckBox(master=self.tab(SPEEDOMETER), text='Show speedometer')
        self.show_speedometer.grid(row=0, column=0, pady=10)

        self.speedometer_type = ctk.CTkComboBox(master=self.tab(SPEEDOMETER), values=['Speedometer type', 'IV (Standard)', 'XZ', 'XYZ'], width=162)
        self.speedometer_type.grid(row=1, column=0, pady=10)

        self.speedometer_text = ctk.CTkComboBox(master=self.tab(SPEEDOMETER), values=['Speedometer text', '"SPEED"', '"KM/H"', 'No text'])
        self.speedometer_text.grid(row=2, column=0, pady=10, sticky='ew')

        #Input Display
        self.show_input_display = ctk.CTkCheckBox(master=self.tab(INPUT), text='Show input display')
        self.show_input_display.grid(row=0, column=0, pady=10)

        self.show_stick_display = ctk.CTkCheckBox(master=self.tab(INPUT), text='Show stick display (stick coordinates)')
        self.show_stick_display.grid(row=1, column=0, pady=10)

        self.input_button = ctk.CTkButton(master=self.tab(INPUT), text='Set position', command=lambda: self.input_pygame())
        self.input_button.grid(row=2, column=0, pady=10)

        #Speed Display
        self.show_speed_display = ctk.CTkCheckBox(master=self.tab(SPEEDDISPLAY), text='Show speed display')
        self.show_speed_display.grid(row=0, column=0, pady=10)

        #Name Display
        self.show_name_display = ctk.CTkCheckBox(master=self.tab(NAMEDISPLAY), text='Show name display')
        self.show_name_display.grid(row=0, column=0, pady=10)

        self.use_game_time = ctk.CTkCheckBox(master=self.tab(NAMEDISPLAY), text='Use in-game time')
        self.use_game_time.grid(row=1, column=0, pady=10)

        self.total_authors = ctk.CTkEntry(master=self.tab(NAMEDISPLAY), placeholder_text='Total # of authors')
        self.total_authors.grid(row=2, column=0, pady=10)

        self.name_disp_btn = ctk.CTkButton(master=self.tab(NAMEDISPLAY), text='Edit name display', command=lambda: self.name_display_button())
        self.name_disp_btn.grid(row=3, column=0, pady=10)

        self.namedisp_pos_btn = ctk.CTkButton(master=self.tab(NAMEDISPLAY), text='Set position', command=lambda: self.set_namedisp_pos(self.name_display_pygame()))
        self.namedisp_pos_btn.grid(row=4, column=0, pady=10)

        #Extra Display
        self.show_extra_display = ctk.CTkCheckBox(master=self.tab(EXTRA), text='Show extra display')
        self.show_extra_display.grid(row=0, column=0, pady=10)

        #Generate File
        clear_btn = ctk.CTkButton(master=self.tab(SAVE), text='Clear all custom positions', fg_color='#FF0000', hover_color='#9B0000', command=self.unset_flag)
        clear_btn.grid(row=0, column=0, pady=10, sticky='ew')

        self.save_btn = ctk.CTkButton(master=self.tab(SAVE), text='Save changes', command=self.save_changes)
        self.save_btn.grid(row=1, column=0, pady=10, sticky='ew')

        self.new_author_data: None | list[None | tuple] = None

    def name_display_button(self) -> None:
        total_authors = self.total_authors.get()
        try:
            total_authors = int(total_authors)
        except ValueError:
            total_authors = 1
        use_seconds = bool(self.use_game_time.get())
        self.write_name_display_file(total_authors, use_seconds)

    def input_pygame(self) -> None:
        show_stick = self.show_stick_display.get()
        if bool(show_stick):
            self.set_input_pos(self.custom_pos('_internal\\input', xsub=33, ysub=37))
        else:
            self.set_input_pos(self.custom_pos('_internal\\input_no_numbers', xsub=33))

    def infodisplay_pygame(self) -> None:
        infodisplay_type = self.type_of_info.get()
        if infodisplay_type == 'IV only':
            self.set_infodisplay_pos(self.custom_pos('_internal\\infodisplay_iv', xsub=33))
        elif infodisplay_type == 'EV only':
            self.set_infodisplay_pos(self.custom_pos('_internal\\infodisplay_ev', xsub=33))
        else:
            self.set_infodisplay_pos(self.custom_pos('_internal\\infodisplay_ivev', xsub=33))

    def custom_pos(self, player, xsub:int=0, ysub: int=0) -> str:
        import pygame
        import game
        player = pygame.image.load(f'{player}.png')
        player_pos = game.init(player, self.flag)
        anchor = [(player_pos[0] - xsub) / 1280, (player_pos[1] - ysub) / 720]
        anchor = str(anchor).strip('[]')
        self.flag = True
        return anchor

    def set_infodisplay_pos(self, pos: str):
        self.info_pos = pos

    def set_input_pos(self, pos: str) -> None:
        self.input_pos = pos

    def set_namedisp_pos(self, pos: str) -> None:
        self.namedisp_pos = pos
        
    def unset_flag(self) -> None:
        self.flag = False

    def write_name_display_file(self, num_of_authors: int, use_seconds: bool) -> None:
        import name_display_gui
        collab: name_display_gui.NameDisplay = name_display_gui.NameDisplay(namedisplay_number=num_of_authors, use_seconds=use_seconds)
        author_data: list[tuple] = name_display_gui.return_namedisp(collab)
        self.new_author_data: None | list[None | tuple] = []
        loop_num = 0
        for author in author_data:
            if author[4]:
                start_frame = round((author[2] * 60) + 240)
                if start_frame == 240:
                    start_frame = 0
                end_frame = round((author[3] * 60) + 240)
            else:
                start_frame = author[2]
                end_frame = author[3]
            self.new_author_data.append((author[0], start_frame, end_frame))
        self.name_display_file = open(open_txt_file(), 'w')
        with self.name_display_file as file:
            for author in self.new_author_data:
                loop_num += 1
                if loop_num == num_of_authors:
                    file.write(f'{author[0]}:{author[1]}-{author[2]}')
                else:
                    file.write(f'{author[0]}:{author[1]}-{author[2]}\n')
            file.flush()
            file.close()

    def name_display_pygame(self) -> None | str:
        if self.new_author_data is None:
            return None
        authors = ''
        for author in self.new_author_data:
            authors += f'{author[0]} \n' 
        from name_display_gui import text_to_image
        from PIL.Image import Image
        text: Image = text_to_image(authors)
        text.save('_internal\\name_display.png')
        return self.custom_pos('_internal\\name_display', xsub=-12, ysub=-8)
        
        
    def save_changes(self) -> None:
        file_path = open_file()
        config = ConfigFile(file_path)

        #Encoding options
        config.create_section('Encoding options')

        encode_style = self.encode_style.get()

        if encode_style in {'YouTube', 'Discord'}:
            config.create_variable(('encode_style', encode_style.lower()), 'Encoding options')
        else:
            config.create_variable(('encode_style', 'normal'), 'Encoding options')

        if encode_style == 'Discord':
            config.create_variable(('output_file_size', '19'), 'Encoding options')
        else:
            config.create_variable(('output_file_size', ' '), 'Encoding options')

        config.create_variable(('crf_value', '0'), 'Encoding options')

        preset = self.preset.get()

        if preset not in {"ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"}:
            preset = 'medium'
        config.create_variable(('preset', preset), 'Encoding options')

        threads = self.threads.get()

        try:
            threads = int(threads)
        except ValueError:
            threads = 8

        threads = str(threads)

        config.create_variable(('threads', threads), 'Encoding options')

        resolution = self.resolution.get()

        if resolution in {'1440p', '1080p', '720p'}:
            resolution = resolution.strip('p')
        elif resolution == '4K UHD':
            resolution = '2160'
        else:
            resolution = '1080'

        config.create_variable(('resize_resolution', resolution), 'Encoding options')

        config.create_variable(('resize_style', 'stretch'), 'Encoding options')

        scaling = self.scaling.get()
        scaling = scaling.lower()

        if scaling not in {'lanczos', 'bicubic', 'bilinear'}:
            scaling = 'bilinear'

        config.create_variable(('scaling_option', scaling), 'Encoding options')

        output_filename = self.output.get()
        try:
            if output_filename[-1] == '.':
                output_filename += 'mp4'
        except IndexError:
            output_filename = 'output.mp4'
        try:
            if output_filename[-4] + output_filename[-3] + output_filename[-2] + output_filename[-1] != '.mp4':
                output_filename += '.mp4'  
        except IndexError:
            if output_filename != '' or output_filename != '.':
                output_filename += '.mp4'

        config.create_variable(('output_filename', output_filename), 'Encoding options')

        video_fade_in = self.fadein_video.get()

        try:
            video_fade_in = float(video_fade_in)
        except ValueError:
            video_fade_in = 0

        video_fade_in = str(video_fade_in)

        config.create_variable(('video_fade_in', video_fade_in), 'Encoding options')

        video_fade_out = self.fadeout_video.get()

        try:
            video_fade_out = float(video_fade_out)
        except ValueError:
            video_fade_out = 0

        video_fade_out = str(video_fade_out)

        config.create_variable(('video_fade_out', video_fade_out), 'Encoding options')

        config.create_variable(('special_effects', 'none'), 'Encoding options')

        #Adding utils files (NOTE: Nothing in here affects the config file)
        author_utils = '_internal\\author_display_util' + resolution + '.py'
        author_utils2 = f'{EXTRADIR}\\author_display_util.py'
        shutil.copy(author_utils, author_utils2)
        shutil.copy('_internal\\input_display_util.py', f'{EXTRADIR}\\input_display_utils.py')
            
        #Audio options
        config.create_section('Audio options')

        play_music = self.play_audio.get()
        config.create_variable(('audiodump_target', 'dsp'), 'Audio options')
        config.create_variable(('audiodump_volume', str(play_music) + '.0'), 'Audio options')

        config.create_variable(('bgm_filename', ' '), 'Audio options')
        config.create_variable(('bgm_volume', '1.0'), 'Audio options')
        config.create_variable(('bgm_offset', '0'), 'Audio options')

        fade_in = self.fadein_audio.get()

        try:
            fade_in = float(fade_in)
        except ValueError:
            fade_in = 0

        fade_in = str(fade_in)

        config.create_variable(('fade_in', fade_in), 'Audio options')

        fade_out = self.fadeout_audio.get()

        try:
            fade_out = float(fade_out)
        except ValueError:
            fade_out = 0

        fade_out = str(fade_out)

        config.create_variable(('fade_out', fade_out), 'Audio options')

        #Infodisplay
        config.create_section('Infodisplay')

        infodisplay_box = str(bool(self.show_infodisplay.get()))

        config.create_variable(('font', 'MKW_Font'), 'Infodisplay')

        config.create_variable(('font_size', '48'), 'Infodisplay')

        if resolution == '2160':
            font_scaling = '4.5'
        elif resolution == '1440':
            font_scaling = '3'
        elif resolution == '720':
            font_scaling = '1.5'
        else:
            font_scaling = '2.25'

        config.create_variable(('mkw_font_scaling', font_scaling), 'Infodisplay')

        config.create_variable(('spacing', '6'), 'Infodisplay')

        config.create_variable(('fade_animation', 'False'), 'Infodisplay')

        config.create_variable(('fly_animation', 'True'), 'Infodisplay')

        config.create_variable(('fly_in_direction', 'bottom'), 'Infodisplay')

        config.create_variable(('invert_text', 'False'), 'Infodisplay')

        config.create_variable(('outline_width', '3'), 'Infodisplay')

        config.create_variable(('outline_color', '000000FF'), 'Infodisplay')

        #Speedometer
        show_speedo = bool(self.show_speedometer.get())
        speedo_type = self.speedometer_type.get()
        if not show_speedo:
            config.create_variable(('pretty_speedometer_type', 'none'), 'Infodisplay')
            config.create_variable(('show_infodisplay', infodisplay_box), 'Infodisplay')
        else:
            config.create_variable(('show_infodisplay', 'True'), 'Infodisplay')
            if speedo_type in {'XZ', 'XYZ'}:
                config.create_variable(('pretty_speedometer_type', speedo_type.lower()), 'Infodisplay')
            else:
                config.create_variable(('pretty_speedometer_type', 'iv'), 'Infodisplay')

        config.create_variable(('pretty_speedometer_color', 'F2E622FF'), 'Infodisplay')

        config.create_variable(('enable_custom_text', str(show_speedo)), 'Infodisplay')

        config.create_variable(('custom_text_anchor_1', '0.745, 0.860'), 'Infodisplay')
        config.create_variable(('custom_text_scaling_1', font_scaling), 'Infodisplay')

        speedo_text = self.speedometer_text.get()
        if speedo_text not in {'"SPEED"', '"KM/H"'}:
            new_speedo_text = ''
        elif speedo_text == '"KM/H"':
            new_speedo_text = 'k<<<m<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"/"<<<<<<<<<<<<<<<<<<<<<<<<<<<<h'
        else:
            new_speedo_text = 's<<p<<e<<<e<<d'
        
        config.create_variable(('custom_text_1', new_speedo_text), 'Infodisplay')
        config.create_variable(('custom_text_color_1', MKW_YELLOW), 'Infodisplay')

        infodisplay_type = self.type_of_info.get()
        if infodisplay_type == 'IV only':
            show_iv = True
            show_ev = False
        elif infodisplay_type == 'EV only':
            show_iv = False
            show_ev = True
        elif infodisplay_type == 'IV & EV':
            show_iv = True
            show_ev = True
        else:
            show_iv = False
            show_ev = False

        anchor = self.info_pos
        if anchor == None:
            anchor = '0, 0'
        config.create_variable(('anchor', anchor), 'Infodisplay')

        config.create_variable(('anchor_style', 'left'), 'Infodisplay')

        if infodisplay_box != 'True':
            show_iv = False
            show_ev = False

        config.create_variable(('show_iv_xyz', str(show_iv)), 'Infodisplay')
        config.create_variable(('text_iv_xyz', '. I>V>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'), 'Infodisplay')
        config.create_variable(('color_iv_xyz', MKW_YELLOW), 'Infodisplay')

        config.create_variable(('show_ev_xyz', str(show_ev)), 'Infodisplay')
        config.create_variable(('text_ev_xyz', '. EV>>>>>>>>>>>>>>>>>>>>>>'), 'Infodisplay')
        config.create_variable(('color_ev_xyz', MKW_YELLOW), 'Infodisplay')  

        #Input Display
        config.create_section('Input display')

        show_input = bool(self.show_input_display.get())
        config.create_variable(('show_input_display', str(show_input)), 'Input display')

        show_numbers = bool(self.show_stick_display.get())
        config.create_variable(('draw_stick_text', str(show_numbers)), 'Input display')

        anchor2 = self.input_pos
        if anchor2 == None:
            anchor2 = '0, 0'
        config.create_variable(('top_left', anchor2), 'Input display')

        config.create_variable(('fade_animation', 'False'), 'Input display')
        config.create_variable(('fly_animation', 'True'), 'Input display')
        config.create_variable(('fly_in_direction', 'bottom'), 'Input display')

        config.create_variable(('width', '5'), 'Input display')
        config.create_variable(('outline_width', '4'), 'Input display')

        config.create_variable(('color_shoulder_left', PURE_WHITE), 'Input display')
        config.create_variable(('color_shoulder_right', PURE_WHITE), 'Input display')
        config.create_variable(('color_dpad', PURE_WHITE), 'Input display')
        config.create_variable(('color_analog', PURE_WHITE), 'Input display')
        config.create_variable(('color_a_button', PURE_WHITE), 'Input display')
        config.create_variable(('color_stick_text', PURE_WHITE), 'Input display')

        if resolution == '2160':
            input_scaling = 2.7
        elif resolution == '1440':
            input_scaling = 1.8
        elif resolution == '720':
            input_scaling = 0.9
        else:
            input_scaling = 1.35

        config.create_variable(('scaling', str(input_scaling)), 'Input display')

        config.create_variable(('scaling_option', scaling), 'Input display')

        config.create_variable(('draw_box', 'False'), 'Input display') 
        config.create_variable(('stick_text_size', '30'), 'Input display') 
        config.create_variable(('special_effects', 'none'), 'Input display')

        #Speed display
        config.create_section('Speed display')

        show_speed_display = bool(self.show_speed_display.get())
        config.create_variable(('show_speed_display', str(show_speed_display)), 'Speed display')

        #Name display
        config.create_section('Author display')

        show_name_display = bool(self.show_name_display.get())
        config.create_variable(('show_author_display', str(show_name_display)), 'Author display')

        config.create_variable(('fade_animation', 'False'), 'Author display') 
        config.create_variable(('fly_animation', 'True'), 'Author display') 
        config.create_variable(('fly_in_direction', 'top'), 'Author display') 

        namedisplay_pos = self.namedisp_pos
        if namedisplay_pos == None:
            namedisplay_pos = '0, 0'
        config.create_variable(('top_left', namedisplay_pos), 'Author display')

        config.create_variable(('author_list_filename', 'authors.txt'), 'Author display')

        config.create_variable(('font', 'FOT-Rodin Pro EB.otf'), 'Author display')

        if resolution == '2160':
            font_size = 72
            outline = 8
        elif resolution == '1440':
            font_size = 48
            outline = 6
        elif resolution == '720':
            font_size = 24
            outline = 3
        else:
            font_size = 36
            outline = 4

        config.create_variable(('font_size', str(font_size)), 'Author display')

        config.create_variable(('active_text_color', PURE_WHITE), 'Author display')
        config.create_variable(('inactive_text_color', 'FFFFFF55'), 'Author display')

        config.create_variable(('outline_width', str(outline)), 'Author display')

        config.create_variable(('active_outline_color', '000000FF'), 'Author display')
        config.create_variable(('inactive_outline_color', '00000055'), 'Author display')

        #Extra display
        config.create_section('Extra display')

        show_extra_display = bool(self.show_extra_display.get())
        config.create_variable(('show_extra_display', str(show_extra_display)), 'Extra display')

        config.write_to_file()
        os.startfile(ROOTDIR)
        sys.exit()     

def open_file() -> str:
    return 'FrameDumps\\config.ini'

def open_txt_file() -> str:
    return 'FrameDumps\\authors.txt'

if __name__ == '__main__':
    window = Window()
    window.mainloop()
