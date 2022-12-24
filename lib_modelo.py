import pandas as pd
import string
import time

datos = pd.read_csv("LALIGA.csv", names=["equipo", "partidos", "goles favor", "goles contra", "per goles favor", 
                                               "per goles contra", "tiros favor", "conversion tiros", "tiros por partido",
                                               "tiros recibidos","conversion tiros contra","tiros recibidos por partido","racha de 5",
                                               "posicion en liga"])

datos["per goles contra"] = datos["per goles contra"].astype(float)

#Definición de funciones
def strtime() -> str:
    t=tuple(time.localtime())
    return f'{str(t[2]).zfill(2)}-{str(t[1]).zfill(2)}-{str(t[0]).zfill(2)} {str(t[3]).zfill(2)}:{str(t[4]).zfill(2)}:{str(t[5]).zfill(2)}'

def contador_racha(dataframe):
    racha_local=dataframe.iloc[0,12]
    racha_visitante=dataframe.iloc[1,12]
    cuenta_local=0
    cuenta_visitante=0
    for letra in racha_local:
        if letra=='V':
            cuenta_local+=2
        if letra=='E':
            cuenta_local+=1
    for letra in racha_visitante:
        if letra=='V':
            cuenta_visitante+=2
        if letra=='E':
            cuenta_visitante+=1
    return (cuenta_local,cuenta_visitante)

def contador_goles(dataframe):
    gol_local=(((float(dataframe.iloc[0,4])+float(dataframe.iloc[1,5]))/2)+((float(dataframe.iloc[0,8])+float(dataframe.iloc[1,11]))/2)*((float(dataframe.iloc[0,7])+float(dataframe.iloc[1,10]))))/2
    gol_local+=0.74
    gol_visitante=(((float(dataframe.iloc[1,4])+float(dataframe.iloc[0,5]))/2)+((float(dataframe.iloc[1,8])+float(dataframe.iloc[0,11]))/2)*((float(dataframe.iloc[1,7])+float(dataframe.iloc[0,10]))))/2
    return(gol_local,gol_visitante)

def contador_posicion(dataframe):
    victoria=0
    derrota=0
    empate=0
    diff_pos=int(dataframe.iloc[0,13])-int(dataframe.iloc[1,13])
    if diff_pos<0:
        if 0>diff_pos>-5:
            victoria+=2
            empate+=6
            derrota+=2
        if -5>=diff_pos>-10:
            victoria+=5
            empate+=3
            derrota+=2
        if -10>=diff_pos>-15:
            victoria+=7
            empate+=2
            derrota+=1
        if -15>=diff_pos:
            victoria+=8
            empate+=1
            derrota+=1
    else:
        if 0<diff_pos<5:
            victoria+=2
            empate+=6
            derrota+=2
        if 5<=diff_pos<10:
            victoria+=2
            empate+=3
            derrota+=5
        if 10<=diff_pos<15:
            victoria+=1
            empate+=2
            derrota+=7
        if 15<=diff_pos:
            victoria+=1
            empate+=1
            derrota+=8
    return(victoria,empate,derrota)

def prediccion_partidos(dataframe,show=True,equipo1='',equipo2=''):
    victoria=0
    empate=0    #Para el equipo local
    derrota=0
    if show:
        local=input('Escriba el elquipo local')
        visitante=input('Escriba el equipo visitante')
    else:
        local=equipo1
        visitante=equipo2
    local=local.upper()  #el dataframe tiene los datos en mayus
    visitante=visitante.upper()
    df= pd.DataFrame(columns=["equipo", "partidos", "goles favor", "goles contra", "per goles favor", 
                                               "per goles contra", "tiros favor", "conversion tiros", "tiros por partido","tiros recibidos","conversion tiros contra","tiros recibidos por partido","racha de 5"])
    eq_loc=dataframe['equipo']==local
    eq_vis=dataframe['equipo']==visitante   #reconocimiento de equipos
    df_equipos=pd.concat([dataframe[eq_loc],dataframe[eq_vis]])  #dataframe de los equipos seleccionados
    goles_par=contador_goles(df_equipos)  #goles
    racha=contador_racha(df_equipos)   #rachas
    #posicion  ----> 25% del total --> 10 puntos
    posicion=contador_posicion(df_equipos)  
    victoria+=posicion[0]
    empate+=posicion[1]      #asignacion de puntos dependiendo de la posicion
    derrota+=posicion[2]
    #racha de partidos ----> 25% del total --> 10 puntos
    racha=contador_racha(df_equipos)   
    if racha[0]==racha[1]:
        victoria+=2
        empate+=6
        derrota+=2
    if racha[0]>racha[1]:
        dif_racha=racha[0]-racha[1]
        sum_vict=dif_racha+(10-dif_racha)//3
        victoria+=sum_vict                       #reparto de probabilidades sobre 10
        empate+=((10-sum_vict)//2)+sum_vict%2
        derrota+=(10-sum_vict)//2
    if racha[0]<racha[1]:
        dif_racha=racha[1]-racha[0]
        sum_vict=dif_racha+(10-dif_racha)//3
        derrota+=sum_vict
        empate+=((10-sum_vict)//2)+sum_vict%2         #reparto de probabilidades sobre 10
        victoria+=(10-sum_vict)//2
    #goles y predicción del resultado ---->50% del total --> 20 puntos
    goles=contador_goles(df_equipos)
    dif_goles=goles[0]-goles[1]
    if dif_goles>0:
        if 0<=dif_goles<0.5:
            victoria+=4
            empate+=12
            derrota+=4
        if 0.5<=dif_goles<1.5:
            victoria+=8
            empate+=7
            derrota+=5
        if 1.5<=dif_goles<2.5:
            victoria+=12
            empate+=5
            derrota+=3
        if 2.5<=dif_goles<3.5:
            victoria+=15
            empate+=3
            derrota+=2
        if 3.5<=dif_goles:
            victoria+=17
            empate+=2
            derrota+=1
    else:
        dif_goles=dif_goles*-1
        if 0<=dif_goles<0.5:
            victoria+=4
            empate+=12
            derrota+=4
        if 0.5<=dif_goles<1.5:
            victoria+=5
            empate+=7
            derrota+=8
        if 1.5<=dif_goles<2.5:
            victoria+=3
            empate+=5
            derrota+=12
        if 2.5<=dif_goles<3.5:
            victoria+=2
            empate+=3
            derrota+=15
        if 3.5<=dif_goles:
            victoria+=1
            empate+=2
            derrota+=17
    probabilidades=(victoria*100/40,empate*100/40,derrota*100/40)
    if show:
        print(f"{local}: {probabilidades[0]}%   EMPATE: {probabilidades[1]}%   {visitante}: {probabilidades[2]}%")
    else:
        return probabilidades


def separador_archivo_futbol(filename):
    lista=[]
    jornada=[]
    espacios=list(string.whitespace)
    puntuacion=list(string.punctuation)  #listas que contienen los espacios y puntuacion
    with open(filename,'r') as file:
        palabra=''
        for line in file:
            for caracter in line:
                if caracter in espacios or caracter in puntuacion:  #separador de palabras
                    if palabra!='':   #no crea espacios vacíos   
                       lista.append(palabra)
                       palabra=''
                else:
                    palabra+=caracter  #añade las letras para formar la palabra
    for i in range(len(lista)-5):
        if lista[i]=='Real' or lista[i]=='Rayo' or lista[i]=='Atletico' or lista[i]=='Athletic':
            lista[i]+=' '+lista[i+1]
            lista.pop(i+1)
    for i in range(10):
        partido=[lista[i],lista[i+1]]
        lista.pop(i+1)
        jornada.append(partido)
    return jornada

def prediccion_jornada(archivo,num_jornada):
    jor= 'Jornada '+str(num_jornada)
    jornada=separador_archivo_futbol(archivo)
    with open(jor,'w') as a:
        for i in range(10):
            prediccion=prediccion_partidos(datos,False,jornada[i][0],jornada[i][1])
            a.write(jornada[i][0]+' vs '+jornada[i][1]+'\n')
            a.write(jornada[i][0]+': '+str(prediccion[0])+'   Empate: '+str(prediccion[1])+'   '+jornada[i][1]+': '+str(prediccion[2])+'\n')
            a.write('\n')
    return 'Archivo preparado'

def filter_data_csv(df: pd.DataFrame):
    try:
        datos_limpio = df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']]
        return datos_limpio
    except: return None