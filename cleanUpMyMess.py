import glob, os, sys, time
from pprint import pprint
from shutil import copyfile
from pathlib import Path

# USAGE
# ordenarFicherosMasivo.py path [niveles] [ficheros por nivel]
# path: directorio sobre el que se quiere realizar la ordenación
# niveles: niveles de ordenación que se crearan. Por defecto 1
# ficheros por nivel: Si no se recibe este parametro, se creará una carpeta por cada vocal. En caso de recibirlo, se intenta ajustar respetando el numero de ficheros, siempre respetando las letras completas

# Definimos el array que usaremos para iterar en la creación de carpetas

specialChars = [',','\'','=','.','-','_',' ','0','1','2','3','4','5','6','7','8','9']
folderIterator = specialChars.copy() + ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


def orderFolder(path, level):
    
    # Creamos las carpetas
    for folderName in folderIterator:
        
        if folderName in specialChars:
            char = '#'
        else:
            char = folderName
        realFolderName = os.path.join(path,char)
        #searchFiles = os.path.join(path, folderName)
        #No funciona para los numeros. preparar para que si llega el caracter # busque numeros
        
        files = glob.glob(path+os.path.sep+folderName.rjust(level+1,'?')+'*')

        if len(files) > 0:                
            if not os.path.exists(realFolderName):
                os.makedirs(realFolderName)
            for aFile in files:
                if os.path.isdir(aFile):
                    continue
                fileSrcName = Path(aFile).name
                auxSrcFile = os.path.join(path,fileSrcName)
                auxdestFile = os.path.join(realFolderName,fileSrcName)
                copyfile(auxSrcFile,auxdestFile)
                os.remove(auxSrcFile)


#comprobamos que, minimo tiene que venir un argumento
if len(sys.argv) <=1:
    print ("Número de argumentos invalido. Es necesario indicar el path")
    sys.exit(1)
else:
    path = sys.argv[1]
    niveles = 1
    if len(sys.argv) == 3:
        if not sys.argv[2].isnumeric():
            print ("El segundo parámetro debe ser numérico")
            sys.exit(3)
        niveles = int(sys.argv[2])
        if niveles > 3:
            print ("Demasiados subniveles")
            sys.exit(4)

    if os.path.exists(path) == False:
        print("El path no es valido")
        sys.exit(2)
    else:
        localtime = time.asctime( time.localtime(time.time()) )
        print ("Inicio del script: "+localtime)
        vueltas  = 0
        arrPath = [path]
        auxArrPath = []        
        while vueltas < niveles:
            # hacemos los path
            
            for folder in arrPath:  
                orderFolder(folder, vueltas)
                numericDone = False
                for letter in folderIterator:
                    if letter in specialChars:
                        if not numericDone:
                            char = '#'
                        else:
                            continue
                    else:
                        char = letter
                    auxArrPath.append(os.path.join(folder, char))
            arrPath = auxArrPath
            auxArrPath = []   
            vueltas = vueltas +1  
        localtime = time.asctime( time.localtime(time.time()) )
        print ("Fin del script: "+localtime)
        sys.exit(0)