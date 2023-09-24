#!/usr/bin/env python

import asyncio
import websockets
import json
import os
from datetime import date

DirectorioAMover = None
async def hello(websocket):
    print("Me esty ejecutando")
    Datos = await websocket.recv()
    properties = ""
    ListaDatos = Datos.split("|")
    print(ListaDatos)
    if ListaDatos[-1] == 'CRA':
        
        add_item(ListaDatos[3], ListaDatos[0], ListaDatos[1], "file",int(ListaDatos[4]), ListaDatos[2])
    elif ListaDatos[-1] == 'CRD':
        #['User2.json', 'local', 'Documentos', 'local/Documentos', 'directory', '', '0CRD']
        add_item_directory(ListaDatos[0], ListaDatos[1], ListaDatos[2],ListaDatos[3] ,ListaDatos[4],0 ,content=None)
        
    elif ListaDatos[-1] == 'MOV':
        #['User2.json', 'local/Documentos/Videos', 'Archivo4.txt', 'local/Documentos/Videos', 'MOV']
            MoverArchivo(ListaDatos[0],ListaDatos[1],ListaDatos[2],ListaDatos[3])

    elif ListaDatos[-1] == 'ElIMN':
        delete_Normal(ListaDatos[0],ListaDatos[1],ListaDatos[2])
        
    elif ListaDatos[-1] == 'ElIMD':
        eliminar_directorio(ListaDatos[1],ListaDatos[0])

    elif ListaDatos[-1] == 'MOVDIR':
        Datos = ListaDatos[1]
        DatosSplit = Datos.split("/")
        item_name = DatosSplit[-1]
        
        MoverDirectorio(ListaDatos[0], ListaDatos[1], item_name, ListaDatos[2])
        eliminar_directorio(ListaDatos[1],ListaDatos[0])
        #actualizaRutasDirectorio(filename,path,NuevoDir,item_name)
    elif ListaDatos[-1] == 'PROP':
        properties = get_properties(ListaDatos[0], ListaDatos[1], ListaDatos[2])
        print(properties)

    elif ListaDatos[-1] == 'MOD':
        modify_file(ListaDatos[0], ListaDatos[1], ListaDatos[2], ListaDatos[3])

    elif ListaDatos[-1] == 'CONTENT':
        properties = get_content(ListaDatos[0], ListaDatos[1], ListaDatos[2])

    elif ListaDatos[-1] == 'DOWN':
        
        download(ListaDatos[0], ListaDatos[1], ListaDatos[2],ListaDatos[3])
    elif ListaDatos[-1] == 'DOWND':
        
        download_directorio(ListaDatos[0], ListaDatos[2], ListaDatos[1],ListaDatos[3])

    elif ListaDatos[-1] == 'COPVIR':
        #['User2.json', 'local/Documentos/Videos', 'Archivo4.txt', 'local/Documentos/Videos', 'MOV']
        CopiarArchivoVirtual(ListaDatos[0],ListaDatos[1],ListaDatos[2],ListaDatos[3])

    elif ListaDatos[-1] == 'LOAD':
        #['User2.json', 'local/Documentos/Videos', 'Archivo4.txt', 'local/Documentos/Videos', 'MOV']
        Load(ListaDatos[0],ListaDatos[2],ListaDatos[1])
    elif ListaDatos[-1] == 'LOADD':
        #['User2.json', 'local/Documentos/Videos', 'Archivo4.txt', 'local/Documentos/Videos', 'MOV']
        Load_Directorio(ListaDatos[0],ListaDatos[2],ListaDatos[1])
        
    elif ListaDatos[-1] == 'SHAREDIR':
        
        Datos = ListaDatos[2]
        DatosSplit = Datos.split("/")
        item_name = DatosSplit[-1]
        
        ShareDirectorio(ListaDatos[0], ListaDatos[2], item_name, "compartido",ListaDatos[1] + ".json")
    elif ListaDatos[-1] == 'COPDIR':
        Datos = ListaDatos[1]
        DatosSplit = Datos.split("/")
        item_name = DatosSplit[-1]
        MoverDirectorio(ListaDatos[0], ListaDatos[1], item_name, ListaDatos[2])
    elif ListaDatos[-1] == 'SH':
        share_file(ListaDatos[0], ListaDatos[1], ListaDatos[2], ListaDatos[3])
        
        
    if properties == "":
        greeting = "No hay propiedades"
        await websocket.send(greeting)
    else:
        greeting = properties
        await websocket.send(greeting)
    print(f">>> {greeting}")
        

    

def MoverArchivo(filename,path,item_name,NuevoDir):
    contenido_borrado = ""
    Content = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if item_name in current_dir:
        contenido_borrado = current_dir[item_name]["content"]
        Content = contenido_borrado
        del current_dir[item_name]
    
    
    with open(filename, "w") as file:
        
        json.dump(filesystem, file)
    add_item(filename, NuevoDir, item_name,"file",len(Content),Content)

   # print(contenido_borrado)


def CopiarArchivoVirtual(filename,path,item_name,NuevoDir):
    contenido_borrado = ""
    Content = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if item_name in current_dir:
        contenido_borrado = current_dir[item_name]["content"]
        Content = contenido_borrado
        
    
    
    with open(filename, "w") as file:
        
        json.dump(filesystem, file)
    add_item(filename, NuevoDir, item_name,"file",len(Content),Content)

#----------------------------------------------------------------------------------------------------------    
def MoverDirectorio(filename, path, item_name, NuevoDir):
    contenido_borrado = ""
    Content = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]


    MoverDirectorioAux(filename,NuevoDir,NuevoDir + "/" + item_name, item_name,"directory",0 ,current_dir)

def ShareDirectorio(filename, path, item_name, NuevoDir,UsuarioCompartir):
    contenido_borrado = ""
    Content = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]


    MoverDirectorioAux(UsuarioCompartir,NuevoDir,NuevoDir + "/" + item_name, item_name,"directory",0 ,current_dir)
    


def MoverDirectorioAux(filename, path,pathDir ,item_name,item_type,tamaño ,content):

    filesystem = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    current_dir[item_name] = {
        "type": item_type,
        "tamano":tamaño,
        "path":pathDir,
        "content":content
    }
    with open(filename, "w") as file:
        json.dump(filesystem, file)

    actualizaRutasDirectorio(filename,pathDir,item_name)



def actualizaRutasDirectorio(filename, path, item_name):
    filesystem =""
    with open(filename, "r") as file:
        filesystem = json.load(file)
        
    actualizaRutasDirectorio_aux(filesystem,path, item_name)

    with open(filename, "w") as file:
        json.dump(filesystem, file)
    
def actualizaRutasDirectorio_aux(filesystem,path, item_name):
    
    
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]

    for key, value in current_dir.items():
        if value["type"] == "file":
            value["path"] = path

        if value["type"] == "directory":
            PathViejo = value["path"]
            PathViejoLista = PathViejo.split("/")
            PathViejo = PathViejoLista[-1]
            PathNuevo = path + "/" + PathViejo
            value["path"] = PathNuevo

      
            # Llamada recursiva para actualizar las rutas de los archivos dentro del directorio
            actualizaRutasDirectorio_aux(filesystem, value["path"], item_name)
   
def download_directorio(filename, path,NombreDirectorio,NuevaRutaReal):

    filesystem =""
    with open(filename, "r") as file:
        filesystem = json.load(file)

        
    directorio = NombreDirectorio
    # Ruta completa del directorio
    ruta_directorio = os.path.join(NuevaRutaReal, directorio)
    
    CreaDirectorio(ruta_directorio)
    
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]

    for key, value in current_dir.items():
        
        if value["type"] == "file":
            ruta_directorio = ruta_directorio.replace("\\", "/")
            AñadirArchivo(key,ruta_directorio,value["content"])
            

def CreaDirectorio(Ruta):
    if not os.path.exists(Ruta):
        os.mkdir(Ruta)


    else:
        print("ya existe.")

def AñadirArchivo(Nombre,ruta,contenido):
    nombre_archivo = Nombre
    ruta = r'C:/Users/josue/Desktop/Videos'
    file = open(r'C:/Users/josue/Desktop/Videos', "w")
    file.write(Contenido + os.linesep)
    file.close()
    # Crear el archivo
    
#-------------------------------------------------------------------------------------------------------------------------------------
    
def eliminar_directorio(directorio, filename):
    with open(filename, "r") as file:
        estructura = json.load(file)

    directorios = directorio.split("/")
    eliminar_recursivo(directorios, estructura)

    with open(filename, "w") as file:
        json.dump(estructura, file, indent=4)

def eliminar_recursivo(directorios, estructura):
    global DirectorioAMover
    if len(directorios) == 1:
        directorio_actual = directorios[0]
        if directorio_actual in estructura:
            if estructura[directorio_actual]["type"] == "directory":
                DirectorioAMover = estructura[directorio_actual]
                del estructura[directorio_actual]
                print(f"Directorio {directorio_actual} eliminado correctamente.")
            else:
                print(f"{directorio_actual} no es un directorio.")
        else:
            print(f"{directorio_actual} no existe.")
    else:
        directorio_actual = directorios[0]
        if directorio_actual in estructura:
            if estructura[directorio_actual]["type"] == "directory":
                eliminar_recursivo(directorios[1:], estructura[directorio_actual].get("content", {}))
            else:
                print(f"{directorio_actual} no es un directorio.")
        else:
            print(f"{directorio_actual} no existe.")

   
    
def delete_Normal(filename,path,item_name):
    
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if item_name in current_dir:
        
        del current_dir[item_name]
    
    
    with open(filename, "w") as file:
        
        json.dump(filesystem, file)
    
    

def Load(User,archivo_ruta,RutaDelArchivoEnDrive):

    archivo = open(archivo_ruta, "r") 
    datos = archivo.read()

    nombre_archivo = os.path.basename(archivo_ruta)
    add_item(User, RutaDelArchivoEnDrive,nombre_archivo,"file",len(datos), datos)

def Load_Directorio(User,archivo_ruta,RutaDelArchivoEnDrive):
    directorio = archivo_ruta  # Reemplaza "ruta_del_directorio" con la ruta real del directorio
    nombre_directorio_or = os.path.basename(directorio)

    archivos_txt = []
    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(directorio, archivo)
            with open(ruta_archivo, "r") as file:
                contenido = file.read()
                archivos_txt.append((archivo, contenido))
                
    add_item_directory(User, RutaDelArchivoEnDrive, nombre_directorio_or,RutaDelArchivoEnDrive + "/" + nombre_directorio_or ,"directory",0)          
    for archivo, contenido in archivos_txt:
        add_item(User,RutaDelArchivoEnDrive + "/" + nombre_directorio_or , archivo, "file",len(contenido), contenido)
        
    for archivo in os.listdir(directorio):
        ruta_directorio= os.path.join(directorio, archivo)
        nombre_directorio = os.path.basename(ruta_directorio)
        if os.path.isdir(ruta_directorio):
            Load_Directorio(User,archivo_ruta + "/" + nombre_directorio,RutaDelArchivoEnDrive + "/" + nombre_directorio_or)

#_________________________________________________________________________________________
def add_item(filename, path, item_name, item_type,tamaño, content=None):
    filesystem = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    current_dir[item_name] = {
        "type": item_type,
        "path":path,
        "current-date": str(date.today()),
        "modified-date": str(date.today()),
        "tamano":tamaño,
        "content": content if item_type == "file" else {}
    }
    with open(filename, "w") as file:
        json.dump(filesystem, file)
##        
def add_item_directory(filename, path, item_name,pathDir ,item_type,tamaño ,content=None):
    filesystem = ""
    with open(filename, "r") as file:
        filesystem = json.load(file)
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    current_dir[item_name] = {
        "type": item_type,
        "tamano":tamaño,
        "path":pathDir,
        "content": content if item_type == "file" else {}
    }
    with open(filename, "w") as file:
        json.dump(filesystem, file)  

def get_properties(user_name, name, path):
    properties = ""
    with open(user_name, "r") as file:
        filesystem = json.load(file)    
    path_parts = path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if name in current_dir:
    #Aqui obtiene las propiedades del archivo que esta buscando.
        current_date = current_dir[name]["current-date"]
        modified_date = current_dir[name]["modified-date"]
        size = current_dir[name]["tamano"]
        properties = f"Nombre: {name}, Fecha de creación: {current_date}, Fecha de modificación: {modified_date}, Tamaño: {size}"

        return properties
    
def modify_file(user, file_path, new_content, name):
    with open(user, "r") as file:
        filesystem = json.load(file)    
    path_parts = file_path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if name in current_dir:
        current_dir[name]["content"] = new_content
        current_dir[name]["tamano"] = len(new_content)
        current_dir[name]["modified-date"] = str(date.today())

    with open(user, "w") as file:
        json.dump(filesystem, file)
        
def get_content(user, name, file_path):
    content_file = ""
    with open(user, "r") as file:
        filesystem = json.load(file)    
    path_parts = file_path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if name in current_dir:
        content_file = current_dir[name]["content"]
        return content_file

def download(user,name,file_path,NuevaRuta):

    contenido = get_content(user,name,file_path)
    download_aux(contenido, name,NuevaRuta)
    
def download_aux(Contenido, NombreArchivo,NuevaRuta):
    #"C:/Users/josue/Downloads/"
    file = open(NuevaRuta + NombreArchivo, "w")
    file.write(Contenido + os.linesep)
    file.close()

def share_file(user, user_to_share, file_path, file_name):
    with open(user, "r") as file:
        filesystem = json.load(file)    
    path_parts = file_path.split("/")
    current_dir = filesystem
    for part in path_parts:
        current_dir = current_dir[part]["content"]
    if file_name in current_dir:
        archivo = current_dir
        archivo[file_name]["path"] = "compartido"
        share_file_aux(user_to_share, archivo)


def share_file_aux(user, target_file):
    with open(user, "r") as file:
        filesystem = json.load(file)

    current_dir = filesystem["compartido"]
    current_dir["content"] = {**current_dir.pop("content"), **target_file}

    with open(user, "w") as file:
        json.dump(filesystem, file)

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
