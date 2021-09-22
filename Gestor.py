from Token import Token
from Errores import Errores 
from Imagen import Imagen
from Celda import Celda

from tkinter import filedialog, Tk
from tkinter.filedialog import askopenfilename
from tkinter import * 

from graphviz import *

global texto

class Gestor:
    
    def __init__(self):
        self.Imagen=[]
        self.Tokens=[]
        self.Errores=[]

    def CargarArchivo(self): 
        self.Imagen.clear()
        self.Tokens.clear()
        self.Errores.clear()
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
        HayError = False
        tempCelda=[]
        tempFiltros=[]
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
        contadorColumna=0
        contadorFila=1
        for x in texto:
            if(ord(x)==10):
                contadorFila+=1
                contadorColumna=0
            contadorColumna+=1
            
            if (estado==0):
                if (self.isLetra(x)==True):
                    lexema += x
                    estado = 1
            elif (estado==1):
                
                if (self.isLetra(x)==True):
                    lexema += x
                    HayError=False
                elif (x == '='):
                    if ((lexema == "TITULO") or (lexema == "ANCHO") or (lexema == "ALTO") or (lexema == "FILAS") or (lexema == "COLUMNAS") or (lexema == "CELDAS") or (lexema == "FILTROS")):
                        estado = 2          
                    else: 
                        e =('--> Error Lexico, se detecto: ' + lexema + ' en ''Fila: '+str(contadorFila)+' Columna: '+str(contadorColumna)+' favor de revisar')
                        HayError=True
                        lexema=''
                        self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 2 ):
                if (x=='"'):
                    ## como es comilla se establece que se esta tomando el titulo
                    lexema = ''
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
                    e = ('--> Error Lexico, se detecto ' + x +" en  "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+" Solo se permite valores '"', '"{"', '"alfabeticos"', }, numericos,  ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            ## El estado 3 significa el titulo de la imagen
            elif (estado == 3 ):
                if (self.isLetra(x)==True):
                    lexema += x
                elif(self.isNumero(x)==True):
                    lexema+=x
                ## en la segunda comilla se le aplica el valor a la variable reservada
                elif(x=='"'):
                    titulo= lexema
                    col = contadorColumna-len(titulo)
                    self.Tokens.append(Token("Titulo",titulo,contadorFila,col))
                elif (x == ';'):
                    lexema=""
                    estado = 4
                ## se ignora los espacios en blanco entre la comilla y el punto y coma
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en  "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+" Solo se permite valores '"', '"alfabeticos"', numericos, ";" ')    
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
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
                       col = contadorColumna-len(ancho)
                       self.Tokens.append(Token("Ancho",ancho,contadorFila,col))
                    elif(atributo=="Alto"):
                        alto=lexema
                        col = contadorColumna-len(alto)
                        self.Tokens.append(Token('Alto',alto,contadorFila,col))
                    elif(atributo=="Filas"):
                        fila=lexema
                        col = contadorColumna-len(fila)
                        self.Tokens.append(Token('Filas',fila,contadorFila,col))
                    elif(atributo=="Columnas"):
                        columna=lexema
                        col = contadorColumna-len(columna)
                        self.Tokens.append(Token('Columnas',columna,contadorFila,col))
                    else:
                        e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores ";" y numericos  ')    
                        HayError=True
                        lexema=''
                        self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
                    lexema=""
                    estado = 4 
            ## el estado 6 es la apertura de cada celda
            elif (estado == 6 ): 
                if (x=='['):
                    estado = 7
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "["')
                    HayError=True
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            ##el estado 7 es el primer parametro de la celda
            elif (estado == 7 ):
                if (self.isNumero(x)==True):
                    lexema += x
                    estado = 8
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores numericos')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e)) 
            elif (estado == 8):
                if (self.isNumero(x)):
                  lexema += x  
                elif (x==','):
                    ## se debe enviar el primer dato/parametro de la celda
                    poX=lexema
                    col = contadorColumna-len(poX) 
                    self.Tokens.append(Token('X',poX,contadorFila,col))
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 9
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "," y numericos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 9 ):
                if (self.isNumero(x)==True):
                    lexema += x
                    estado= 10
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else: 
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "," y numericos ')
                    HayError=True
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado==10):
                if (self.isNumero(x)==True):
                    lexema += x
                elif (x==','):
                     ## se debe enviar el segundo dato/parametro de la celda
                    poY= lexema
                    col = contadorColumna-len(poY)
                    self.Tokens.append(Token('Y',poY,contadorFila,col))
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 11
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "," y valores tipo numericos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 11):
                if (self.isLetra(x)==True):
                    lexema+=x
                    estado = 12
                ## si es un espacio, tab, o nueva linea, se ignora la iteracion
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "," y valores tipo "TRUE" O "FALSE" ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            ## El estado 12 es del booleano TRUE or FALSE
            elif (estado ==12):
                if(self.isLetra(x)==True):
                    lexema += x
                elif (x==','):
                    ## se debe enviar el tercer dato/parametro de la celda
                    if lexema == 'TRUE':
                        valorB=True
                        col = contadorColumna-4
                        self.Tokens.append(Token('ValorBool','TRUE',contadorFila,col))
                    else: 
                        valorB=False
                        col = contadorColumna-5
                        self.Tokens.append(Token('ValorBool','FALSE',contadorFila,col))
                    ##se reinicia el lexema
                    lexema = ""
                    estado = 13
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else: 
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "," y valores tipo alfabeticos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            ## EL estado 13 representa el color
            elif (estado == 13):
                if (x=='#'):
                    lexema += x
                    ## se envia al estado 14 para recolectar los caracteres para el color hexadecimal
                    estado=14
                else: 
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite el valor de "#" ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
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
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores numericos y alfabeticos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 15):
                if (self.isLetra(x)==True):
                    lexema += x    
                elif(self.isNumero(x)==True):
                    lexema += x
                elif (x == ']'):
                    ## se debe enviar el ultimo dato/parametro de la celda
                    color = lexema
                    col = contadorColumna-len(color)
                    self.Tokens.append(Token('Color',color,contadorFila,col))
                    ##se reinicia el lexema
                    tempCelda.append(Celda(poX,poY,valorB,color))
                    lexema = ""
                    estado = 16
                else: 
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores "]" numericos y alfabeticos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 16):
                if (x == ','):
                    estado = 6 
                elif(x=='}'):
                   estado = 17
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +"en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores "," o "}"')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
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
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores alfabeticos ')   
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado==19):
                if(self.isLetra(x)==True):
                    lexema += x
                elif (x==';'):
                    if (lexema=="MIRRORX" or lexema == "MIRRORY" or lexema=='DOUBLEMIRROR'):
                        tempFiltros.append(lexema)
                        col = contadorColumna-len(lexema)
                        self.Tokens.append(Token('Filtro',lexema,contadorFila,col))
                    else: 
                        e =('--> Error Lexico, se detecto ' + lexema +" en Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores alfabeticos, "," y ";" ')
                        HayError=True
                        lexema=''
                        self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))

                    estado = 20
                    lexema = ''
                elif(x==','):
                    if (lexema=="MIRRORX" or lexema == "MIRRORY" or lexema=='DOUBLEMIRROR'):
                        tempFiltros.append(lexema)
                        col = contadorColumna-len(lexema)
                        self.Tokens.append(Token('Filtro',lexema,contadorFila,col))
                    else: 
                        e =('--> Error Lexico, se detecto ' + lexema +" en Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores alfabeticos, "," y ";" ')
                        HayError=True
                        lexema=''
                        self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
                        
                    estado = 21
                    lexema = ''
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores alfabeticos, "," y ";" ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif (estado == 20):
                if(x=='@'):
                    contadorArroba=1
                    lexema+=x
                    estado = 22
                elif (x=='%'):
                    self.Imagen.append(Imagen(titulo,int(ancho),int(alto),int(fila), int(columna),tempCelda,tempFiltros))
                    estado = 23
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores "@" y "%" ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif(estado==21):
                if (self.isLetra(x)==True):
                   lexema +=x
                   estado=19
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+"Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores valores alfabeticos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
            elif(estado==22):
                
                if(x=='@' and contadorArroba<4):
                    contadorArroba+=1
                    lexema+=x
                elif(self.isLetra(x)==True):
                    
                    if(HayError==False and lexema=='@@@@'):
                        self.Imagen.append(Imagen(titulo,int(ancho),int(alto),int(fila), int(columna),tempCelda,tempFiltros))
                        lexema=''
                        estado=1
                    else: 
                        print("La anterior imagen no se genera")
                        lexema=''
                        estado=1
                        lexema=''
                    tempCelda=[]
                    tempFiltros=[]
                    estado = 1
                    lexema+=x
                elif ord(x) == 32 or ord(x) == 10 or ord(x) == 9: 
                    pass
                elif (x=='@' and contadorArroba>=4):
                    e =('--> Error Lexico, se detecto ' + x +" en "+" Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite 4 valores de "@" ')
                    HayError=True
                    
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
                elif(self.isLetra(x)==True and contadorArroba>=4):
                    lexema=''
                    estado=1
                    lexema+=x
                else:
                    e =('--> Error Lexico, se detecto ' + x +" en "+" Fila: "+str(contadorFila)+" Columna: "+str(contadorColumna)+' Solo se permite valores de "@" y alfabeticos ')
                    HayError=True
                    lexema=''
                    self.Errores.append(Errores(str(contadorFila), str(contadorColumna), e))
        if (estado==23):
            if HayError==False:
                self.GenerarArchivosPixeles()
            else:
                 print('La imagen final no se genero')
        
    def GenerarArchivosPixeles(self):
        for i in range(0,len(self.Imagen)):    
            filehtml = open("./Htmls/"+self.Imagen[i].Titulo+".html","w")
            fileCss = open("./Htmls/css/"+self.Imagen[i].Titulo+".css","w")
            pixel = ''
            for c in range(int(self.Imagen[i].Filas)*int(self.Imagen[i].Columnas)): 
                pixel += '<div class="pixel"></div>\n\n'
            contenidoHTML=(
              '<!DOCTYPE html>\n'
                ' <html>\n' 
                '<head> \n'
                '<meta charset="utf-8"> \n'
                '<link rel="stylesheet" href="css/'+self.Imagen[i].Titulo+'.css">\n'
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
            AlmacenarGrafica=''
            AlmacenarGrafica+='<\n<TABLE cellspacing="0" cellpadding="10">\n'
            celdaExiste=False
            for fila in range(0,self.Imagen[i].Filas):
                AlmacenarGrafica+='<TR>'
                for columna in range(0, self.Imagen[i].Columnas):
                    contador+=1
                    for celda in self.Imagen[i].Celda:
                        if(int(celda.x)==columna) and (int(celda.y)==fila):
                            celdaExiste=True
                            if (celda.valor==True):
                                AlmacenarGrafica+='<TD bgcolor="'+celda.color+'"></TD>\n'
                                cssPixel+='\n.pixel:nth-child('+str(contador)+'){\n'+'background:'+str(celda.color)+';\n}\n'
                            else:
                                AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                    if(celdaExiste==False):
                        AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                    celdaExiste=False
                AlmacenarGrafica+='</TR>\n'            
            AlmacenarGrafica+='</TABLE>>'
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
            self.GenerarPNG(self.Imagen[i].Titulo,str(AlmacenarGrafica))


        ##Generamos los html de los filtros
        self.HtmlFiltros()
        print("Ver filtros")

    def HtmlFiltros(self):
        for i in range(0,len(self.Imagen)):
            for j in range(0,len(self.Imagen[i].Filtros)):
                fileHtml= open("./Htmls/"+self.Imagen[i].Titulo+" "+self.Imagen[i].Filtros[j]+".html","w")
                fileCss = open("./Htmls/css/"+self.Imagen[i].Titulo+" "+self.Imagen[i].Filtros[j]+".css","w")
                pixel = ''
                for c in range(int(self.Imagen[i].Filas)*int(self.Imagen[i].Columnas)): 
                    pixel += '<div class="pixel"></div>\n\n'
                contenidoHTML=(
                '<!DOCTYPE html>\n'
                ' <html>\n' 
                '<head> \n'
                '<meta charset="utf-8"> \n'
                '<link rel="stylesheet" href="css/'+self.Imagen[i].Titulo+" "+self.Imagen[i].Filtros[j]+'.css">\n'
                '<title>Reporte' +self.Imagen[i].Titulo +'</title>\n'
                '</head>\n' 
                '<body>\n'
                '<div class="canvas">\n'
                +pixel+
                '</div>\n''</body>\n''</html>\n'
            )
                fileHtml.write(str(contenidoHTML))
                cssPixel =''
                contador=0
                AlmacenarGrafica=''
                AlmacenarGrafica+='<\n<TABLE cellspacing="0" cellpadding="10">\n'
                celdaExiste=False
                if(self.Imagen[i].Filtros[j]=="MIRRORX"):
                    for fila in range(0,self.Imagen[i].Filas):
                        AlmacenarGrafica+='<TR>'
                        for columna in range((self.Imagen[i].Columnas)-1,-1,-1):
                            contador+=1
                            for celda in self.Imagen[i].Celda:
                                if(int(celda.y)==fila) and (int(celda.x)==columna):
                                    celdaExiste=True
                                    if (celda.valor==True):
                                        AlmacenarGrafica+='<TD bgcolor="'+celda.color+'"></TD>\n'
                                        cssPixel+='\n.pixel:nth-child('+str(contador)+'){\n'+'background:'+str(celda.color)+';\n}\n'
                                    else:
                                        AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            if(celdaExiste==False):
                                AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            celdaExiste=False
                        AlmacenarGrafica+='</TR>\n'            
                    AlmacenarGrafica+='</TABLE>>'    

                elif(self.Imagen[i].Filtros[j]=="MIRRORY"):
                    for fila in range(self.Imagen[i].Filas-1,-1,-1):
                        AlmacenarGrafica+='<TR>'
                        for columna in range(0,self.Imagen[i].Columnas):
                            contador+=1
                            for celda in self.Imagen[i].Celda:
                                if(int(celda.y)==fila) and (int(celda.x)==columna):
                                    celdaExiste=True
                                    if (celda.valor==True):
                                        AlmacenarGrafica+='<TD bgcolor="'+celda.color+'"></TD>\n'
                                        cssPixel+='\n.pixel:nth-child('+str(contador)+'){\n'+'background:'+str(celda.color)+';\n}\n'
                                    else:
                                        AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            if(celdaExiste==False):
                                AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            celdaExiste=False
                        AlmacenarGrafica+='</TR>\n'            
                    AlmacenarGrafica+='</TABLE>>'

                elif(self.Imagen[i].Filtros[j]=="DOUBLEMIRROR"):
                    for fila in range(self.Imagen[i].Filas-1,-1,-1):
                        AlmacenarGrafica+='<TR>'
                        for columna in range(self.Imagen[i].Columnas-1,-1,-1):
                            contador+=1
                            for celda in self.Imagen[i].Celda:
                                if(int(celda.y)==fila) and (int(celda.x)==columna):
                                    celdaExiste=True
                                    if (celda.valor==True):
                                        AlmacenarGrafica+='<TD bgcolor="'+celda.color+'"></TD>\n'
                                        cssPixel+='\n.pixel:nth-child('+str(contador)+'){\n'+'background:'+str(celda.color)+';\n}\n'
                                    else:
                                        AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            if(celdaExiste==False):
                                AlmacenarGrafica+='<TD bgcolor="#ffffff"></TD>\n'
                            celdaExiste=False
                        AlmacenarGrafica+='</TR>\n'            
                    AlmacenarGrafica+='</TABLE>>'
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
                fileHtml.close()
                cssPixel=pixel=''
                self.GenerarPNG(self.Imagen[i].Titulo+""+self.Imagen[i].Filtros[j],str(AlmacenarGrafica))
   
    def GenerarPNG(self,titulo,texto):
        Ima = Digraph(format='png')
        Ima.node(titulo,label=texto,color='white')
        Ima.render('Imagenes/'+titulo)

    def ReporteToken(self):
        Archivo = open("./Reportes/Tokens.html",'w')
        contenidoTabla = ''
        count=0
        for i in range(len(self.Tokens)):
            contenidoTabla+='<tr><th scope="row">'+str(i+1)+'</th>\n'
            contenidoTabla+='<td>'+self.Tokens[i].token+'</td>\n'
            contenidoTabla+='<td>'+self.Tokens[i].lexema+'</td>\n'
            contenidoTabla+='<td>'+str(self.Tokens[i].Fila)+'</td>\n'
            contenidoTabla+='<td>'+str(self.Tokens[i].Columna)+'</td>\n</tr>'

        contenidoHTML=(
              '<!DOCTYPE html>\n'
                ' <html>\n' 
                '<head> \n'
                '<meta charset="utf-8"> \n'
                '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">\n'
                '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">\n'
                '<link rel="stylesheet" type="text/css" href="./css/bootstrap.css">\n'
                '<link rel="stylesheet" type="text/css"  href="css/Style.css">'
                '<title>Reporte de Tokens' '</title>\n'
                '</head>\n' 
                '<body>\n'
                '<div class="container-fluid welcome-page" id="home">\n'
                '   <div class="jumbotron">\n'
                '       <h1>\n <span>\nTokens\n</span>\n </h1>\n<p>Reporte con todos los tokens, lexemas, sus fila y sus columna</p>\n'
                '</div>'
                '</div>'
                '<div class="container-fluid " ><div class="jumbotron">'
                '<table class="table table-responsive">\n'
                '   <thead>\n'
                        '<tr>\n'
                            '<th scope="col">#</th>\n'
                            '<th scope="col">Token</th>\n'
                            '<th scope="col">Lexema</th>\n'
                            '<th scope="col">Fila</th>\n'
                            '<th scope="col">Columna</th>\n'
                        '</tr>\n'
                    '</thead>\n'
                    '<tbody>\n'
                    +contenidoTabla+
                    '</tbody>\n'
                    '</table>'   
                    '</div>'
                '</div>\n''</body>\n''</html>\n'
            )
        Archivo.write(contenidoHTML)
        Archivo.close()

    def ReporteErrores(self):
        Archivo = open("./Reportes/Errores.html",'w')
        contenidoTabla = ''
        count=0
        for i in range(len(self.Errores)):
            contenidoTabla+='<tr><th scope="row">'+str(i+1)+'</th>\n'
            contenidoTabla+='<td style="color:blue;">'+self.Errores[i].Fila+'</td>\n'
            contenidoTabla+='<td style="color:blue;">'+self.Errores[i].Columna+'</td>\n'
            contenidoTabla+='<td style="color:red;">'+str(self.Errores[i].Descripcion)+'</td>\n'

        contenidoHTML=(
              '<!DOCTYPE html>\n'
                ' <html>\n' 
                '<head> \n'
                '<meta charset="utf-8"> \n'
                '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">\n'
                '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">\n'
                '<link rel="stylesheet" type="text/css" href="./css/bootstrap.css">\n'
                '<link rel="stylesheet" type="text/css"  href="css/Style.css">'
                '<title>Reporte de Errores' '</title>\n'
                '</head>\n' 
                '<body>\n'
                '<div class="container-fluid welcome-page" id="home">\n'
                '   <div class="jumbotron">\n'
                '       <h1>\n <span>Tabla de Errores\n</span>\n </h1>\n<p>Reporte con todos los Errores, sus filas y sus columnas</p>\n'
                '</div>'
                '</div>'
                '<div class="container-fluid " ><div class="jumbotron">'
                '<table class="table table-responsive">\n'
                '   <thead>\n'
                        '<tr>\n'
                            '<th scope="col">#</th>\n'
                            '<th scope="col">Fila</th>\n'
                            '<th scope="col">Columna</th>\n'
                            '<th scope="col">Descripcion</th>\n'
                        '</tr>\n'
                    '</thead>\n'
                    '<tbody>\n'
                    +contenidoTabla+
                    '</tbody>\n'
                    '</table>'   
                    '</div>'
                '</div>\n''</body>\n''</html>\n'
            )
        Archivo.write(contenidoHTML)
        Archivo.close()

        