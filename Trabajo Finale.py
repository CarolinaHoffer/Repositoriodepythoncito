import PySimpleGUI as sg
import random as rd
import string
import constantes as const
#EJEMPLO LAYOUT  columna 1                   x,y    columna 2
#LAYOUT=[[sg.ReadButton('r',size=(1,1), key=(0,0), sg.ReadButton(..)],fila 1
#        [sg.ReadButton('q',size=(1,1), key=(0,1), sg.ReadButton(..)]]fila 2
#
##palabra={'casa':'sust','beber':'verb','ridiculo':'adj','gato':'sust', 'frío':'adj','ver':'verb','manta':'sust','saltar':'verb','lapiz':'sust', 'ser':'verb'}
palabra={'casa':'sust','ver':'verb','lindo':'adj'}
sg.SetOptions(background_color='#ffe4b5',button_color=const.COLOR_BOTON,text_element_background_color='#ffe4b5')
def agregar_fila(layout, m, cant):
    lista=[]
    for x in range(m):
        lista.append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(x,cant)))
    layout.append(lista)
    return layout
def agregar_columna(layout, m, cant):
    for i in range(m):
        layout[i].append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(cant,i)))
    return layout
def crear_cuadrado(m):
    layout=[]
    for i in range(m):
        lista=[]
        for x in range(m):
            lista.append(sg.ReadButton(rd.choice(string.ascii_letters).upper(),size=(1,1),font='Bold',key=(x,i)))
        layout.append(lista)
    return layout
def invertido(palabra):
    invertido=rd.randrange(2)
    if invertido == 1:
        palabra=palabra[::-1]
    return palabra
def agregar_horizontal(layout,dic_palabras,invertir,longitud,letra):
    cant=longitud-1
    lista_coordenadas=[]
##    tipos={'verb':[],'adj':[],'sust':[]}
    lista_filas=list(range(longitud))
    dic={}
    coor_pal={}
    for var in dic_palabras:
        coor_pal[var]=[dic_palabras[var],[]]
    for fila in range(longitud):
        dic[fila]=[]
    for palabra in dic_palabras:
        llave=palabra
        while True:
            try:
                fila=rd.choice(lista_filas)
                mover=(longitud-len(palabra))+1
                columna=rd.randrange(mover)
                if dic[fila]:
                    pri=dic[fila][0][0]
                    if pri>=len(palabra):
                        columna=rd.randrange(pri-len(palabra)+1)
                        break
                    else:
                        ult=dic[fila][-1][0]
                        if (longitud-1)-ult==len(palabra):
                            columna=ult+1
                            break
                        elif (longitud-1)-ult>len(palabra):
                            pos=ult+1
                            columna=rd.randrange(pos,pos+((longitud-1)-(pos-1)-len(palabra)))
                            break    
                    lista_filas.remove(fila) 
                else:
                    break                 
            except:
                cant+=1
                layout = agregar_fila(layout,longitud,cant)
                lista_filas.append(cant)
                dic[cant]=[]
        if(invertir==True):
            palabra=invertido(palabra)
        if letra==True:
            palabra=palabra.upper()  
        for caracter in palabra:
            layout[fila][columna]=sg.ReadButton(caracter,size=(1,1),button_color=('white','red'),font='Bold',key=(columna,fila))
            lista_coordenadas.append((columna,fila))
            dic[fila].append((columna,fila))
            coor_pal[llave][1].append((columna,fila))
            columna+=1
    return(layout,coor_pal,lista_coordenadas)        
def agregar_vertical(layout,dic_palabras,invertir,longitud,letra=False):
    dic={}
    coor_pal={}
    for var in dic_palabras:
        coor_pal[var]=[dic_palabras[var],[]]    
    cant=longitud-1
    for x in range(longitud):
        dic[x]=[]
    lista_columnas=list(range(longitud))
    lista_coordenadas=[]
    for palabra in dic_palabras:
        llave=palabra
        while True:
            try:
                columna=rd.choice(lista_columnas)
                mover=(longitud-len(palabra))+1
                fila=rd.randrange(mover)
                if dic[columna]:
                    pri=dic[columna][0][1]
                    if pri>=len(palabra):
                        fila=rd.randrange(pri-len(palabra)+1)
                        break
                    elif pri<len(palabra):
                        ult=dic[columna][-1][1]
                        if (longitud-1)-ult==len(palabra):
                            fila=ult+1
                            break
                        elif ((longitud-1)-ult>len(palabra)):    
                            ult+=1
                            fila=rd.randrange(ult,ult+(((longitud-1)-(ult-1))-len(palabra)))
                            break
                    lista_columnas.remove(columna)                                   
                else:
                    break
            except(IndexError):
                cant+=1
                layout = agregar_columna(layout,longitud,cant)
                lista_columnas.append(cant)
                dic[cant]=[]
        if(invertir==True):
            palabra=invertido(palabra)
        if letra==True:
            palabra=palabra.upper()              
        for caracter in palabra:
            layout[fila][columna]=sg.ReadButton(caracter,size=(1,1),font='Bold',button_color=('white','red'),key=(columna,fila))
            lista_coordenadas.append((columna,fila))
            dic[columna].append((columna,fila))
            coor_pal[llave][1].append((columna,fila))
            fila+=1
    return(layout,coor_pal,lista_coordenadas)
def agregar_botones(layout,palabras):
    lista=[]
    for pal in palabras:
        cadena=''
        for x in pal:
            cadena+='_ '   
        lista.append(sg.Text(cadena))
    layout.append(lista)    
    layout.append([sg.Button('Sustantivos',button_color=('white','blue')),sg.Button('Verbos', button_color=('white', 'green')),
                   sg.Button('Adjetivos', button_color=('white', 'red')),sg.Button('Borrar Tablero'),sg.Button('Borrar boton')])
    layout.append([sg.Button('Cerrar'),sg.Button('Listo!')])
    return layout
def agregar_palabras(palabras, invertir=False ,posicion='horizontal',letra=False):
    longitud=max(len(elem) for elem in palabras)
    layout=crear_cuadrado(longitud)
    if posicion=='horizontal':
        layout,coordenadas,lista_coord= agregar_horizontal(layout,palabras, invertir,longitud,letra)
    elif posicion=='vertical':
        layout,coordenadas,lista_coord= agregar_vertical(layout,palabras,invertir,longitud,letra)
    return agregar_botones(layout,palabras),coordenadas,lista_coord
def comprobar(pintadas, coordenadas):
    OK=[]
##    for x in coordenadas:#toma palabra
##        for s in coordenadas[x][1]:
##            print(s,' y ',pintadas[coordenadas[x][0]])
##            if s in pintadas[coordenadas[x][0]]:
##                print('verdad')
##                OK.append(True)
##            else:
##                print('mentira')
##                OK.append(False)
##                break
    for x in coordenadas:            
        if all(map(lambda elem: False if not elem in coordenadas[x][1] else True,pintadas[coordenadas[x][0]]))and pintadas[coordenadas[x][0]]:
            OK.append(True)
        else:
            OK.append(False)
    if all(OK):        
#all devuelve true si en el iterable pasado como argumento no hay ningun false. Pregunto and pintadas ya que python devuelve false si la estructura esta vacia.
        layout=[[sg.Text('Lo haz logrado!',font='Bold')],[sg.OK()]]
    else:
        layout=[[sg.Text('No haz marcado con los colores correctos o te faltaron marcar',font='Bold')],[sg.OK()]]
    window=sg.Window('Resultado').Layout(layout)
    button,valor=window.Read()
    if button=='OK'or None:
        window.Close()

layout,coor,lis_coord=agregar_palabras(palabra,invertir=True, posicion='vertical',letra=True)
window=sg.Window('Sopa de letras').Layout(layout)
ingresados={'verb':[],'adj':[],'sust':[]}
adjetivos=[]
verbos=[]
color=const.COLOR_BOTON
no_marcado=[]
while True:
    event,values=window.Read()
    if(event=='Cerrar'or None):
        break
    elif type(event)==tuple:
        print(color)
        if(color[1]=='red'):
            ingresados['adj'].append(event)
        elif(color[1]=='green'):
            ingresados['verb'].append(event)
        elif(color[1]=='blue'):
            ingresados['sust'].append(event)
        elif(color==const.COLOR_BOTON):
            for var in ingresados:
                if event in ingresados[var]:
                    ingresados[var].remove(event)                    
        window.FindElement(event).Update(button_color=color)
    elif(event=='Adjetivos'):
        color=('white','red')
    elif(event=='Sustantivos'):
        color=('white','blue')
    elif(event=='Verbos'):
        color=('white','green')
    elif(event=='Borrar boton'):
        color=const.COLOR_BOTON
    elif(event=='Borrar Tablero'):
        for llave in ingresados:
            if ingresados[llave]:
                for var in ingresados[llave]:
                    window.FindElement(var).Update(button_color=const.COLOR_BOTON)
        for llave in ingresados:
            ingresados[llave].clear()            
    elif(event=='Listo!'):
        comprobar(ingresados, coor)
window.Close()        
###
##ACTUALIZACION 0.3:
##Se puede poner dos palabras por fila en orden horizontal y por columna en orden vertical
##Se puede comprobar si se marcaron todos los verbos, adjetivos y sustantivos correctamente
##Se puede borrar todo el tablero y con opcion de borrar una letra mal marcada
##Se necesita configurar las ayudas, ideas:multiline con las palabras a buscar y/o cantidad de verb/adj/sust a buscar
##Se necesita implementar el menu del docente
##Se necesita implementar el revisado de wikidictionary y pattern
##Se necesita implementar la eleccion al azar de las palabras ingresadas
