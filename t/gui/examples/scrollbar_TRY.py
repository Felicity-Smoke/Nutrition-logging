from tkinter import Entry, Label, Button, Frame, Tk, Canvas, ttk

class Window(Frame):
    def __init__(self, parent):
        super(Window, self).__init__(parent)
        self.parent = parent
        self.grid(row=0,column=0)      

        # Entry, Start
        self.entry = Entry(self)
        self.entry.grid(column=0, row=0, padx=1,pady=0)
        self.entry.bind('<Return>',self.started)
        self.btn_start = Button(self, text='start',command=self.started)
        self.btn_start.grid(column=1, row=0, padx=2, pady=2)

        # Result
        self.results=Frame(self, background='blue')
        self.canvas=Canvas(self.results, background='green')
        self.labels_frame=Frame(self.canvas, background='pink')
        self.scrollbar = ttk.Scrollbar(self.results, orient='vertical', command=self.canvas.yview)
        self.heading=Label(self.labels_frame, text='Suchergebnisse:', anchor='w',width=50)     

        self.results.grid(row=1,column=0,sticky='w',padx=2,pady=2, columnspan=2)
        self.canvas.grid(row=0,column=0, padx=2,pady=2)#todo delete padding
        #self.labels_frame.grid(row=0,column=0, padx=2,pady=2)#benötigt obwohl canvas.create_window?
        self.heading.grid(column=0,row=0,columnspan=3,sticky='wesn', padx=2, pady=2)
        self.canvas.create_window(0, 0, anchor='nw', window=self.labels_frame)#,height=250,width=300)
        
    def started(self, events=None): 
        self.found_foods=[]
        for i in range(int(self.entry.get())):
            self.found_foods.append(i)
        self.create_labels()
                
    def create_labels(self):
        labels=[]
        for found_food in self.found_foods:
            name_label = Label(self.labels_frame, text=found_food, anchor='w') 
            category_label = Label(self.labels_frame, text='--missing yet--', anchor='w')
            labels.append([name_label,category_label])
        self.update_view(labels)

    def update_view(self,labels):
        self.del_old_labels()
        for row,labelrow in enumerate(labels):
            for col,element in enumerate(labelrow):
                element.grid(row=row+1, column=col, padx=1,pady=1, sticky='wsen')

        if len(self.found_foods)>10: #10 nur als Bsp
            self.canvas.update_idletasks() #no idea what this does
            self.canvas.config(yscrollcommand=self.scrollbar.set)
            self.canvas.config(height=250,width=300)
            self.scrollbar.grid(row=0,column=1, sticky='ns',padx=2,pady=2)
        else:
            self.scrollbar.grid_forget()

    def del_old_labels(self):
        for label in self.labels_frame.grid_slaves():
            if int(label.grid_info()["row"]) > 0:
                label.grid_forget()            
        
if __name__ == '__main__':        
    root = Tk()
    app = Window(root)
    root.mainloop()
