# Herramienta de tableros para ScrabbleAR
Herramienta para el trabajo final de Python

>La herramienta permite pintar en una matriz de NxN con 8 tipos de ficha distintos y los exporta a un .json que se puede usar de tablero 
en ScrabbleAR contiene un .json donde se encuentran los codigos de color que usa cada ficha para que sea facil de actualizar con los del juego

#### Instrucciones de uso
- Ni bien ejecute el programa vera un menu de dificultad y para seleccionar el tamaño de dicho tablero
- El boton dibujar mostrara la ventana donde puede empezar a crear el tablero y exportarlo
#### Dependencias
- PysimpleGui
- Python 3.8.3

##### Limitaciones
 Como el json del tablero tiene el siguiente formato
 ```
 {
 (0,0) = ""
 (0,1) = ""
 ...
 (0,n) = ""
 (1,0) = ""
 (1,1) = ""
 ...
 (1,n) = ""
 ...
 (n,n) = ""
 }
 ``` 
 Los tableros solo se pueden hacer cuadrados


