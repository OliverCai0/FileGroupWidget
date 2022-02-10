from __future__ import print_function
import tkinter as tk
from tkinter import ttk

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

class FileGroupSummaryFrame(tk.Frame):

    def __init__(self, parent, text='', header='Files', *args, **options):   
        tk.Frame.__init__(self, parent, *args, **options)
        self.groups = []

    def add_frame(self,name):
        #Adding Toggled Frame
        new_frame = ToggledFrame(self,text=name)
        new_frame.pack()

        list_box = tk.Listbox(new_frame.sub_frame, selectmode='multiple')
        scroll = tk.Scrollbar(new_frame.sub_frame)
        scroll.pack(side='right', fill='y')
        list_box.pack(fill='x')
        list_box.config(yscrollcommand= scroll.set)
        scroll.config(command=list_box.yview)

        groups.append([new_frame,list_box])

    def insert_file(self, frame_index, filename):
        self.groups[frame_index][1].insert(tk.END,filename)




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

        label = ttk.Label(self, text=filename)
        label.grid(row = self.rows, column = 0)

        for col in range(self.columns):
            indicator = ttk.Checkbutton(self, variable=None)
            indicator.grid(row = self.rows, column = col + 1)
            indicator.focus_set()
            indicator.bind("<Button-1>", self.status_update)

    def delete_row(self, row_index):
        self.destroyed_rows.append(row_index)
        row = self.grid_slaves(row_index + 1)
        for i in range(len(row)):
            row[i].destroy()

    def swap_to_label(self,event):
        rowcoord = event.widget.grid_info()['row']
        colcoord = event.widget.grid_info()['column']
        new_label = ttk.Label(self,text = event.widget.get())
        self.grid_slaves(rowcoord, colcoord)[0].destroy()
        new_label.grid(row=rowcoord,column=colcoord)
        new_label.bind("<Double-Button-1>",self.swap_to_entry)

    def swap_to_entry(self,event):
        rowcoord = event.widget.grid_info()['row']
        colcoord = event.widget.grid_info()['column']
        new_group_entry = ttk.Entry(self)
        #print(f"swap_to_entry")
        self.grid_slaves(rowcoord, colcoord)[0].destroy()
        new_group_entry.grid(row=rowcoord,column=colcoord)
        new_group_entry.bind("<Return>",self.swap_to_label)

    def add_new_col(self,event):
        self.columns += 1
        rowcoord = event.widget.grid_info()['row']
        colcoord = event.widget.grid_info()['column']

        #Destroy Previous Header for Group Entry
        self.grid_slaves(rowcoord, colcoord)[0].destroy()

        #Reaplce with Header For Group Entry
        new_group_entry = ttk.Entry(self)
        new_group_entry.grid(row=rowcoord,column=self.columns)
        new_group_entry.bind("<Return>",self.swap_to_label)

        #Add New Group Label
        new_add_group_label = ttk.Label(self,text='+ New Group')
        new_add_group_label.grid(row=rowcoord,column=colcoord + 1)
        new_add_group_label.focus_set()
        new_add_group_label.bind("<Double-Button-1>",self.add_new_col)

        #Add Checkboxes
        for row in range(self.rows):
            if row not in self.destroyed_rows:
                indicator = ttk.Checkbutton(self, variable=None)
                indicator.grid(row = row + 1, column = self.columns)
                indicator.focus_set()
                indicator.bind("<Button-1>",self.status_update)


if __name__ == "__main__":
    root = tk.Tk()
    funct = lambda e: print("Click!")
    t = FileMatrixFrame(root, status_update = funct)
    for i in range(10):
        t.add_new_row(str(f'Row {i}'))
    for i in [1,5,7]:
        t.delete_row(i)
    t.add_new_row(str("lol"))
    new_file_button = ttk.Button(root,text="Add File", command= lambda: t.add_new_row('new_row'))
    new_file_button.pack()

    delete_row_entry = ttk.Entry(root)
    delete_row_entry.pack()
    delete_row_entry.focus_set()
    delete_row_entry.bind("<Return>", lambda e: t.delete_row(int(e.widget.get())))
    t.pack()
    root.mainloop()