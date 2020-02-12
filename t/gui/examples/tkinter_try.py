from tkinter import *
from tkinter import font

class GUI(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master, height = 400, width = 600)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.button_left = Button(self, text = '<', relief='flat')
        self.mainframe = Frame(self, borderwidth = 2, relief = 'raised')
        self.button_right = Button(self, text = '>',relief='flat')

        self.button_left.grid(column = 0, row = 0)
        self.mainframe.grid(column = 1, row = 0)
        self.button_right.grid(column = 2, row = 0)

        
        self.label_viewname = Label(self.mainframe, text = 'Übersicht', font = font.Font(weight = 'bold'))
        self.temp_grafikframe = Frame(self.mainframe, borderwidth = 2, relief = 'sunken', height = 200, width = 200)
        self.B1 = Button(self.mainframe, text = 'Button 1', command = self.button_pressed)
        self.quitButton = Button(self.mainframe, text = 'Schließen', command = self.quit())

        self.label_viewname.grid(column = 0, row = 0)
        self.temp_grafikframe.grid(column = 1, row = 1)
        self.B1.grid(column = 0, row = 1)
        self.quitButton.grid(column = 0, row = 2)

        # MENU
        self.menubar = Menu(self)
        self.winfo_toplevel()['menu'] = self.menubar

        self.filemenu = Menu(self.menubar, tearoff = 0)
        self.filemenu.add_command(label='New', command = self.NewFile)
        self.filemenu.add_command(label = 'Open...', command = self.OpenFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command = self.quit)
        self.menubar.add_cascade(label='Datei', menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Hilfe', menu = self.helpmenu)
        self.helpmenu.add_command(label='Über...', command = self.About)

        self.viewmenu = Menu(self.menubar, tearoff = 0)
        self.viewmenu.add_command(label = 'Übersicht', command = self.select_view_overview)
        self.viewmenu.add_command(label = 'Eingabe', command = self.select_view_input)
        self.viewmenu.add_command(label = 'Analyse', command = self.select_view_output)
        self.menubar.add_cascade(label = 'Ansicht', menu = self.viewmenu)

        self.extrasmenu = Menu(self.menubar, tearoff = 0)
        self.extrasmenu.add_command(label = 'Einstellungen', command = self.properties)
        self.menubar.add_cascade(label = 'Optionen', menu = self.extrasmenu)

    def button_pressed(self):
        print('Button pressed')

    def select_view_overview(self):
        print('Ansicht "Übersicht" aktiviert')

    def select_view_input(self):
        print('Ansicht "Eingabe" aktiviert')
        
    def select_view_output(self):
        print('Ansicht "Analyse" aktiviert')
        
    def NewFile(self):
        print("New File!")
    def OpenFile(self):
        name = askopenfilename()
        print(name)
    def About(self):
        print("This is a simple example of a menu")
    def properties(self):
        print('Eisntellungen wurden gedrückt')
        

        


app = GUI()
app.master.title('Titel')
app.mainloop()


