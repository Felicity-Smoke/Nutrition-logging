from tkinter import Button, Frame, LEFT as compound_left

class MainButton(Button):
    def __init__(self,master=None, cnf={}, **kw):
        Button.__init__(self,master, cnf, **kw)
        self.save_text = self['text']
        self.active_color = 'whitesmoke'
        self.passive_color = 'lightgrey'
        self.active_width = 60

        self.background=self.passive_color
        self.activebackground=self.active_color

        self['compound'] = compound_left
        self['anchor'] = 'w'
        self['background'] = self.passive_color
        self['activebackground'] = self.active_color
        self['height'] = 50
        self['width'] = self.active_width
        self['padx'] = 15 #Todo.. funktioniert nur in 'active'
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.hide_text()

    def on_enter(self, e):
        self.config(bg=self.active_color)

    def on_leave(self, e):
        self.config(bg=self.passive_color)

    def show_text(self):
        self['text'] = self.save_text
        self['width'] = 200

    def hide_text(self):
        self['text']=''
        self['width'] = self.active_width

    def not_chosen(self):
        self['state'] = NORMAL

    #@classmethod
    def chosen(self):
        self['state'] = ACTIVE
