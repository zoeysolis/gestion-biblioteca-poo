import wx

# --- LÓGICA DE NEGOCIO (POO) ---

class Recurso:
    """Clase base para cualquier recurso de la biblioteca."""
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponible = True

    def obtener_tipo(self):
        return "Recurso"

class Libro(Recurso):
    """Subclase que representa un Libro (Herencia)."""
    def obtener_tipo(self):
        return "Libro"

class Revista(Recurso):
    """Subclase que representa una Revista (Herencia)."""
    def obtener_tipo(self):
        return "Revista"

class Biblioteca:
    """Clase que gestiona la colección de objetos."""
    def __init__(self):
        self.catalogo = [
            Libro("Cien años de soledad", "Gabriel García Márquez"),
            Libro("Fundación", "Isaac Asimov"),
            Revista("National Geographic", "Varios"),
            Libro("El Aleph", "Jorge Luis Borges")
        ]

    def prestar_recurso(self, indice):
        recurso = self.catalogo[indice]
        if recurso.disponible:
            recurso.disponible = False
            return True
        return False

# --- INTERFAZ GRÁFICA (wxPython) ---

class VentanaBiblioteca(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Gestor de Biblioteca POO', size=(500, 400))
        self.biblioteca = Biblioteca()
        self.configurar_interfaz()
        self.actualizar_lista()
        self.Show()

    def configurar_interfaz(self):
        panel = wx.Panel(self)
        self.sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Tabla de recursos
        self.lista = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista.InsertColumn(0, 'Tipo', width=80)
        self.lista.InsertColumn(1, 'Título', width=200)
        self.lista.InsertColumn(2, 'Estado', width=100)

        # Botón de acción
        self.btn_prestar = wx.Button(panel, label="Prestar Recurso Seleccionado")
        self.btn_prestar.Bind(wx.EVT_BUTTON, self.al_prestar)

        self.sizer_principal.Add(self.lista, 1, wx.ALL | wx.EXPAND, 10)
        self.sizer_principal.Add(self.btn_prestar, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(self.sizer_principal)

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        for idx, r in enumerate(self.biblioteca.catalogo):
            self.lista.InsertItem(idx, r.obtener_tipo())
            self.lista.SetItem(idx, 1, r.titulo)
            estado = "Disponible" if r.disponible else "Prestado"
            self.lista.SetItem(idx, 2, estado)

    def al_prestar(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion == -1:
            wx.MessageBox("Por favor, seleccione un ítem de la lista.", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return

        exito = self.biblioteca.prestar_recurso(seleccion)
        if exito:
            wx.MessageBox("¡Préstamo realizado con éxito!", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.actualizar_lista()
        else:
            wx.MessageBox("El recurso ya se encuentra prestado.", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    VentanaBiblioteca()
    app.MainLoop()
