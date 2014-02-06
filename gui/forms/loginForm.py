import npyscreen

class LoginForm(npyscreen.ActionPopupOk):
    def create(self):
        self.failcount = 0
        #self.logo = self.add(npyscreen.MultiLineEdit,
        self.head = self.add(npyscreen.TitleFixedText, name = "Authentication required", editable=False)
        self.user = self.add(npyscreen.TitleText, name="Username:")
        self.passwd = self.add(npyscreen.TitlePassword, name = "Password:")

    def on_ok(self):
        if self.user.value == "jack" and self.passwd.value == "secret":
            self.parentApp.setNextForm("MAIN")
            self.user.value = ""
            self.passwd.value = ""
            self.editing = False
            self.parentApp.switchFormNow()
        else:
            self.failcount = self.failcount + 1
            self.head.value = "FAILURES:" + str(self.failcount)

    def on_cancel(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()
