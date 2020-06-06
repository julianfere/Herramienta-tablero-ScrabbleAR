import PySimpleGUI as sg
import csv
import sys
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))

def exportar(lista,nombre):  # recibe el layout saca los botones que no son del tablero y los exporta a un csv
    guardar = lista
    guardar.pop(len(guardar)-1)
    if "win" in sys.platform:
        # arch = open(".\\TrabajoFinalPython\\TrabajoFinalPython\\scrabbleAR\\Datos\\guardado.csv","w")

        arch = open(absolute_path + '\\Export\\'+nombre+'.csv',
                    "w")  # esto lo agregue porque no me encontraba el archivo
    else:
        arch = open(absolute_path + "/Export/"+nombre+".csv", "w")

    escritor = csv.writer(arch)
    for aux in lista:
        escritor.writerow(aux[i].get_text() for i in range(len(aux)))
    arch.close()

def abrir():
    arch = open(absolute_path+"/Info/base.csv","r")
    csvreader = csv.reader(arch)
    return csvreader

def crear_pantalla(csvreader):  # Creacion del Layout, interpretando los caracteres del csv traduciendo a botones
    "Carga la pantalla con el base.csv"

    descuento_3 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#F44336')) # rojo

    descuento_2 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#FFB74D')) # marron
   
    descuento = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#000000')) # negro

    premio_2 = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                            pad=(0, 0), button_color=('black', '#8BC34A')) # verde

    blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#FFFFFF')) # blanco
    premio = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black', '#2196F3')) # celeste
    sg.theme("lightblue")
    layout = []
    botones = {}
    key = 0

    i = 0  # i lleva la posicion de fila
    for fila in csvreader:
        fichas = []
        j = 0  # j lleva la posicion de columna
        for boton in fila:
            key = (i, j)  # por lo tanto las key ahora son elementos de una matriz
            if boton == "":  # esto antes eran 4 if, los cambie por un if y 3 elif
                fichas.append(blanco("", key))
                botones[key] = ""
            elif boton == "+":
                fichas.append(premio("", key))
                botones[key] = "+"
            elif boton == "++":
                fichas.append(premio_2("", key))
                botones[key] = "++"
            elif boton == "-":
                fichas.append(descuento("", key))
                botones[key] = "-"
            elif boton == "--":
                fichas.append(descuento_2('', key))
                botones[key] = "--"
            elif boton == "---":
                fichas.append(descuento_3('', key))
                botones[key] = "---"
            j += 1
        layout.append(fichas)
        i += 1
    
    colores = [
        sg.B("R",key="rojo",button_color=("#F44336","#F44336"),size=(4,1)),
        sg.B("M",key="marron",button_color=("#FFB74D","#FFB74D"),size=(4,1)),
        sg.B("C",key="celeste",button_color=("#2196F3","#2196F3"),size=(4,1)),
        sg.B("N",key="negro",button_color=("#000000","#000000"),size=(4,1)),
        sg.B("V",key="verde",button_color=("#8BC34A","#8BC34A"),size=(4,1)),
        sg.B("B",key="blanco",button_color=("#FFFFFF","#FFFFFF"),size=(4,1))        
    ]
    frame = [colores,[sg.T("Color seleccionado:"),sg.T("",key="color",size=(10,1))],
    [sg.B("Guardar",key="guardar")]
    ]
    aux = [sg.Frame("",layout=frame)]
    layout.append(aux)
    return layout,botones


def main():
    colores = ["rojo","marron","negro","blanco","verde","celeste"]
    csvreader = abrir()
    layout,botones = crear_pantalla(csvreader)
    window =  sg.Window("Le Peint",layout)
    color = "blanco"
    while True:
        event,values = window.read()
        print(event,values)
        if event == None:
            break
        if event in colores:
            color = event
            window["color"].update(color)
        if event in botones.keys(): 
            ind = event
            if color == "rojo":                
                window[ind].update("---",button_color=("#F44336","#F44336"))
            elif color == "marron":
                window[ind].update("--",button_color=("#FFB74D","#FFB74D"))
            elif color == "negro":
                window[ind].update("-",button_color=("#000000","#000000"))
            elif color == "verde":
                window[ind].update("++",button_color=("#8BC34A","#8BC34A"))
            elif color == "blanco":
                window[ind].update("",button_color=("#FFFFFF","#FFFFFF"))
            elif color == "celeste":
                window[ind].update("+",button_color=("#2196F3","#2196F3"))
               

        if event == "guardar":
            nombre = sg.popup_get_text("Ingrese nombre del archivo")
            exportar(layout,nombre)






        

if __name__ == "__main__":
    main()

