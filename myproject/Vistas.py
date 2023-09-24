from django.template import Template, Context
from django.http import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from Client import *
import os
import json


User_actual = ""


@csrf_exempt
def Main(request):
    global User_actual
    doc_externo = open(
        "C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/Main.html"
    )
    plt = Template(doc_externo.read())
    with open(User_actual, "r") as file:
        data = json.load(file)
    doc_externo.close()

    if request.method == "POST":
        # Esta funcionalidad es para cre un archivo

        if "BotonArchivo" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("nombre")
            contenido = request.POST.get("contenido")
            print("ESTA ES LA RUTA CON EL CONTENIDO:" + ruta + "|" + contenido)

            # Dismunuir la capacidad del usuario con el tamaño - Funcion
            tamaño = len(contenido)
            Funcion_Capacidad(tamaño)
            asyncio.run(AñadirArchivo(ruta, nombre, contenido, User_actual, tamaño))

            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        # Esta funcionalidad es para crear un directorio
        elif "BotonDirectorio" in request.POST:
            ruta = request.POST.get("ruta")
            nombre_directorio = request.POST.get("nombre-directorio")
            ruta_directory = ruta + "/" + nombre_directorio

            asyncio.run(
                AñadirDirectorio(
                    User_actual,
                    ruta,
                    nombre_directorio,
                    ruta_directory,
                    "directory",
                    0,
                    "",
                )
            )

            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "BotonMoverArchivo" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")
            nuevoDir = request.POST.get("ArchivoNRuta")

            if nombre == "COMANDO-A|B":
                asyncio.run(MoverDirectorio(User_actual, ruta, nuevoDir))

            else:
                asyncio.run(MoverArchivo(User_actual, ruta, nombre, nuevoDir))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "Boton-Cargar" in request.POST:
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "Boton-EliminarN" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")
            if nombre == "COMANDO-A|B":
                asyncio.run(EliminarDirec(User_actual, ruta))

            else:
                asyncio.run(EliminarNormal(User_actual, ruta, nombre))

            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "Boton-Compartir" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")
            Usuario_A_Compartir = request.POST.get("UsuarioArchivoCompartir")
        elif "boton-props" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("nombre-propiedades")

            propiedades = asyncio.run(show_properties(User_actual, nombre, ruta))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": propiedades, "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-modify" in request.POST:
            ruta = request.POST.get("ruta")
            new_content = request.POST.get("input-modificar-contenido")
            nombre = request.POST.get("nombre-archivo-modificar")

            asyncio.run(modify_file(User_actual, ruta, new_content, nombre))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-contenido" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("nombre-archivo-mostrar")

            content = asyncio.run(get_content(User_actual, nombre, ruta))
            data = cargarJson(data)
            ctx = Context({"data": data, "content": content, "propiedades": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-Download" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("nombre-archivo-mostrar")
            nuevoDir = request.POST.get("ArchivoNRuta")

            content = asyncio.run(download(User_actual, nombre, ruta, nuevoDir))
            data = cargarJson(data)
            ctx = Context({"data": data, "content": content, "propiedades": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-DownloadD" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("nombre-archivo-mostrar")
            nuevoDir = request.POST.get("ArchivoNRuta")

            content = asyncio.run(download_dir(User_actual, nombre, ruta, nuevoDir))
            data = cargarJson(data)
            ctx = Context({"data": data, "content": content, "propiedades": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-VV" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")
            nuevoDir = request.POST.get("ArchivoNRuta")

            if nombre == "COMANDO-A|B":
                asyncio.run(CopiarDirectorioVirtual(User_actual, ruta, nuevoDir))

            else:
                asyncio.run(CopiarArchivoVirtual(User_actual, ruta, nombre, nuevoDir))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-RV" in request.POST:
            RutaDrive = request.POST.get("input-ruta-real")
            RutaReal = request.POST.get("input-ruta-drive")
            asyncio.run(CopiarArchivoRealVirtual(User_actual, RutaReal, RutaDrive))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-RVD" in request.POST:
            RutaDrive = request.POST.get("input-ruta-real")
            RutaReal = request.POST.get("input-ruta-drive")
            asyncio.run(CopiarDirectorioRealVirtual(User_actual, RutaReal, RutaDrive))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "boton-compartir-direc" in request.POST:
            NombreUsuario = request.POST.get("UsuarioArchivoCompartir")
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")

            asyncio.run(ShareDir(User_actual, NombreUsuario, ruta))
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "archivo" in request.POST:
            ruta = request.POST.get("ruta")
            nombre = request.POST.get("NombreMovAr")
            Usuario_A_Compartir = request.POST.get("UsuarioArchivoCompartir")

            asyncio.run(
                share_file(User_actual, Usuario_A_Compartir + ".json", ruta, nombre)
            )
            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)
        elif "boton-eliminar" in request.POST:
            ruta = request.POST.get("input-ruta-eliminar-AD")
            path_parts = []
            path_parts = ruta.split(":")
            path_parts_copy = path_parts
            while path_parts != []:
                nombre_archivo = ""
                new_path = ""
                nombre_archivo = path_parts[0].split("/")[-1]
                path_parts_copy = path_parts[0].split("/")[:-1]
                separator = "/"
                new_path = separator.join(path_parts_copy)
                asyncio.run(EliminarNormal(User_actual, new_path, nombre_archivo))
                path_parts = path_parts[1:]

            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

        elif "boton-eliminar-Dir" in request.POST:
            ruta = request.POST.get("input-ruta-eliminar-AD")
            path_parts = []
            path_parts = ruta.split(":")
            while path_parts != []:
                asyncio.run(EliminarDirec(User_actual, path_parts[0]))
                path_parts = path_parts[1:]

            data = cargarJson(data)
            ctx = Context({"data": data, "propiedades": "", "content": ""})
            documento = plt.render(ctx)
            return HttpResponse(documento)

    else:
        data = cargarJson(data)
        ctx = Context({"data": data, "propiedades": "", "content": ""})
        documento = plt.render(ctx)
        return HttpResponse(documento)


@csrf_exempt
def login_view(request):
    global User_actual
    doc_externo = open(
        "C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/login.html"
    )

    plt = Template(doc_externo.read())

    doc_externo.close()

    ctx = Context()

    documento = plt.render(ctx)
    if request.method == "POST":
        if "login" in request.POST:
            # El botón "Iniciar sesión" ha sido presionado
            username = request.POST["username"]

            filename = f"{username}.json"
            User_actual = filename
            # add_item(filename, "local/subdir", "archivo1.txt", "file", "Contenido del archivo")
            # add_item(filename, "local", "Videos", "directory")
            # add_item(filename, "local/Videos", "VideosDatos.txt", "file", "Contenido del archivo")
            return redirect("/Main/")  # Redirige al nombre registrado en las URLs
        elif "register" in request.POST:
            return redirect("/register/")

    return HttpResponse(documento)


@csrf_exempt
def register_view(request):
    global User_actual
    doc_externo = open(
        "C:/Users/Josue/Desktop/Semestre I 2023/Operativos/Proyecto 3/myproject/myproject/Plantillas/register.html"
    )
    plt = Template(doc_externo.read())
    doc_externo.close()
    ctx = Context()
    documento = plt.render(ctx)
    if request.method == "POST":
        username = request.POST["username"]
        capacidad_str = request.POST["capacidad"]
        capacidad_int = int(capacidad_str)

        filename = f"{username}.json"
        User_actual = filename
        create_user_json(
            username, capacidad_int
        )  # Llama a la función para crear el JSON

        return redirect("/Main/")
    return HttpResponse(documento)


# _-------------------------------------------------------------------------------------------

# Entradas: Nombre de usuario log
# Restricciones: El usuario debe de estar creado
# Salida: Retorna un string simulando un html que contiene la estructura de una file system
# con los datos del Json


def cargarJson(estructura):
    html = "<ul>"
    for nombre, elemento in estructura.items():
        if elemento["type"] == "file":
            path = elemento["path"]

            html += f"<li class='file' onclick='mostrarOpcionesDirectorio(\"{nombre}\",\"{path}\") '>{nombre}</li>"
        elif elemento["type"] == "directory":
            path = elemento["path"]
            html += f"<li class='file' onclick='mostrarOpcionesDirectorio(\"{nombre}\",\"{path}\") '>{nombre} - Tipo: Directorio"
            html += cargarJson(elemento["content"])
            html += "</li>"
    html += "</ul>"
    return html


# Entradas : Num, largo del archivo que se esta creando
# Salidas : El archivo Json modificado con la nueva capacidad


def Funcion_Capacidad(Num):
    global User_actual
    # Cargar el archivo JSON
    with open(User_actual) as file:
        estructura = json.load(file)

    capacidad = estructura["User"]["capacidad"]

    # Modificar el valor sumando 10
    capacidad -= Num

    # Asignar el nuevo valor de "capacidad" en la estructura JSON
    estructura["User"]["capacidad"] = capacidad

    # Guardar los cambios en el archivo JSON
    with open(User_actual, "w") as file:
        json.dump(estructura, file)


def Validar_Existencia_Archivo(Estructura, Nombre, path):
    if Nombre in Estructura[path]["content"]:
        return "¡Ya existia!"

    else:
        return "¡No existia!"


def create_user_json(username, capacidad):
    filename = f"{username}.json"
    if not os.path.exists(filename):
        user_data = {
            "local": {"type": "directory", "path": "local", "tamano": 4, "content": {}},
            "compartido": {
                "type": "directory",
                "path": "compartido",
                "tamano": 10,
                "content": {},
            },
            "User": {"type": "none", "capacidad": capacidad},
        }
        with open(filename, "w") as file:
            json.dump(user_data, file)
