
# config.ini tool

A tool to help set up a config.ini file to use when recording Mario Kart Wii with [Dolphin PyCore](https://github.com/Blounard/dolphin-pycore)


## The following can be customized

- Video Settings
- Audio Settings
- IV/EV Display (Infodisplay)
- Speedometer (AKA pretty speedometer)
- Input Display
- Name Display (to a lesser extent)


## How to use

To use, simply download the latest release. The tool is fairly intuitive aside for a few things: When customizing the position of any OSD element, use WASD to control the element, and close the window when adjusted. When editing the name display, make sure to click the "Edit name display" button before customizing the position. If you placed an element in the wrong spot, you can go to the "Save Config" tab and click "Clear all custom positions" to reset all the custom positions you set. Finally, when your done. Click the "Save changes" button in the "Save Config" tab. This will open a folder, where you can simply drag and drop everything in your "FrameDumps" folder, which can be found in Dolphin at the directory "User\Load\Scripts\FrameDumps".
    
## External libraries used

- [CustomTkinter](https://pypi.org/project/customtkinter/) ([Documentation](https://customtkinter.tomschimansky.com/documentation/))
- [Pygame - Community Edition](https://pypi.org/project/pygame-ce/) ([Documentation](https://pyga.me/docs/index.html))
- [Pillow](https://pypi.org/project/pillow/) ([Documentation](https://pillow.readthedocs.io/en/stable/))

