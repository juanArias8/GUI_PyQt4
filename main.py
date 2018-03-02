"""
Nombre del archivo      :       main.py
Dependencias            :       main.ui, archivos txt o csv
Ejecución del proyecto  :       python3 main.py
Materia                 :       Algoritmos y programación
Docentes                :       Jaime A. Valencia & Álvaro Jaramillo Duque
Semestre                :       2017-2
Estudiante 1            :       nombre_estudiante1
Correo estudiante 1     :       correo_estudiante1
cédula estudiante 1     :       cédula estudante1
Estudiante 2            :       nombre_estudiante2
Correo estudiante 2     :       correo_estudiante2
cédula estudiante 2     :       cédula estudante2
"""

#Importamos las librerías necesarias
import sys
import os
import matplotlib.figure
from PyQt4 import  QtGui, uic
from PyQt4.QtGui import QMainWindow, QFont, QMessageBox, QInputDialog, QImage
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


#Definimos la clase principal main
class main(QMainWindow):

    #Definimos variables globales
    lista = []
    lstlst = []
    a = []
    number_axe_1 = 0
    number_axe_2 = 0
    cwd = os.getcwd()
    dirs = os.listdir(cwd)

    #Creamos el constructor de la clase
    def __init__(self):
        QMainWindow.__init__(self)

        #Cargamos el archivo que contiene la interfáz gráfica
        uic.loadUi("main.ui", self)

        #Configuramos tamaño mínimo y máximo
        self.setMinimumSize(863, 640)
        self.setMaximumSize(863, 640)

        #Configuramos la fuente
        qfont = QFont("Arial", 12)
        self.setFont(qfont)

        #Centramos la ventana en la pantalla
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        #Definimos el área de dibujo
        grid = QtGui.QGridLayout()
        self.frame_figure.setLayout(grid)
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas)

        #Desactivamos los botones btn_select_file, btn_plot_data, btn_save_figure
        self.btn_select_file.setEnabled(False)
        self.btn_plot_data.setEnabled(False)
        self.btn_save_figure.setEnabled(False)

        #Asociamos los eventos (Funciones) a los botones del sistema
        self.btn_show_files.clicked.connect(self.show_files)
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_plot_data.clicked.connect(self.show_plot)
        self.btn_save_figure.clicked.connect(self.save_figure)
        self.btn_restart.clicked.connect(self.restart)

    #Función show_files
    def show_files(self):
        """
        La función show_files hace un análisis de los archivos que se encuentren en el directorio actual,
        haciendo un filtro con la extención de cada archivo y guardando en lista[] los archivos cuya
        extención sea .txt o .csv, posteriormente muestra en un área de texto dicha lista.
        """
        #Declaramos variables locales
        n = 0

        #Deshabilitamos el botón btn_show_files y habilitamos el botón btn_select_file
        self.btn_show_files.setEnabled(False)
        self.btn_select_file.setEnabled(True)

        #Creamos el ciclo que se encarga de analizar la extensión de los archivos y almacenarlos en la lista
        for i in self.dirs:
            if ".csv" in i or ".txt" in i:
                self.lista.append(i)

        #Creamos una condición preventiva que se ejecutará en caso de que el directorio no contenga archivos válidos
        if (len(self.lista) == 0):

            #Mostramos un mensaje de alerta indicando de que no hay archivos válidos
            QMessageBox.warning(self, "File Error",
                                "Ha ocurrido un error, No hay archivos disponibles!!!")

            # Deshabilitamos el botón btn_select_files y habilitamos el botón btn_show_file
            self.btn_select_file.setEnabled(False)
            self.btn_show_files.setEnabled(True)

        #Creamos la condición para el caso de que si hayan archivos
        else:
            text = ("                                            ARCHIVOS DISPONIBLES\n"
                    "----------------------------------------------------------------------------------------------------------\n")
            #Mostramos los archivos disponibles en un área de texto
            for i in self.lista:
                n = n + 1
                text += (str(n) + "." + i + "\t\t")
                self.area_text.setText(text)


    #Función select_files
    def select_file(self):
        """
        La función select_files permite seleccionar de la lista de archivos disponibles un archivo,
        además se encarga de crear las estructuras de datos necesarias para almacenarlas en memoria local
        y de corregir posibles errores en los datos
        """
        #Definimos variables locales
        error = []
        indiceserror = []
        filaserror = []

        #Deshabilitamos el botón btn_select_file y habilitamos el botón btn_plot_data
        self.btn_select_file.setEnabled(False)
        self.btn_plot_data.setEnabled(True)

        #Solicitamos al usuario que ingrese el índice del archivo a ser cargado, la variable number_file almacena
        #dicho índice, mientras la variable ok almacena el estado de la solicitud
        number_file, ok = QInputDialog.getInt(self, "Select File", "Ingrese el número del archivo a procesar")

        #Verificamos que la variable ok contenga un dato exitoso, esto es, verdadero
        if ok:

            #Verificamos que el número ingresado por el usuario corresponda al índice de un archivo
            if number_file in range(1,len(self.lista)+1):

                #Guardamos en la variable file el nombre del archivo
                file = self.lista[number_file - 1]

                #Abrimos el archivo
                openf = open(file)

                #Mostramos en el campo de texto file_loaded_text el nombre del archivo cargado
                self.file_loaded.setText("Se ha abierto el archivo " + openf.name);

                #Creamos la variable route que contiene la ruta absoluta del archivo
                route = self.cwd + "/" + openf.name;

                #Mostramos en el campo de texto dir_file_loaded la ruta
                self.dir_file_loaded.setText(route)

                #Procesamos el archivo cargado eliminando comas y puntoycomas que se encuentren en los archivos
                for line in openf:

                    #Realizamos los procedimientos necesarios en caso de que el archivo sea txt
                    if ".txt" in file:
                        if "," in line:
                            temp_list = line.split(",")
                        if ";" in line:
                            temp_list = line.split(";")

                        #Agregamos los datos a la lista lstlst
                        self.lstlst.append(temp_list)

                    # Realizamos los procedimientos necesarios en caso de que el archivo sea csv
                    if ".csv" in file:
                        temp_list = line.split(";")

                        # Agregamos los datos a la lista lstlst
                        self.lstlst.append(temp_list)

                #Procesamos la lista lstlst eliminando posibles errores
                for i in self.lstlst:
                    for j in i:

                        #Intentamos convertir los datos de la lista en números reales
                        try:
                            j = float(j)

                        #Capturamos cualquier posible error en el proceso de conversión y obtenemos el índice del error
                        except ValueError:
                            error.append(j)
                            indiceserror.append(i.index(j))
                            filaserror.append(self.lstlst.index(i))

                #Eliminamos de lstlst los datos que contengan errores
                for i in range(0, len(error)):
                    self.lstlst[filaserror[i]].remove(error[i])
                    self.lstlst[filaserror[i]].insert(indiceserror[i], None)

            #Mostramos una alerta en caso de que el usuario ingrese un número que no corresponde aun índice
            else:
                QMessageBox.warning(self, "Select File Error",
                                    "Ha ocurrido un error, verifique los datos ingresados!!!")

                #Habilitamos el botón btn_select_file y deshabilitamos el botón btn_plot_data
                self.btn_select_file.setEnabled(True)
                self.btn_plot_data.setEnabled(False)

        #Procesamos un posible error en la entrada de datos, esto es, ok es falso
        else:
            QMessageBox.warning(self, "Select File Error",
                                "Ha ocurrido un error, verifique los datos ingresados!!!")

            #Habilitamos el botón btn_select_file y deshabilitamos el botón btn_plot_data
            self.btn_select_file.setEnabled(True)
            self.btn_plot_data.setEnabled(False)


    #Función show_plot
    def show_plot(self):
        """
        La funcíón show_plot es la encargada de mostar la gráfica de los datos, para realizar dicha tarea, primero
        se muestran las columnas disponibles para la comparación (lo que llamarémos ejes), cada eje corresponde a una
        columna del archivo, además permite al usuario seleccionar dos de dichos ejes para realizar la comparación,
        separa los datos en listas y por último grafica dicha información,
        """
        #Definimos variables locales
        primereje = []
        segundoeje = []
        op = 0
        e = "eje "
        n = 0
        text_eje_x = "     "
        text_eje_y = "     "

        #Deshabilitamos el botón btn_plot_data y habilitamos el botón btn_save_figure
        self.btn_plot_data.setEnabled(False)
        self.btn_save_figure.setEnabled(True)

        #Contamos el número de ejes
        temp_list = self.lstlst[1]

        #Agregamos los ejes dispobibles a la lista a
        for i in range(1, len(temp_list) + 1):
            op += 1
            self.a.append(e + str(op))
        text = ("                                            EJES DISPONIBLES\n"
                    "----------------------------------------------------------------------------------------------------------\n")

        #Mostramos los ejes disponibles en un área de texto
        for i in self.a:
            n = n + 1
            text += (str(n) + ".  " + i + " \t\t ")
            self.area_text.setText(text)

        #Solicitamos al usuario que ingrese el primer eje a graficar (La solicitud se realiza mientras
        #los datos ingresados sean erroneos)
        while(True):

            #Solicitamos el primer eje a graficar, la variable global number_axe_1 contiene el número del eje,
            #la variable ok contiene información sobre el éxito de la solicitud
            self.number_axe_1, ok = QInputDialog.getInt(self, "Select Axe", "Ingrese el número del primer eje a graficar")

            #Definimos las instrucciones correspondientes al éxito de la solicitud
            if ok:

                #Verificamos que el número ingresado corresponda a un índice de eje, en caso de que sea cierto
                #salimos del ciclo while
                if self.number_axe_1 in range(1, len(self.a) +1 ):
                    break

                #Procesamos el posible error de que el dato ingresado sea erroneo
                else:
                    QMessageBox.warning(self, "Select Axe Error",
                                        "Ha ocurrido un error, verifique los datos ingresados!!!")

            #Procesamos un posible error en caso de que la solicitud no se realice con éxito
            else:
                QMessageBox.warning(self, "Select Axe Error",
                                    "Ha ocurrido un error, verifique los datos ingresados!!!")

        #Solicitamos al usuario que ingrese el segundo eje a graficar (La solicitud se realiza mientras
        #los datos ingresados sean erroneos)
        while (True):

            #Solicitamos el segundo eje a graficar, la variable global number_axe_2 contiene el número del eje,
            #la variable ok contiene información sobre el éxito de la solicitud
            self.number_axe_2, ok = QInputDialog.getInt(self, "Select Axe", "Ingrese el número del segundo eje a graficar")

            #Definimos las instrucciones correspondientes al éxito de la solicitud
            if ok:

                #Verificamos que el número ingresado corresponda a un índice de eje
                if self.number_axe_2 in range(1, len(self.a) + 1):

                    #Comprobamos que el número ingresado para el segundo eje sea diferente del número ingresado
                    #para el primer eje, si la condición se cumple salimos del while
                    if (self.number_axe_1 != self.number_axe_2):
                        break

                    #Procesamos el posible error de que el dato ingresado sea igual al primero
                    else:
                        QMessageBox.warning(self, "Select Axe Error",
                                            "Ha ocurrido un error, Debe seleccionar un eje diferente!!")

                #Procesamos el posible error de que el dato ingresado sea erroneo
                else:
                    QMessageBox.warning(self, "Select Axe Error",
                                        "Ha ocurrido un error, verifique los datos ingresados!!!")

            #Procesamos un posible error en caso de que la solicitud no se realice con éxito
            else:
                QMessageBox.warning(self, "Select Axe Error",
                                    "Ha ocurrido un error, verifique los datos ingresados!!!")

        #Agregamos los datos de los ejes a comparar en dos listas
        for i in self.lstlst:
            primereje.append(i[self.number_axe_1 - 1])
            segundoeje.append(i[self.number_axe_2 - 1])

        #Agregamos los datos de los ejes a comparar en dos cadenas
        for i in range(len(primereje)):
            text_eje_x += (primereje[i]) + "\n     "
        for i in range(len(segundoeje)):
            text_eje_y += (segundoeje[i]) + "\n     "

        #Mostramos en las áreas de texto data_eje_x y data_eje_y las cadenas que contienen los datos
        self.data_eje_x.setText(text_eje_x)
        self.data_eje_y.setText(text_eje_y)

        #Preparamos la figura para mostrar la gráfica
        self.figure.clf()
        ax = self.figure.add_subplot(111)

        #Mostramos la gráfica de los datos
        ax.plot(primereje, segundoeje, 'r.-')

        #Agregamos un título a la gráfica
        ax.set_title(self.a[self.number_axe_2 - 1] + " vs " + self.a[self.number_axe_1 - 1])

        #Mostramos los datos
        self.canvas.draw()


    #Función save_figure
    def save_figure(self):
        """
        La función save_figure contiene las instrucciones necesarias para almacenar una imagen en formato png
        de la gráfica mostrada
        """
        #Deshabilitamos el botón btn_save_figure
        self.btn_save_figure.setEnabled(False)

        #Obtenemos el tamaño de la gráfica
        size = self.canvas.size()

        #Obtenemos el ancho y el alto de la imagen en las variables width y height
        width, height = size.width(), size.height()

        #Creamos la imagen a guardar
        im = QImage(self.canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)

        #Guardamos la imagen en formato png
        im.save(str(self.a[self.number_axe_2 - 1] + self.a[self.number_axe_1 - 1] + ".png"))

        #Informamos que la imagen ha sido guardad con éxito
        QMessageBox.information(self, "Save Figure Success",
                                "La gráfica ha sido guardada!!!")

        #Mostramos en el campo de texto dir_img_shown la dirección de la imagen guardada
        dir_image_save = self.cwd + "/" + str(self.a[self.number_axe_2 - 1] + self.a[self.number_axe_1 - 1] + ".png")
        self.dir_img_shown.setText(dir_image_save)


    #Función restart
    def restart(self):
        """
        La función restart contiene el conjunto de instrucciones necesarias para preparar el sistema
        con el fin repetir el proceso de graficación de imágenes, se encarga de llevar a sus estados iniciales
        todas las variables globales utilizadas, limpiar los campos y áreas de texto y limpiar el área de graficado
        """
        #Restauramos las variables globales
        self.lista = []
        self.lstlst = []
        self.a = []
        self.number_axe_1 = 0
        self.number_axe_2 = 0

        #Limpiamos campos y áreas de texto
        self.data_eje_x.setText("")
        self.data_eje_y.setText("")
        self.file_loaded.setText("")
        self.dir_file_loaded.setText("")
        self.dir_img_shown.setText("")
        self.area_text.setText("")

        #Habilitamos el botón btn_show_files y deshabilitamos el botón btn_save_figure
        self.btn_show_files.setEnabled(True)
        self.btn_save_figure.setEnabled(False)

        #Reseteamos el área de graficado
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.plot(0, 0)
        self.canvas.draw()


    #Función closeEvent
    def closeEvent(self, QCloseEvent):
        """
        La función closeEvent contiene las instrucciones a ser seguidas al momento de cerrar la aplicación
        """
        #Preguntamos al usuario si realmente quiere salir de la aplicación
        result = QMessageBox.question(self, "Salir...", "¿Seguro que quieres cerrar la aplicación?",
                                      QMessageBox.Yes | QMessageBox.No)

        #Cerramos la aplicación en caso de respuesta afirmatica
        if result == QMessageBox.Yes:
            QCloseEvent.accept()

        #Ignoramos el evento en caso de que la respuesta sea negativa
        else:
            QCloseEvent.ignore()


#Ejecutamos la aplicación
app = QtGui.QApplication(sys.argv)
myWindow = main()
myWindow.show()
sys.exit(app.exec_())
