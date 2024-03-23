import re
import datetime
from peewee import * 

db = SqliteDatabase("base_productos_sqlite.db")

class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    id = AutoField()
    nombre = CharField()
    cantidad = IntegerField()
    laboratorio = CharField()
    fecha = CharField()

class InteraccionBD():
    def __init__(self):
        self.actualizarTv = Abcm()

    def conectar_base(self,tv):
        try:
            self.actualizarTv.actualizar_treeview(tv)
            return "Se conectó a la base"
        except:
            return "Debe crear la tabla 'Productos'"

    def crear_tabla(self):
        if not(Producto.table_exists()):
            db.create_tables([Producto])
            return "Se creó la tabla 'Productos'"
        else:
            return "La tabla 'Productos' ya fue creada"

    def seleccionar_base(self, seleccion):
        """
        Con esta función deberías de poder crear las bases de datos de MySQL y Postgres y a partir de un servidor de estos manipularlas.
        """
        global db
        if seleccion =="SQLite3 (default)":
            db = SqliteDatabase("base_productos_sqlite.db")
            print(db)
            #return "Se selecciono la base SQLite3"
        elif seleccion == "MySQL":
            db = MySQLDatabase("base_productos_mysql.db")
            print(db)
            #return "Se selecciono la base MySQL"
        elif seleccion == "Postgres":
            db = PostgresqlDatabase("base_productos_postgres.db")
            print(db)
            #return "Se selecciono la base Postgres"
# ABCM------------------------------------------------------------------------
class Abcm():
    def __init__(self):
        pass
    def alta(self, tree, p1, l1, c1):
        self.producto = p1.get()
        self.cantidad = c1.get()
        self.laboratorio = l1.get()
        # regex para el campo cadena
        patron_producto = "^[A-Za-záéíóú]+$"
        # regex para la cantidad
        patron_cantidad = "^[1-9]\d*$"
        print(self.producto)
        if re.match(patron_producto, self.producto):
            if re.match(patron_cantidad,self.cantidad):
                fecha = str(datetime.datetime.today().strftime("%d/%m/%y"))
                alta = Producto()
                alta.nombre = p1.get()
                alta.cantidad = c1.get()
                alta.laboratorio = l1.get()
                alta.fecha = fecha
                alta.save()
                try:
                    self.actualizar_treeview(tree)
                    self.limpiar_datos(p1, l1, c1)
                    return "Se ha agregado: \nProducto: "+ self.producto +"\nLaboratorio:"+ self.laboratorio +"\nCantidad:" + self.cantidad
                except:
                    return "La tabla 'Productos' no fue creada"
            else:
                self.limpiar_cantidad(c1)
                return "Error en el campo 'Cantidad'"   
        else:
            self.limpiar_producto(p1)
            return "Error en el campo 'Producto'" 

    def baja(self, tree, valor):
        self.item = tree.item(valor)
        self.id_delete = self.item["text"]
        self.producto = self.item['values'][0]
        self.laboratorio = self.item['values'][1]
        self.cantidad = str(self.item['values'][2])
        self.baja = Producto.get(Producto.id == self.id_delete)
        self.baja.delete_instance()
        tree.delete(valor)
        try:
            self.actualizar_treeview(tree)
            return "Se ha modificado: \nProducto: "+ str(self.producto) +"\nLaboratorio:"+ str(self.laboratorio) +"\nCantidad:" + str(self.cantidad)
        except:
            return "La tabla 'Productos' no fue creada"

    def modificacion(self,tree, p1, l1, c1, valor):
        self.producto = p1.get()
        self.cantidad = c1.get()
        self.laboratorio = l1.get()
        # regex para el campo cadena
        patron_producto = "^[A-Za-záéíóú]+$"
        # regex para la cantidad
        patron_cantidad = "^[1-9]\d*$"
        if re.match(patron_producto, self.producto):
            if re.match(patron_cantidad,self.cantidad):
                item = tree.item(valor)
                id_update = item["text"]
                fecha2 = str(datetime.datetime.today().strftime("%d/%m/%y"))
                actualizar = Producto.update(nombre = p1.get(),cantidad = c1.get(),laboratorio = l1.get(), fecha = fecha2).where(Producto.id == id_update)
                actualizar.execute()
                try:
                    self.actualizar_treeview(tree)
                    self.limpiar_datos(p1, l1, c1)
                    return "Se ha modificado: \nProducto: "+ self.producto +"\nLaboratorio:"+ self.laboratorio +"\nCantidad:" + self.cantidad
                except:
                    return "La tabla 'Productos' no fue creada"
                
            else:
                self.limpiar_cantidad(c1)
                return "Error en el campo 'Cantidad'"   
        else:
            self.limpiar_producto(p1)
            return "Error en el campo 'Producto'"
        
    #EXTRAS Relacionadas a la BD---------------------------------------------------------
    def actualizar_treeview(self, tree):
        self.records = tree.get_children()
        try:
            for x in self.records:
                print(x)
                tree.delete(x)
        finally:
            for x in Producto.select():
                tree.insert("", 0, text=x.id, values=(x.nombre, x.cantidad, x.laboratorio,
                                                    x.fecha))
        
    def cargar_entrys(self, producto, laboratorio, cantidad, id):
        try:
            item = Producto.get_by_id(id)
            producto.set(item.nombre)
            laboratorio.set(item.laboratorio)
            cantidad.set(str(item.cantidad))    
            print(item)
        finally:
            pass
    #EXTRAS Relacionadas a la Vista---------------------------------------------------------
    def limpiar_datos(self, producto, combo_laboratorio, cantidad):
        producto.set("")
        combo_laboratorio.set("")
        cantidad.set("")
    def limpiar_producto(self,producto):
        producto.set("")
    def limpiar_cantidad(self,cantidad):
        cantidad.set("")
