import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading


def criar_icone():

    img = Image.new("RGB", (64, 64), "green")
    draw = ImageDraw.Draw(img)
    draw.rectangle((16,16,48,48), fill="white")

    return img


def iniciar_tray(mostrar_janela):

    def sair(icon, item):
        icon.stop()

    menu = (
        item("Abrir Painel", lambda: mostrar_janela()),
        item("Sair", sair)
    )

    icon = pystray.Icon(
        "Agente Fiscal",
        criar_icone(),
        "Agente Fiscal",
        menu
    )

    threading.Thread(target=icon.run, daemon=True).start()