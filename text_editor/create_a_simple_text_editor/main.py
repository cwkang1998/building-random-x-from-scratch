from tkinter import Button, Menu, Tk, Text, filedialog, Menubutton, RAISED
from typing_extensions import IntVar


def save_as():
    global text
    t = text.get("1.0", "end-1c")
    save_location = filedialog.asksaveasfilename()
    file1 = open(save_location, "w+")
    file1.write(t)
    file1.close()


def font_helvetica():
    global text
    text.config(font="Helvetica")


def font_courier():
    global text
    text.config(font="Courier")


root = Tk()
root.title("My Text Editor")
root.resizable(False, False)

# The editor
text = Text(root)
text.grid()

# save button
button = Button(root, text="Save", command=save_as)
button.grid()

# hardcoded font button

fontSelection = Menubutton(root, text="Font", relief=RAISED)
fontMenu = Menu(fontSelection, tearoff=0)
helvetica = IntVar('Helvetica')
courier = IntVar('Courier')
fontMenu.add_checkbutton(label="Helvetica", variable=helvetica, command=font_helvetica)
fontMenu.add_checkbutton(label="Courier", variable=courier, command=font_courier)

fontSelection["menu"] = fontMenu
fontSelection.grid()


root.mainloop()
