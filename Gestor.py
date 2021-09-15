from Imagen import Imagen
from Celda import Celda
from os import truncate
from tkinter import filedialog, Tk
from tkinter.filedialog import askopenfilename
from tkinter import * 


global texto
class Gestor:
    
    def __init__(self):
        self.Imagen=[]
        
        self.Filtros=[]

    def CargarArchivo(self): 

        global texto 
        Tk().withdraw()
        archivo = filedialog.askopenfile(initialdir="./Archivos Prueba", title="Seleccione un archivo",filetypes=(("Archivos pxla",".pxla"),("ALL files",".txt")))
        if archivo is None:
            print('No se selecciono ni un archivo\n')
            return None
        else:
            texto = archivo.read()
            print(texto)
            print('\n\n')
            texto+='%'
            print(texto)
            archivo.close()
            print("Lectura Exitosa")
            

    def isLetra(self,caracter):
        if((ord(caracter) >= 65 and ord(caracter) <= 90) or (ord(caracter) >= 97 and ord(caracter) <= 122) or ord(caracter) == 164 or ord(caracter) == 165):
            return True
        else:
            return False
    
    def isNumero(self,caracter):
        if ((ord(caracter) >= 48 and ord(caracter) <= 57)):
            return True
        else:
            return False

    def Analizar(self):
        global texto
        tempCelda=[]
        titulo = ""
        ancho = '' 
        alto = ''
        fila = ''
        columna = ''
        poX=''
        poY=''
        valorB = ''
        color= ''
        estado = 0 
        lexema = ""
        
        for x in texto:
            if (estado==0):
                if (self.isLetra(x)==True):
                    lexema += x
                    estado = 1
            elif (estado==1):
               
                if (self.isLetra(x)==True):
                    lexema += x
                elif (x == '='):
                    if ((lexema == "TITULO") or (lexema == "ANCHO") or (lexema == "ALTO") or (lexema == "FILAS") or (lexema == "COLUMNAS") or (lexema == "CELDAS") or (lexema == "FILTROS")):
                        estado = 2          
                    else: 
                        print("Error Lexico, se detecto " + lexema + " en S0 F,C")
            elif (estado == 2 ):
                if (x=='"'):
                    ## como es comilla se establece que se esta tomando el titulo
                    lexema = ""
                    estado = 3
                ## en esta opcion pueden haber 4, alto, ancho, filas o columnas 
                elif(self.isNumero(x)==True):
                    if (lexema == "ANCHO"):
                        atributo = "Ancho"
                        lexema=""
                    elif (lexema == 'ALTO'):
                        atributo="Alto"
                        lexema=""
                    elif (lexema == 'FILAS'):
                        atributo="Filas"
                        lexema=""
                    elif (lexema == 'COLUMNAS'):
                        atributo="Columnas"
                        lexema=""
                    lexema += x
                    estado = 5
                elif (x=='{'):
                    lexema = ""
                    estado = 6
                elif (self.isLetra(x)==True):
                    lexema=''
                    lexema += x
                    estado = 19
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    print("Error Lexico, se detecto " + x + " en S0 F,C")
            ## El estado 3 significa el titulo de la imagen
            elif (estado == 3 ):
                if (self.isLetra(x)==True):
                    lexema += x
                elif(self.isNumero(x)==True):
                    lexema+=x
                ## en la segunda comilla se le aplica el valor a la variable reservada
                elif(x=='"'):
                    titulo= lexema         
                elif (x == ';'):
                    lexema=""
                    estado = 4
                ## se ignora los espacios en blanco entre la comilla y el punto y coma
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    print("Error Lexico, se detecto " + x + " en S0 F,C")    
            elif (estado == 4):
                if self.isLetra(x)==True:
                    lexema += x 
                    estado = 1
            elif (estado == 5):
                if (self.isNumero(x)==True):
                    lexema +=x 
                elif (x == ';'):
                    if(atributo=="Ancho"):
                       ancho=lexema
                    elif(atributo=="Alto"):
                        alto=lexema
                    elif(atributo=="Filas"):
                        fila=lexema
                    elif(atributo=="Columnas"):
                        columna=lexema
                    lexema=""
                    estado = 4 
            ## el estado 6 es la apertura de cada celda
            elif (estado == 6 ): 
                if (x=='['):
                    estado = 7
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            ##el estado 7 es el primer parametro de la celda
            elif (estado == 7 ):
                if (self.isNumero(x)==True):
                    lexema += x
                    estado = 8
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass 
            elif (estado == 8):
                if (self.isNumero(x)):
                  lexema += x  
                elif (x==','):
                    ## se debe enviar el primer dato/parametro de la celda
                    poX=lexema
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 9
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado == 9 ):
                if (self.isNumero(x)==True):
                    lexema += x
                    estado= 10
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado==10):
                if (self.isNumero(x)==True):
                    lexema += x
                elif (x==','):
                     ## se debe enviar el segundo dato/parametro de la celda
                    poY= lexema
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 11
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado == 11):
                if (self.isLetra(x)==True):
                    lexema+=x
                    estado = 12
                ## si es un espacio, tab, o nueva linea, se ignora la iteracion
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            ## El estado 12 es del booleano TRUE or FALSE
            elif (estado ==12):
                if(self.isLetra(x)==True):
                    lexema += x
                elif (x==','):
                    ## se debe enviar el tercer dato/parametro de la celda
                    if lexema == 'TRUE':
                        valorB=True
                    else: 
                        valorB=False
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 13
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            ## EL estado 13 representa el color
            elif (estado == 13):
                if (x=='#'):
                    lexema += x
                    ## se envia al estado 14 para recolectar los caracteres para el color hexadecimal
                    estado=14
            elif (estado == 14):
                if (self.isLetra(x)==True):
                    lexema += x
                    estado = 15
                elif(self.isNumero(x)==True):
                    lexema += x
                    estado = 15
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else: 
                    print("Error Lexico, se detecto " + x + " en S0 F,C")
            elif (estado == 15):
                if (self.isLetra(x)==True):
                    lexema += x    
                elif(self.isNumero(x)==True):
                    lexema += x
                elif (x == ']'):
                    ## se debe enviar el ultimo dato/parametro de la celda
                    color = lexema
                    ##se reinicia el lexema
                    tempCelda.append(Celda(poX,poY,valorB,color))
                    lexema = ""
                    estado = 16
                else: 
                    print("Error Lexico, se detecto " + x + " en S0 F,C")
            elif (estado == 16):
                if (x == ','):
                    
                    estado = 6 
                elif(x=='}'):
                    
                    
                    estado = 17
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado == 17):
                if(x==';'):
                    estado = 18
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado == 18 ):
                if(self.isLetra(x)==True):
                    lexema += x 
                    estado = 1
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass   
            elif (estado==19):
                if(self.isLetra(x)==True):
                    lexema += x
                elif (x==';'):
                    self.Filtros.append(lexema)
                    estado = 20
                    lexema = ''
                elif(x==','):
                    self.Filtros.append(lexema)
                    estado = 21
                    lexema = ''
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif (estado == 20):
                if(x=='@'):
                    
                    lexema+=x
                    estado = 22
                elif (x=='%'):
                    self.Imagen.append(Imagen(titulo,int(ancho),int(alto),int(fila), int(columna),tempCelda,self.Filtros))
                    
                    estado = 23
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
            elif(estado==21):
                if (self.isLetra(x)==True):
                   lexema +=x
                   estado=19
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    print("Error Lexico, se detecto " + x + " en S0 F,C")
            elif(estado==22):
                if(x=='@'):
                    lexema+=x
                elif(self.isLetra(x)==True):
                    lexema=''
                    self.Imagen.append(Imagen(titulo,int(ancho),int(alto),int(fila), int(columna),tempCelda,self.Filtros))
                    tempCelda=[]
                    estado = 1
                    lexema +=x
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
        if (estado==23):
            self.GenerarArchivosPixeles()
            print('Se ejecuto todo el archivo')

    def GenerarArchivosPixeles(self):
        for i in range(0,len(self.Imagen)):    
            filehtml = open("./Reportes/Reporte"+self.Imagen[i].Titulo+".html","w")
            fileCss = open("./Reportes/Reporte"+self.Imagen[i].Titulo+".css","w")
            pixel = ''
            for c in range(int(self.Imagen[i].Filas)*int(self.Imagen[i].Columnas)): 
                pixel += '<div class="pixel"></div>\n\n'
            contenidoHTML=(
              '<!DOCTYPE html>\n'
                ' <html>\n' 
                '<head> \n'
                '<meta charset="utf-8"> \n'
                '<link rel="stylesheet" href="Reporte'+self.Imagen[i].Titulo+'.css">\n'
                '<title>Reporte' +self.Imagen[i].Titulo +'</title>\n'
                '</head>\n' 
                '<body>\n'
                '<div class="canvas">\n'
                +pixel+
                '</div>\n''</body>\n''</html>\n'
            )
            filehtml.write(str(contenidoHTML))
            cssPixel =''
            contador=0
            
            for fila in range(0,self.Imagen[i].Filas):
                for columna in range(0, self.Imagen[i].Columnas):
                    contador+=1
                    for celda in self.Imagen[i].Celda:
                        if(int(celda.x)==fila) and (int(celda.y)==columna):
                            if (celda.valor==True):
                                cssPixel+='\n.pixel:nth-child('+str(contador)+'){\n'+'background:'+str(celda.color)+';\n}\n'
                                
            #num = int(self.Imagen[i].Celda[n].x)*int(self.Imagen[i].Columnas)+int(self.Imagen[i].Celda[j].y) + 1
            ##cssPixel += '.pixel:nth-child('+str(conta)+'){\n'+'background:'+str(self.Imagen[i].Celda[n].color)+';\n}\n'
            print(cssPixel)
            contenidoCSS=(
                ##se le agrega estilo al cuerpo del html
                'body {\n' 
                'background: #333333;      /* Background color de toda la página */\n'
                'height: 100vh;\n'
                'display: flex;            /* Define contenedor flexible */\n'
                'justify-content: center;  /* Centra horizontalmente el lienzo */\n'
                'align-items: center;      /* Centra verticalmente el lienzo */\n' 
                ## cierra el estilo del body
                '}\n\n'
                ##se agrega estilo al lienzo (div clase canvas)
                '.canvas {\n'
                'width:'+str(self.Imagen[i].Ancho)+'px;   /* Ancho del lienzo, se asocia al ANCHO de la entrada */\n'
                'height:'+str(self.Imagen[i].Alto)+'px;  /* Alto del lienzo, se asocia al ALTO de la entrada */\n}\n\n'
                ## CIerra el estilo del lienzo
                ## abre el estilo de los pixeles
                '.pixel {\n'
                ' width:'+str(self.Imagen[i].Ancho/self.Imagen[i].Columnas)+'px;   /* Ancho de cada pixel, se obtiene al operar ANCHO/COLUMNAS (al hablar de pixeles el resultado de la división debe ser un numero entero) */\n'
                'height:'+str(self.Imagen[i].Alto/self.Imagen[i].Filas)+'px;   /* Alto de cada pixel, se obtiene al operar ALTO/FILAS (al hablar de pixeles el resultado de la división debe ser un numero entero) */\n'
                'float: left;\n'
                'box-shadow: 0px 0px 1px #fff; /*Si lo comentan les quita la cuadricula de fondo */\n'
                '}\n\n'
                #cierra el estilo de los pixeles
                +cssPixel
            )       
            
            fileCss.write(str(contenidoCSS))
            
            fileCss.close()
            filehtml.close()
            cssPixel=pixel=''
  
        