import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from typing import List
from pathlib import Path

from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfWriter

app = TkinterDnD.Tk()
fileList: List[str] = []

show_full_path = False


def insert_item(file, index=tk.END):
    """
    @param file: full path of file
    """
    if show_full_path == True:
        listBox.insert(index, file)
    else:
        listBox.insert(index, Path(file).name)


def show_or_hide():
    global show_full_path
    if show_full_path:
        """show -> hide"""
        show_full_path = False
        showOrHide_btn["text"] = "show"
        listBox.delete(0, tk.END)
        for item in fileList:
            insert_item(item)
    else:
        """hide -> show"""
        show_full_path = True
        showOrHide_btn["text"] = "hide"
        listBox.delete(0, tk.END)
        for item in fileList:
            insert_item(item)


def add_file():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file in files:
        fileList.append(file)
        insert_item(file)


def drag_file(event):
    for file in event.data.split(' '):
        if Path(file).suffix.lower() == ".pdf":
            fileList.append(file)
            insert_item(file)


def change_file_order(event: tk.Event):
    """
    drag and drop to change file order
    """
    old_index, *_ = listBox.curselection()
    new_index = listBox.nearest(event.y)
    
    file = fileList.pop(old_index)
    fileList.insert(new_index, file)
    
    listBox.delete(old_index)
    insert_item(file, new_index)


def remove_item(event: tk.Event):
    """
    right click to remove item
    """
    # 從 y 取得 item
    y = event.y
    index = listBox.nearest(y)
    if index >= 0:
        fileList.pop(index)
        listBox.delete(index)


def merge_file():
    merger = PdfWriter()
    for file in fileList:
        merger.append(file)
    merger.write("merge.pdf")
    merger.close()
    messagebox.showinfo("Merge PDF", "Merge PDF successfully!")


tk.Button(text="Add", command=add_file).pack(anchor='nw', padx=7, pady=5)
listBox = tk.Listbox(selectmode='single')
listBox.drop_target_register(DND_FILES)
listBox.dnd_bind('<<Drop>>', drag_file)
listBox.bind("<ButtonRelease-1>", change_file_order)
listBox.bind("<Button-3>", remove_item)
listBox.pack(expand=True, fill='both', padx=7)

f = tk.Frame()
showOrHide_btn = tk.Button(f, text="show", command=show_or_hide)
showOrHide_btn.pack(side='left')
tk.Button(f, text="Merge", command=merge_file).pack(side='right')
f.pack(fill='x', expand=False, padx=7, pady=10)
        
app.geometry("400x300")

app.mainloop()