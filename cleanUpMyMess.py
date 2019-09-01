from time import asctime,localtime,time
from sys import exit, argv
from os import path, makedirs, remove
from glob import glob
from pprint import pprint
from shutil import copyfile
from pathlib import Path

# USAGE
# ordenarFicherosMasivo.py path [niveles]
# path: directorio sobre el que se quiere realizar la ordenación
# niveles: niveles de ordenación que se crearan. Por defecto 1

# Definimos el array que usaremos para iterar en la creación de carpetas

specialChars = [',','\'','=','.','-','_',' ','0','1','2','3','4','5','6','7','8','9']
folderIterator = specialChars.copy() + ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


def orderFolder(apath, level):
    
    # Creamos las carpetas
    for folderName in folderIterator:
        
        if folderName in specialChars:
            char = '#'
        else:
            char = folderName
        realFolderName = path.join(apath,char)
        files = glob(apath+path.sep+folderName.rjust(level+1,'?')+'*')

        if len(files) > 0:                
            if not path.exists(realFolderName):
                makedirs(realFolderName)
            for aFile in files:
                if path.isdir(aFile):
                    continue
                fileSrcName = Path(aFile).name
                auxSrcFile = path.join(apath,fileSrcName)
                auxdestFile = path.join(realFolderName,fileSrcName)
                try:
                    copyfile(auxSrcFile,auxdestFile)
                    remove(auxSrcFile)
                except PermissionError as pe:
                    print("Permission denied on file "+auxSrcFile+"\n"+str(pe));
                except Exception as e:
                    print("Unknown Exception on file"+auxSrcFile+"\n"+str(e))
                    


#comprobamos que, minimo tiene que venir un argumento
if len(argv) <=1:
    print ("Invalid argument number. Path is mandatory")
    exit(1)
else:
    mypath = argv[1]
    niveles = 1
    if len(argv) == 3:
        if not argv[2].isnumeric():
            print ("Deep argument must be numeric")
            exit(3)
        niveles = int(argv[2])
        if niveles > 3:
            print ("Too many deep")
            exit(4)
        elif niveles < 1:
            print ("Min deep must be 1")
            exit(5)

    if path.exists(mypath) == False:
        print("Invalid path")
        exit(2)
    else:
        mytime = asctime(localtime(time()) )
        print ("Script starts at: "+mytime)
        vueltas  = 0
        arrPath = [mypath]
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
                    auxArrPath.append(path.join(folder, char))
            arrPath = auxArrPath
            auxArrPath = []   
            vueltas = vueltas +1  
        mytime = asctime(localtime(time()))
        print ("Script ends at: "+mytime)
        exit(0)