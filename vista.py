from tkinter import StringVar
from tkinter import Entry
from tkinter import ttk
from tkinter import messagebox

from modelo import Abcm

from modelo import InteraccionBD

from widgets import MiBoton
from widgets import MiLabel

objeto = Abcm()
objetoBase = InteraccionBD()

class Vista():
    def __init__(self,window):
        self.root = window
        self.root.title("PS COSMÉTICA")
        self.root.resizable(0, 0)
        self.root.config(bg="#F0C266")
        # MENU----------------------------------------------------------------
        # BASE DE DATOS Y TABLA----------------------------------------------------------------
        """self.boton1 = MiBoton(
            self.root, 
            text="Alta",
            command=lambda: self.alta())
        self.boton1.grid(row=2)"""

        self.boton_db = MiBoton(
            self.root,
            text="Conectarse a la Base de Datos",
            command=lambda:self.conectar_base(),
        )
        self.boton_db.grid(column=1, row=1)
        self.boton_table = MiBoton(
            self.root,
            text="Crear Tabla Productos",
            command=lambda:self.crear_tabla(),
        )
        self.boton_table.grid(column=2, row=1)

        # INGRESO DE DATOS------------------------------------------------------------------------
        self.labe1_p = MiLabel(self.root, text="Producto:")
        self.labe1_p.grid(row=2)

        self.combo = ttk.Combobox(
            state="readonly",
            values=[
                "LIDHERMA",
                "EXEL",
                "IDRAET",
                "AP",
                "COLONY",
                "ZINE",
            ],
        )
        self.combo.grid(column=2, row=3, padx=5, pady=5, sticky="w")

    # ------------------------------------------------------------------------

        self.labe1_l = MiLabel(self.root, text="Laboratorio:")
        self.labe1_l.grid(row=3)

        self.labe1_l = MiLabel(self.root, text="Cantidad:")
        self.labe1_l.grid(row=4)

        self.producto = StringVar()
        self.laboratorio = StringVar()
        self.cantidad = StringVar()

        self.producto_e = Entry(self.root, textvariable=self.producto)
        self.producto_e.grid(column=2, row=2)

        self.cantidad_e = Entry(self.root, textvariable=self.cantidad)
        self.cantidad_e.grid(column=2, row=4)

        # TREEVIEW------------------------------------------------------------------------
        self.tv = ttk.Treeview(self.root, columns=("col1", "col2", "col3", "col4"))
        self.tv.column("#0", anchor="w", width=80, minwidth=80)
        self.tv.heading("#0", text="id")
        self.tv.column("col1", anchor="w", width=80, minwidth=80)
        self.tv.heading("col1", text="Producto")
        self.tv.column("col2", anchor="w", width=80, minwidth=80)
        self.tv.heading("col2", text="Laboratorio")
        self.tv.column("col3", anchor="w", width=80, minwidth=80)
        self.tv.heading("col3", text="Cantidad")
        self.tv.column("col4", anchor="w", width=80, minwidth=80)
        self.tv.heading("col4", text="Fecha")
        self.tv.grid(column=0, row=6, columnspan=5)

        #Se activa la funcion seleccion cada vez que se selecciona en el tv 
        self.tv.bind("<<TreeviewSelect>>", self.seleccion) 
        
        self.boton1 = MiBoton(
            self.root, 
            text="Alta",
            command=lambda: self.alta())
        self.boton1.grid(column=0,row=2)

        self.boton2 = MiBoton(
            self.root,
            text="Baja",
            command=lambda: self.baja(),
        )
        self.boton2.grid(column=0,row=3)

        self.boton3 = MiBoton(
            self.root,
            text="Modificación",
            command=lambda: self.modificacion(),
        )
        self.boton3.grid(column=0,row=4,)
        #--------------------------------------------------------------
        self.combo_bases = ttk.Combobox(
            state="readonly",
            values=[
                "SQLite3 (default)",
                "MySQL",
                "Postgres"
            ],
        )
        self.combo_bases.bind("<<ComboboxSelected>>", self.cambiar_base)
        self.combo_bases.grid(column=0, row=1, padx=5, pady=5, sticky="w")

    def cambiar_base(self, event=None):
        seleccion = self.combo_bases.get()
        objetoBase.seleccionar_base(seleccion)
        #messagebox.showinfo("Base de datos", retorno)
        
    def seleccion(self,event):
        valor = self.tv.selection()
        item = self.tv.item(valor)
        id = item["text"]
        if id:
            objeto.cargar_entrys(self.producto,self.combo,self.cantidad,id)


    # ABCM------------------------------------------------------------------------
    def alta(self):
        retorno = objeto.alta(self.tv, self.producto, self.combo, self.cantidad)
        messagebox.showinfo("Alta", retorno)

    def baja(self):
        valor = self.tv.selection()  
        if valor: 
            resultado = messagebox.askquestion("Baja", "¿Estas seguro de querer eliminar este producto?")
            if resultado == "yes":
                retorno = objeto.baja(self.tv, valor)
                print(retorno)
                messagebox.showinfo("Baja", retorno)
            else:
                messagebox.showinfo("Acción cancelada", "No se eliminó el producto")
        else:
            messagebox.showinfo("Acción cancelada", "Debe seleccionar un producto a eliminar")
        
    def modificacion(self):
        valor = self.tv.selection()
        if valor:
            resultado = messagebox.askquestion("Modificación", "¿Estas seguro de querer modificar este producto?")
            if resultado == "yes":
                retorno = objeto.modificacion(self.tv, self.producto, self.combo, self.cantidad,valor)
                messagebox.showinfo("Modificación", retorno)
            else:
                messagebox.showinfo("Acción cancelada", "No se modificó el producto")
        else:
            messagebox.showinfo("Acción cancelada", "Debe seleccionar un producto a modificar")
    # ------------------------------------------------------------------------
    def conectar_base(self):
        retorno = objetoBase.conectar_base(self.tv) 
        messagebox.showinfo("Base de Datos", retorno)
    def crear_tabla(self):
        retorno = objetoBase.crear_tabla()
        messagebox.showinfo("Tabla 'Productos'", retorno)