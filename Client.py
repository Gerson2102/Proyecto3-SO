#!/usr/bin/env python

import asyncio
import websockets


async def AñadirArchivo(ruta, nombre, contenido, User, tamaño):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            ruta
            + "|"
            + nombre
            + "|"
            + contenido
            + "|"
            + User
            + "|"
            + str(tamaño)
            + "|"
            + "CRA"
        )
        await websocket.send(listaDatos)
        print(f">>> {nombre}")
        listaDatos = ""
        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def AñadirDirectorio(
    User_actual, ruta, nombre, ruta_directory, tipo, tamaño, content=None
):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            User_actual
            + "|"
            + ruta
            + "|"
            + nombre
            + "|"
            + ruta_directory
            + "|"
            + tipo
            + "|"
            + content
            + "|"
            + str(tamaño)
            + "|"
            + "CRD"
        )
        await websocket.send(listaDatos)
        print(f">>> {nombre}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def MoverArchivo(User, path, nombre, nuevoDir):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + nombre + "|" + nuevoDir + "|" + "MOV"
        await websocket.send(listaDatos)
        print(f">>> {nombre}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def CopiarArchivoVirtual(User, path, nombre, nuevoDir):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + nombre + "|" + nuevoDir + "|" + "COPVIR"
        await websocket.send(listaDatos)
        print(f">>> {nombre}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def CopiarDirectorioVirtual(User, path, nuevoDir):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + nuevoDir + "|" + "COPDIR"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def MoverDirectorio(User, path, nuevoDir):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + nuevoDir + "|" + "MOVDIR"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def EliminarNormal(User, path, nombre):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + nombre + "|" + "ElIMN"
        await websocket.send(listaDatos)
        print(f">>> {nombre}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def EliminarDirec(User, path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + path + "|" + "ElIMD"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def show_properties(User_actual, nombre, ruta):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User_actual + "|" + nombre + "|" + ruta + "|" + "PROP"
        await websocket.send(listaDatos)
        print(f">>> {nombre}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        return greeting


async def modify_file(User_actual, ruta, new_content, name):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            User_actual + "|" + ruta + "|" + new_content + "|" + name + "|" + "MOD"
        )
        await websocket.send(listaDatos)
        print(f">>> {ruta}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        return greeting


async def get_content(User_actual, name, ruta):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User_actual + "|" + name + "|" + ruta + "|" + "CONTENT"
        await websocket.send(listaDatos)
        print(f">>> {ruta}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        return greeting


async def download(User_actual, name, ruta, NuevaRuta):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            User_actual + "|" + name + "|" + ruta + "|" + NuevaRuta + "|" + "DOWN"
        )
        await websocket.send(listaDatos)
        print(f">>> {ruta}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        return greeting


async def download_dir(User_actual, name, ruta, NuevaRuta):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            User_actual + "|" + name + "|" + ruta + "|" + NuevaRuta + "|" + "DOWND"
        )
        await websocket.send(listaDatos)
        print(f">>> {ruta}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

        return greeting


async def CopiarArchivoRealVirtual(User, ArchivoReal, ArchivoDrive):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + ArchivoReal + "|" + ArchivoDrive + "|" + "LOAD"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def CopiarDirectorioRealVirtual(User, ArchivoReal, ArchivoDrive):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + ArchivoReal + "|" + ArchivoDrive + "|" + "LOADD"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def ShareDir(User, UsuarioCompartir, Path):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = User + "|" + UsuarioCompartir + "|" + Path + "|" + "SHAREDIR"
        await websocket.send(listaDatos)
        print(f">>> {User}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


async def share_file(User_actual, user_to_share, ruta, name):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        listaDatos = (
            User_actual + "|" + user_to_share + "|" + ruta + "|" + name + "|" + "SH"
        )
        await websocket.send(listaDatos)
        print(f">>> {ruta}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")
