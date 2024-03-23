from tkinter import *
class MiBoton():
    def __init__(self, parent = None, **kwargs):
        self.root = parent
        self.boton = Button(self.root, **kwargs, bg="#F0C266", 
                            activebackground="#BD761A")

    def grid(self, **kwargs):
        self.boton.grid(**kwargs, sticky="w", padx=5, pady=2)

class MiLabel():
    def __init__(self, parent = None, **kwargs):
        self.root = parent
        self.boton = Label(self.root, **kwargs, bg="#F9FFDB")

    def grid(self, **kwargs):
        self.boton.grid(**kwargs, column=1, padx=5, pady=5, sticky="w")

if __name__ == "__main__":
    root = Tk()
    boton = MiBoton(root, text="Alta")
    boton.grid(column=0, row=2)
    root.mainloop()