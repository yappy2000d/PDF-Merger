import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
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
        show_full_path = False
        showOrHide_btn["image"] = off
        listBox.delete(0, tk.END)
        for item in fileList:
            insert_item(item)
    else:
        show_full_path = True
        showOrHide_btn["image"] = on
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
    if not listBox.curselection():
        return
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
    y = event.y
    index = listBox.nearest(y)
    if index >= 0:
        fileList.pop(index)
        listBox.delete(index)


def merge_file():
    if len(fileList) <= 1:
        messagebox.showerror("Merge PDF", "Please add more than one PDF file!")
        return
    merger = PdfWriter()
    for file in fileList:
        merger.append(file)
    merger.write("merge.pdf")
    merger.close()
    messagebox.showinfo("Merge PDF", "Merge PDF successfully!")

on = tk.PhotoImage(data=b'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').subsample(2, 2)
off = tk.PhotoImage(data=b'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').subsample(2, 2)

tk.Button(text="+", font=font.Font(size=14), width=3, command=add_file).pack(anchor='nw', padx=7, pady=5)
listBox = tk.Listbox(selectmode='single')
listBox.drop_target_register(DND_FILES)
listBox.dnd_bind('<<Drop>>', drag_file)
listBox.bind("<ButtonRelease-1>", change_file_order)
listBox.bind("<Button-3>", remove_item)
listBox.pack(expand=True, fill='both', padx=7)

f = tk.Frame()
showOrHide_btn = tk.Button(f, image=off, command=show_or_hide)
showOrHide_btn.pack(side='left')
tk.Button(f, text="Merge", command=merge_file, height=2, width=20).pack(side='right')
f.pack(fill='x', expand=False, padx=7, pady=10)
        
app.geometry("400x300")
app.title("Merge PDF")

app.mainloop()
