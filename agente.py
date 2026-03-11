import tkinter as tk
from tkinter import filedialog
import json
import os
import time
import threading
import requests

CONFIG_FILE = "config.json"

rodando = False


# ===============================
# CONFIGURAÇÃO
# ===============================

def salvar_config():

    config = {
        "cnpj": entry_cnpj.get(),
        "token": entry_token.get(),
        "api_url": entry_api.get(),
        "pasta_xml": entry_pasta.get()
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    log("Configuração salva")


def carregar_config():

    if not os.path.exists(CONFIG_FILE):
        return

    with open(CONFIG_FILE) as f:
        config = json.load(f)

    entry_cnpj.insert(0, config.get("cnpj", ""))
    entry_token.insert(0, config.get("token", ""))
    entry_api.insert(0, config.get("api_url", ""))
    entry_pasta.insert(0, config.get("pasta_xml", ""))


def escolher_pasta():

    pasta = filedialog.askdirectory()

    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)


# ===============================
# LOG
# ===============================

def log(msg):

    texto_log.insert(tk.END, msg + "\n")
    texto_log.see(tk.END)


# ===============================
# ENVIO XML
# ===============================

def enviar_xml(caminho, config):

    try:

        with open(caminho, "rb") as f:

            r = requests.post(
                config["api_url"],
                files={"arquivo": f},
                data={"cnpj": config["cnpj"]},
                headers={
                    "Authorization": f"Bearer {config['token']}"
                }
            )

        log(f"{os.path.basename(caminho)} -> {r.text}")

    except Exception as e:

        log(f"Erro: {e}")


# ===============================
# MONITORAMENTO
# ===============================

def monitorar():

    global rodando

    enviados = set()

    with open(CONFIG_FILE) as f:
        config = json.load(f)

    pasta = config["pasta_xml"]

    log("Monitorando pasta: " + pasta)

    while rodando:

        try:

            arquivos = os.listdir(pasta)

            for arquivo in arquivos:

                if not arquivo.lower().endswith(".xml"):
                    continue

                if arquivo in enviados:
                    continue

                caminho = os.path.join(pasta, arquivo)

                enviar_xml(caminho, config)

                enviados.add(arquivo)

        except Exception as e:

            log(f"Erro monitoramento: {e}")

        time.sleep(5)


# ===============================
# CONTROLE
# ===============================

def iniciar():

    global rodando

    if rodando:
        log("Agente já está rodando")
        return

    rodando = True

    thread = threading.Thread(target=monitorar, daemon=True)
    thread.start()

    log("Agente iniciado")


def parar():

    global rodando

    rodando = False

    log("Agente parado")


# ===============================
# INTERFACE
# ===============================

janela = tk.Tk()
janela.title("Agente Integração Fiscal")
janela.geometry("500x500")

tk.Label(janela, text="CNPJ").pack()

entry_cnpj = tk.Entry(janela, width=50)
entry_cnpj.pack()

tk.Label(janela, text="Token").pack()

entry_token = tk.Entry(janela, width=50)
entry_token.pack()

tk.Label(janela, text="URL da API").pack()

entry_api = tk.Entry(janela, width=50)
entry_api.pack()

tk.Label(janela, text="Pasta XML").pack()

entry_pasta = tk.Entry(janela, width=50)
entry_pasta.pack()

tk.Button(janela, text="Escolher pasta", command=escolher_pasta).pack(pady=5)

tk.Button(janela, text="Salvar configuração", command=salvar_config).pack(pady=5)

tk.Button(janela, text="Iniciar agente", command=iniciar).pack(pady=5)

tk.Button(janela, text="Parar agente", command=parar).pack(pady=5)

tk.Label(janela, text="Log").pack()

texto_log = tk.Text(janela, height=15)
texto_log.pack(fill="both", expand=True)

carregar_config()

janela.mainloop()