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

def base():
    dic = dict()
    
    for x in range(15):
        for y in range(15):
            dic[(x,y)] = ""

    base = open(os.path.join(absolute_path,"Info","base.json"),"w")
    dic_fin = convertirJson(dic)
    json.dump(dic_fin,base,indent=1)

#----------------------------------------------------------------------------------

def crear_layout(colores,dificultad):
    casillero = lambda name, key: sg.Button('', border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), button_color=('black',"white"))

    # casilleros con letras de una partida anterior:

    ficha_pc = lambda name,key: sg.Button(name, disabled=True, border_width = 3, size = (3,1), key = key, pad = (0,0), button_color = ("#000000","green"),
                                            disabled_button_color = ("#000000","green"))

    # blanco = lambda name, key: sg.Button(name, border_width=1, size=(3, 1), key=key,
    #                                      pad=(0, 0), button_color=('black', 'white'))

    ficha_jugador = lambda name, key: sg.Button(name, disabled=True,border_width=3, size=(3, 1), key=key,
                                         pad=(0, 0), disabled_button_color=('black', "blue"),button_color=('black', "blue"))

    base = open(os.path.join(absolute_path,"Info","base.json"),"r")
    tablero = json.load(base)
    tab = convertirDic(tablero)
    # import pprint
    # p = pprint.PrettyPrinter(indent=2)
    # p.pprint(tab)
    layout = []
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
            # casilleros que ya están ocupados por letras (caso de partida previamente guardada)
            elif (tab[key][0] in string.ascii_uppercase) and (tab[key] != " "):
                if (len(tab[key])> 1):
                    if tab[key][1] == "*":
                        fichas.append(ficha_pc(tab[key][0],key)) # casillas ocupadas por la maquina en una partida previa fueron guardadas con *
                    else:
                        fichas.append(ficha_jugador(tab[key][0],key))  # casillas ocupadas por el jugador en una partida previa
                botones[key] = ""
        layout.append(fichas)
    tipo_ficha = ["blanco","---","--","-","+","++","+++","++++"]
    frame_layout = [
        [sg.InputCombo(tipo_ficha,key="col")],[sg.Button("Guardar",key="g")]
    ]
    frame = [sg.Frame("cosa",layout=frame_layout)]
    layout.append(frame)
    return layout, botones


colores =  open(os.path.join(absolute_path,"info","colores.json"),"r")
col = json.load(colores)
dificultad = sg.popup_get_text("facil medio dificil")
layout,botones = crear_layout(colores,dificultad)
window = sg.Window("asd",layout)
while True:
    event,  values =  window.read()
    print(event)
    if (event == None):
        break
    if event in botones.keys():
        ind = event
        valor =values["col"]
        print(valor)
        if valor == "blanco":
            window[ind].update("",button_color=("white","white"))
        else:
            window[ind].update(valor,button_color=('black',col[dificultad][valor]))
        botones[ind] = valor if valor != "blanco" else ""
    if event == "g":
        nombre = sg.popup_get_text("Ingrese nombre de json")
        dic = convertirJson(botones)
        datos = open(os.path.join("Export",nombre+".json"),"w")
        json.dump(dic,datos)
        datos.close()

    
window.close()
            
