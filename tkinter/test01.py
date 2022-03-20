from sys import version_info
if version_info.major == 2:
    from Tkinter import *
    from tkinter.ttk import *
elif version_info.major == 3:
    from tkinter import *
    from tkinter.ttk import *

app = Tk()
app.style = Style()
#print(app.style.theme_names())
app.style.theme_use('clam')

Radiobutton(app, text="Radiobuton").grid(row=1, column=1, padx=5, pady=10)
Checkbutton(app, text="Checkbuton").grid(row=1, column=2, padx=5)
Button(app, text="Quitter", command=app.destroy).grid(row=1, column=3, padx=5)

app.mainloop()
