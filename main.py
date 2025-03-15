from turtle import *
import time
import random

# definimos variables globales del juego
ventana = Screen() # objeto ventana
delay = 0.1 # delay con el que se moverá el juego
puntaje = 0
cabeza = Turtle()
comida = Turtle()
tableroPuntaje = Turtle()
colorSerpiente = "green"
segmentos = [] #son las partes del cuerpo de la serpiente
lineaArriba = Turtle()

# Ajustes de la ventana
ventana.title("Snake Game")
ventana.bgcolor("#FDFD96") #amarillo suave
ventana.setup(width=600, height=600)
ventana.tracer(0)

#Definicion de la linea de arriba para separar donde va el marcador y area de juego
lineaArriba.penup() # levanta el lapiz para no trazar de donde a donde se mueve el puntero de turtle
lineaArriba.goto(-300,260)
lineaArriba.pendown()
lineaArriba.pensize(6)
lineaArriba.pencolor("gray")
lineaArriba.forward(600)
lineaArriba.hideturtle()

# ajuste de la cabeza de la serpiente 
cabeza.speed(0)
cabeza.shape("square")
cabeza.color(colorSerpiente)
cabeza.penup()
cabeza.goto(0,0)
cabeza.direction = "stop"

# se crea la comida de del juego
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(100,200)

#tablero de puntuacion 
tableroPuntaje.speed(0)
tableroPuntaje.color("black")
tableroPuntaje.penup()
tableroPuntaje.goto(0,260)
tableroPuntaje.write(f"Puntaje : {puntaje}", align="center", font=("ds-digital",24,"normal"))
tableroPuntaje.hideturtle() #oculta el puntero con el que turtle dibuja.

#label de opcion de salida 
labelSalida = Turtle()
def mostrarLabel():
    labelSalida.speed(0)
    labelSalida.color("black")
    labelSalida.penup()
    labelSalida.goto(-260,275)
    labelSalida.write("[q]= salir", align="center", font=("ds-digital",10,"normal"))
    labelSalida.hideturtle()
mostrarLabel()

# definimos funciones del juego
def haciaArriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"
def haciaAbajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"
def haciaIzquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"
def haciaDerecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"

def movimiento():
    if cabeza.direction == "up":
        eje_y = cabeza.ycor()
        cabeza.sety(eje_y+10)
    elif cabeza.direction == "down":
        eje_y = cabeza.ycor()
        cabeza.sety(eje_y-10)
    elif cabeza.direction == "left":
        eje_x = cabeza.xcor()
        cabeza.setx(eje_x-10)
    elif cabeza.direction == "right":
        eje_x = cabeza.xcor()
        cabeza.setx(eje_x+10)

def reiniciar():
    valoresInicio=[0,0]
    time.sleep(1)
    cabeza.goto(0,0)
    cabeza.direction = "stop"

    #ocultar las partes del cuerpo
    for segmento in segmentos:
        segmento.goto(1000,1000)

    #limpiar los segmentos
    segmentos.clear()

    #reiniciar el puntaje
    puntaje_f = 0 
    valoresInicio[0]=puntaje_f
    #reinciar el delay
    delay_f = 0.1
    valoresInicio[1]=delay_f

    tableroPuntaje.clear()
    return valoresInicio

#funcion que cambia los colores del cuerpo
def colorCuerpo(puntaje):
    if puntaje %2 == 0:
        color = "green"
    else:
        color = "#3ECF72"
    return color

#funcion para subir el nivel con la comida
def comidaUbicacion(puntaje):
    ubicacion = [0,0]
    bordex=[288,-288,-285,285]
    bordey=[238,-288, -285, 235]
    if puntaje>10 and puntaje<30: #modalidad a los bordes
       if (puntaje%2 == 0):
            ubicacion[0]= random.choice(bordex)
            ubicacion[1]=random.randint(-288,238)
       else:
           ubicacion[0]=random.randint(-288,288)
           ubicacion[1]=random.choice(bordey)  
        
    else: #modo normal
        ubicacion[0]=random.randint(-288,288)
        ubicacion[1]=random.randint(-288,238)
    return ubicacion

#funcion que termina la ejecucion del juego
def finJuego():
    global jugando
    var = reiniciar() #se restablecen valores para evitar errores al cerrar
    jugando = False
    ventana.bye() 

# mapeo del teclado
ventana.listen()
ventana.onkeypress(haciaArriba,"Up")
ventana.onkeypress(haciaAbajo,"Down")
ventana.onkeypress(haciaIzquierda,"Left")
ventana.onkeypress(haciaDerecha,"Right")
ventana.onkeypress(finJuego,"q")

jugando = True
# Ciclo del juego
while jugando:
    ventana.update()

    # revisar las coliciones con la paredes
    if cabeza.xcor()>290 or cabeza.xcor()<-290 or cabeza.ycor()>240 or cabeza.ycor()<-290:
        valoresInicio = reiniciar() # se restablecen valores
        puntaje = valoresInicio[0]
        delay = valoresInicio[1]
    
        tableroPuntaje.clear()
        tableroPuntaje.write("puntaje: {}".format(puntaje), align="center", font=("ds-digital",24,"normal"))      
              
#revisar las coliciones con la comida
    if cabeza.distance(comida) <15:
        #se reubica la comida a un punto aleatorio
        ubicaciones = comidaUbicacion(puntaje)
        x = ubicaciones[0]
        y = ubicaciones[1]
        comida.goto(x,y)
        #se crean las partes del cuerpo
        nuevoSegmento = Turtle()
        nuevoSegmento.speed(0)
        nuevoSegmento.shape("square")
        colorSerpiente= colorCuerpo(puntaje)
        nuevoSegmento.color(colorSerpiente)
        nuevoSegmento.penup()
        segmentos.append(nuevoSegmento)

        #acortamos el delay
        delay -= 0.003

        # incrementamos el puntaje
        puntaje += 1
        tableroPuntaje.clear()
        tableroPuntaje.write("puntaje: {}".format(puntaje),align="center", font=("ds-digital",24,"normal"))
    
    # mueve el segmento 0 a la cabeza
    if len(segmentos)>0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x,y)

    # mueve los segmentos en orden inverso
    for index in range(len(segmentos)-1,0,-1):
        x = segmentos[index-1].xcor()
        y = segmentos[index-1].ycor()
        segmentos[index].goto(x,y)
        
    movimiento()

    # revisa por las coliciones con el cuerpo
    for segmento in segmentos:
        if segmento.distance(cabeza)<10:
            valoresInicio = reiniciar() # se restablecen valores
            puntaje = valoresInicio[0]
            delay = valoresInicio[1]
            tableroPuntaje.write("puntaje: {}".format(puntaje), align="center", font=("ds-digital",24,"normal"))
    time.sleep(delay)
    
ventana.mainloop()
