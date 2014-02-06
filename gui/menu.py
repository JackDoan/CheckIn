#!/usr/bin/env python

import dbal, npyscreen, curses, forms.loginForm, forms.mainForm 
npyscreen.NPSAppManaged.STARTING_FORM = "MAIN"
npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
class MyTestApp(npyscreen.NPSAppManaged):
   def onStart(self):
        self.registerForm("LOGIN", forms.loginForm.LoginForm())
        self.registerForm("MAIN", forms.mainForm.MainForm())
      #  self.registerForm("LOOKUP", LookupForm())
def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass  
