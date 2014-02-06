#!/usr/bin/env python
# encoding: utf-8

import npyscreen
class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        t  = F.add(npyscreen.TitleText, name = "Text:",)
        fn = F.add(npyscreen.TitleFilename, name = "Filename:")
        fn2 = F.add(npyscreen.TitleFilenameCombo, name="Filename2:")
        dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
        s  = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
        ml = F.add(npyscreen.BoxTitle,
               value = """ ____                       _   _   _                 _                      \n|  _ \  ___   __ _ _ __    / \ | |_| |_ ___ _ __   __| | __ _ _ __   ___ ___ \n| | | |/ _ \ / _` | '_ \  / _ \| __| __/ _ \ '_ \ / _` |/ _` | '_ \ / __/ _ \\\n| |_| | (_) | (_| | | | |/ ___ \ |_| ||  __/ | | | (_| | (_| | | | | (_|  __/\n|____/ \___/ \__,_|_| |_/_/   \_\__|\__\___|_| |_|\__,_|\__,_|_| |_|\___\___|""", max_height=5, rely=9)
        ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several",
                values = ["Option1","Option2","Option3"], scroll_exit=True)

        # This lets the user interact with the Form.
        F.edit()

        print ms.get_selected_objects()

if __name__ == "__main__":
    App = TestApp()
    App.run()
