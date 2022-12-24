import PySimpleGUI as sg
import pandas as pd
from lib_modelo import *

#INTERFAZ GRÁFICA
predicted_data = pd.DataFrame()
sg.theme('DarkAmber')

#Inicio de la ventana
layout = [[sg.Text('Equipo local')], 
                 [sg.InputText()],
                 [sg.Text('Equipo visitante')], 
                 [sg.InputText()],      
                 [sg.Submit(),sg.Button('Borrar'),sg.Button('Ver predicciones'),sg.Exit()]]   
      
window = sg.Window('Predicción futbol', layout)

def clear_inputs():
    for key, element in window.key_dict.items():
        if isinstance(element, sg.Input):
            element.update('')
    
#Loop principal
while True:
    try:
        event, values = window.read() 
        equipos=tuple([v for v in values.values()])  

        if event == 'Submit':
            try: 
                predicted_data[(equipos[0],equipos[1])] = prediccion_partidos(datos,show=False, equipo1 = equipos[0], equipo2 = equipos[1])
                sg.popup(f'{equipos[0]}: {prediccion_partidos(datos,show=False, equipo1 = equipos[0], equipo2 = equipos[1])[0]}%, Empate: {prediccion_partidos(datos,show=False, equipo1 = equipos[0], equipo2 = equipos[1])[1]}%, {equipos[1]}: {prediccion_partidos(datos,show=False, equipo1 = equipos[0], equipo2 = equipos[1])[2]}%')
            except: sg.popup('Argumentos inválidos')

        if event == 'Ver predicciones':
            try:
                if len(predicted_data) == 0: raise ValueError
                lay_preds = [[sg.Text(f'{element}: {prediccion_partidos(datos,show=False, equipo1 = equipos[0], equipo2 = equipos[1])}')] for element in predicted_data]
                window = sg.Window('Predicciones realizadas',lay_preds)
            except: sg.popup('Imposible realizar la operación')

        if event == 'Borrar':
            clear_inputs()

        if event == 'Exit':
            window.close()

    except: break

