from __future__ import print_function
import tkinter as tk
from tkinter import ttk


class FileMatrixFrame(tk.Frame):

    def __init__(self, parent, status_update, text='', header='Files', *args, **options):
        
        tk.Frame.__init__(self, parent, *args, **options)
        self.destroyed_rows = []
        self.status_update = status_update
        self.rows = 0
        self.columns = 0

        #intialize header
        self.header = ttk.Label(self,text=header)
        self.header.grid(row=0,column=0)

        self.add_group = ttk.Label(self, text= '+ New Group')
        self.add_group.grid(row = 0, column = 1)
        self.add_group.bind("<Double-Button-1>",self.add_new_col)


    def add_new_row(self,filename):
        self.rows += 1

        label = ttk.Label(self, filename)
        label.grid(row = rows, column = 0)

        for col in range(columns):
            indicator = tkk.Checkbutton(self, variable=None)
            indicator.grid(row = self.rows, column = col + 1)
            indicator.focus_set()
            indicator.bind("<Button-1>", self.status_update)

    def delete_row(self, row_index):
        self.destroyed_rows.append(row_index)
        row = self.grid_slaves(row_index)
        for i in range(len(row)):
            target[i].destroy()

    def add_new_col(self,event):
        self.columns += 1
        rowcoord = event.widget.grid_info()['row']
        colcoord = event.widget.grid_info()['column']

        #Add Header For Group
        new_group_entry = ttk.Entry(self)
        new_group_entry.grid(row=rowcoord,column=colcoord)
        new_group_entry.bind("<Return>",self.swap_to_label)

        #Add Checkboxes
        for row in range(rows):
            if row not in destroyed_rows:
                indicator = ttk.Checkbutton(self, variable=None)
                indicator.grid(row = row + 1, column = self.columns)
                indicator.focus_set()
                indicator.bind("<Button-1>",self.status_update())


if __name__ == "__main__":
    root = tk.Tk()
    funct = lambda : print("Click!")
    t = FileMatrixFrame(root, status_update = funct)
    t.pack()
    root.mainloop()