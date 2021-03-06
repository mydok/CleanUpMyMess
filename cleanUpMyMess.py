from time import asctime,localtime,time
from sys import exit, argv
from os import path, makedirs, remove
from glob import glob
from pprint import pprint
from shutil import copyfile, move
from pathlib import Path

# USAGE
# ordenarFicherosMasivo.py path [levels]
# path: directorio sobre el que se quiere realizar la ordenación
# levels: niveles de ordenación que se crearan. Por defecto 1
# startAt: caracter del nombre por el cual empezará la busqueda. Por defecto 0

# Definimos el array que usaremos para iterar en la creación de carpetas

specialChars = [',','\'','=','.','-','_',' ','0','1','2','3','4','5','6','7','8','9']
folderIterator = specialChars.copy() + ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def getSublevelPath(level, char, apath):
    finalFolder = ''
    # Comprobamos si es el primer nivel. Si no lo es, concatenamos los nombres de
    # las carpetas padres
    if level > 0:                
        loop = level
        
        apathList = apath.split(path.sep)
        apathList.reverse()
    
        finalFolder += apathList[0]                  
        
    finalFolder += char      
    return finalFolder

def orderFolder(apath, level, startAt=0):  

    # Creamos las carpetas
    for folderName in folderIterator:  
        
        if folderName in specialChars:
            char = '#'
        else:
            char = folderName
        
        files = glob(apath+path.sep+folderName.rjust(level+startAt+1,'?')+'*')

        if len(files) > 0:    
            finalFolder = getSublevelPath(level,char,apath)
            realFolderName = path.join(apath,finalFolder)
            if not path.exists(realFolderName):
                makedirs(realFolderName)
            for aFile in files:
                if path.isdir(aFile):
                    continue
                fileSrcName = Path(aFile).name
                auxSrcFile = path.join(apath,fileSrcName)
                auxdestFile = path.join(realFolderName,fileSrcName)
                try:
                    #copyfile(auxSrcFile,auxdestFile)
                    #remove(auxSrcFile)
                    move(auxSrcFile,auxdestFile)
                except PermissionError as pe:
                    print("Permission denied on file "+auxSrcFile+"\n"+str(pe))
                except Exception as e:
                    print("Unknown Exception on file"+auxSrcFile+"\n"+str(e))
                    


#comprobamos que, minimo tiene que venir un argumento
if len(argv) <=1:
    print ("Invalid argument number. Path is mandatory")
    exit(1)
else:
    mypath = argv[1]
    levels = 1
    forceLevelNo = 0
    if len(argv) >= 3:
        if not argv[2].isnumeric():
            print ("Deep argument must be numeric")
            exit(3)
        levels = int(argv[2])
        if levels > 3:
            print ("Too many deep")
            exit(4)
        elif levels < 1:
            print ("Min deep must be 1")
            exit(5)
    if len(argv) >= 4:
        if not argv[3].isnumeric():
            print ("Start char argument must be numeric")
            exit(6)
        if int(argv[3]) < 1 and int(argv[3]) > 3:
            print ("Start char argument must be between 1 and 3")
            exit(7)        
        forceLevelNo = int(argv[2])

    if path.exists(mypath) == False:
        print("Invalid path")
        exit(2)
    else:
        mytime = asctime(localtime(time()) )
        print ("Script starts at: "+mytime)
        loops  = 0
        arrPath = [mypath]
        auxArrPath = []        
        while loops < levels:
            # hacemos los path
            
            for folder in arrPath:  
                orderFolder(folder, loops, forceLevelNo)
                numericDone = False
                for letter in folderIterator:
                    if letter in specialChars:
                        if not numericDone:
                            char = '#'
                        else:
                            continue
                    else:
                        char = letter
                    char = getSublevelPath(loops,char,folder)
                    auxArrPath.append(path.join(folder, char))
            arrPath = auxArrPath
            auxArrPath = []   
            loops = loops +1  
        mytime = asctime(localtime(time()))
        print ("Script ends at: "+mytime)
        exit(0)