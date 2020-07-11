import json
import PySimpleGUI as sg 
import os
import string
import math

absolute_path = os.path.dirname(os.path.abspath(__file__))
def convertirJson(dic):
    """
    Parsea el Json para poder guardarlo
    """
    # import pprint
    # p = pprint.PrettyPrinter(indent = 2)
    # p.pprint(self._botones)
    dic_aux = {}
    for clave,valor in dic.items():
        dic_aux[str(clave[0])+","+str(clave[1])] = valor        
    return dic_aux


def convertirDic(botones):
    """
    Vuelve a darle formato al diccionario de botones
    """
    dic_aux = {}
    for clave,valor in botones.items():
        dic_aux[tuple(map(int,clave.split(",")))] = valor  
    # import pprint
    # p = pprint.PrettyPrinter(indent=4)
    # p.pprint(dic_aux)
    return dic_aux

def base(tamaño):
    dic = dict()
    
    for x in range(tamaño):
        for y in range(tamaño):
            dic[(x,y)] = ""

    base = open(os.path.join(absolute_path,"Info","base.json"),"w")
    dic_fin = convertirJson(dic)
    json.dump(dic_fin,base,indent=1)

#----------------------------------------------------------------------------------
def crear_menu():
    valores = [15 + i for i in range(10)]
    layout_menu = [
        [sg.Radio("facil",group_id="grupo",key="facil",default=True),sg.Radio("medio",group_id="grupo",key="medio"),sg.Radio("dificil",group_id="grupo",key="dificil")],
        [sg.T("Tamaño de la matriz"),sg.Spin(valores,key="tam",initial_value=15)],
        [sg.B("Dibujar",key="dibujo",size=(20,None))]
    ]
    return layout_menu
#----------------------------------------------------------------------------------

def crear_layout(colore,dificultad):
    casillero = lambda name, key: sg.Button('', border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=("white",colore[dificultad][name]if name != "blanco" else colore[dificultad][""]))

    print(colore[dificultad]["++++"])
    base = open(os.path.join(absolute_path,"Info","base.json"),"r")
    tablero = json.load(base)
    tab = convertirDic(tablero)
    # import pprint
    # p = pprint.PrettyPrinter(indent=2)
    # p.pprint(tab)
    layout = []
    layout_fichas = []
    largo = int(math.sqrt(len(tab)))
    botones = dict()
    for x in range(largo):
        fichas = []
        for y in range(largo):
            key = (x,y)
            if tab[key] == "":
                fichas.append(casillero('', key))
                botones[key] = ""
            elif tab[key] == "+":
                fichas.append(casillero('+', key))
                botones[key] = "+"
            elif tab[key] == "++":
                fichas.append(casillero('++', key))
                botones[key] = "++"
            elif tab[key] == '+++':
                fichas.append(casillero('+++', key))
                botones[key] = '+++'
            elif tab[key] == '++++':
                fichas.append(casillero('++++', key))
                botones[key] = '++++'   
            elif tab[key] == "-":
                fichas.append(casillero('-', key))
                botones[key] = "-"
            elif tab[key] == "--":
                fichas.append(casillero('--', key))
                botones[key] = "--"
            elif tab[key] == "---":
                fichas.append(casillero('---', key))
                botones[key] = "---"
            
        layout_fichas.append(fichas)
    tipo_ficha = ["blanco","---","--","-","+","++","+++","++++"]
    frame_layout = [
        [casillero(name,name)for name in tipo_ficha],
        [sg.Button("Guardar",key="g")]
    ]
    columna_datos = []
    premio_y_descuento = {'': 'Simple', '+': 'Duplica puntaje por letra', '++': 'Triplica puntaje por letra', '+++': 'Duplica puntaje por palabra', '++++': 'Triplica puntaje por palabra', '-': 'Resta 1 pto', '--': 'Resta 2 ptos', '---': 'Resta 3 ptos'}
    info_colores = list(map(lambda x: [sg.Button(button_color=('white',colore[dificultad][x]), size=(3,1), disabled=True), sg.Text(premio_y_descuento[x])], colore[dificultad].keys()))

    for i in range(len(info_colores)):
        columna_datos.append(info_colores[i])
    col = [sg.Column(columna_datos)]
    frame = [sg.Frame("Botones",layout=frame_layout)]
    columna_principal = [
        [sg.Col(layout_fichas)]+col
    ]
    layout.extend(columna_principal)
    layout.append(frame)
    return layout, botones


sg.LOOK_AND_FEEL_TABLE['MyNewTheme'] = {'BACKGROUND': '#c5dbf1',
                                    'TEXT': '#000000',
                                    'INPUT': '#2a6daf',
                                    'TEXT_INPUT': '#000000',
                                    'SCROLL': '#2a6daf',
                                    'BUTTON': ('white', '#2a6daf'),
                                    'PROGRESS': ('#2a6daf', '#2a6daf'),
                                    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                    }

sg.theme("MyNewTheme")

colores =  open(os.path.join(absolute_path,"info","colores.json"),"r")
col = json.load(colores)

window_menu  = sg.Window("Main menu",crear_menu())
while True:
    event, values = window_menu.read()
    if (event ==  None):
        break
    
    if (event == "dibujo"):
        if (window_menu["facil"].get()):
            dificultad = "facil"
        elif (window_menu["medio"].get()):
            dificultad = "medio"
        elif (window_menu["dificil"].get()):
            dificultad = "dificil"
        tamaño = int(window_menu["tam"].get())
        base(tamaño)
        window_menu.close()


        layout,botones = crear_layout(col,dificultad)
        window_2 = sg.Window("Board Maker",layout)
        tipos = ["-","--","---","+","++","+++","++++","blanco"]
        while True:
            event,  values =  window_2.read()
            print(event)
            if (event == None):
                break
            if (event in tipos):
                color = col[dificultad][event] if event != "blanco" else col[dificultad][""]
                ind = event
                ficha = event if event != "blanco" else ""
            if event in botones.keys():
                ind = event
                window_2[ind].update(ficha,button_color=('black',color))
                botones[ind] = ficha
            if event == "g":
                nombre = sg.popup_get_text("Ingrese nombre de json")
                dic = convertirJson(botones)
                datos = open(os.path.join("Export",nombre+".json"),"w")
                json.dump(dic,datos,indent=1)
                datos.close()

    
        window_2.close()
            
