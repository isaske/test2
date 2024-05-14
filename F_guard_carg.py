
# funcion Cargar Variables
def cargar_variables():
  variables = {}
  with open('variables.txt', 'r') as file:
      for line in file:
          # Buscar la primera aparición del signo igual "="
          index = line.find('=')
          # Si se encontró el signo igual
          if index != -1:
              # Separar la línea en clave y valor (todo antes del primer "=" es la clave, el resto es el valor)
              clave = line[:index].strip()
              valor = line[index+1:].strip()
              # Asignar clave y valor al diccionario de variables
              variables[clave] = valor
  return variables

# Función para guardar variables
def guardar_variables(variables):
    # Leer el contenido actual del archivo
    with open('variables.txt', 'r') as file:
        lineas = file.readlines()

    # Modificar la línea que contiene la clave que se va a actualizar
    for i, linea in enumerate(lineas):
        # Separar la línea en clave y valor (maxsplit=1 para evitar cortar valores que contengan "=")
        clave_actual, valor_actual = linea.split("=", maxsplit=1)
        # Si la clave está en el diccionario de variables, actualizar el valor
        if clave_actual.strip() in variables:
            valor_nuevo = variables[clave_actual.strip()]
            # Reemplazar el valor actual con el nuevo valor
            lineas[i] = f"{clave_actual.strip()}={valor_nuevo}\n"

    # Escribir todas las variables nuevamente en el archivo
    with open('variables.txt', 'w') as file:
        for linea in lineas:
            file.write(linea)




# Cargar Variables

variables = cargar_variables()
GlobalAnuncio = (variables['anuncioAuto'])

variables = cargar_variables()
tipstate = bool((variables['autoTipSave']))

if tipstate:
  variables = cargar_variables()
  tipcantidad = (variables['cantidadTipSave'])
  variables = cargar_variables()
  tiptimerestaurar = (variables['tiempoTipSave'])
  tiptime = (variables['tiempoTipSave'])