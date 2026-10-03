import customtkinter as ctk
from PIL import ImageFont, ImageDraw, Image

def init() -> ctk.CTk:
    root = ctk.CTk()
    root.withdraw()
    return root

def text_to_image(
    text: str,
    font_size: int=24,
    color: tuple[int]=(255, 255, 255, 255),
    stroke_width: int=3,
    stroke_color: tuple[int]=(0, 0, 0, 255),
) -> Image.Image:

    font_filepath = '_internal\\namedisplay_font.otf'
    
    font = ImageFont.truetype(font_filepath, size=font_size)

    dummy_img = Image.new("RGBA", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    bbox = dummy_draw.multiline_textbbox(
        (0, 0), text, font=font, stroke_width=stroke_width
    )
    
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)


    draw_point = (-bbox[0], -bbox[1])

    draw.multiline_text(
        draw_point,
        text,
        font=font,
        fill=color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )

    return img

class NameDisplay(ctk.CTkToplevel):
    def __init__(self, namedisplay_number: str | int, use_seconds: bool, author_num: int=1, master: ctk.CTk=init()):
        super().__init__(master)
        self.title('Name Display Editor')
        self.geometry('500x500')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.grab_set()

        self.button_pressed = False
        self.use_seconds = use_seconds
        self.withdrew = False
        self.author_num = author_num

        try:
            namedisplay_number = int(namedisplay_number)
        except ValueError:
            namedisplay_number = 2

        try:
            author_num = int(author_num)
        except ValueError:
            author_num = 1

        self.namedisplay_number = int(namedisplay_number)

        self.author_name_entry = ctk.CTkEntry(master=self, placeholder_text=f'Name of author #{str(author_num)}')
        self.author_name_entry.grid(row=0, column=0, pady=10)

        if use_seconds:
            text = 'second'
        else:
            text = 'frame'
        self.startframe = ctk.CTkEntry(master=self, placeholder_text=f'Start {text}')
        self.startframe.grid(row=1, column=0, pady=10)

        self.endframe = ctk.CTkEntry(master=self, placeholder_text=f'End {text}')
        self.endframe.grid(row=2, column=0, pady=10)

        self.btn = ctk.CTkButton(master=self, text='Continue', command=lambda: self.button_command())
        self.btn.grid(row=3, column=0, pady=10)

    def button_command(self) -> tuple:
        if not self.withdrew:
            self.author_name = self.author_name_entry.get()
            self.start = self.startframe.get()
            self.end = self.endframe.get()
            self.withdraw()
        self.button_pressed = True
        self.withdrew = True
        if not self.use_seconds:
            try:
                self.start = int(self.start)
            except ValueError:
                self.start = 0
            try:
                self.end = int(self.end)
            except ValueError:
                self.end = 10000
        else:
            try:
                self.start = float(self.start)
            except ValueError:
                self.start = 0
            try:
                self.end = float(self.end)
            except ValueError:
                self.end = 10000           
        
        self.destroy()
        return (self.author_name, self.author_num, self.start, self.end, self.use_seconds, self.namedisplay_number)


def return_namedisp(namedisplay: NameDisplay, list_of_authors: list[tuple | None]=None) -> list[tuple]:
    if list_of_authors is None:
        list_of_authors = []

    namedisplay.master.wait_window(namedisplay)

    list_of_authors.append(namedisplay.button_command())

    if len(list_of_authors) == namedisplay.namedisplay_number:
        namedisplay.master.destroy()
        return list_of_authors
    else:
        new_namedisplay = NameDisplay(namedisplay.namedisplay_number, namedisplay.use_seconds, namedisplay.author_num + 1, namedisplay.master)
        return return_namedisp(namedisplay=new_namedisplay, list_of_authors=list_of_authors)