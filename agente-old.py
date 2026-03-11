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

import tkinter as tk
from tkinter import filedialog, ttk  # Adicionado ttk para componentes modernos

# ... (Mantenha suas funções de lógica iguais) ...

# ===============================
# INTERFACE MODERNA
# ===============================

import tkinter as tk
from tkinter import ttk
import os

janela = tk.Tk()
janela.title("Agente de Integração Fiscal")
janela.geometry("650x700")
janela.configure(bg="#f5f6f7")

# ===============================
# ESTILO
# ===============================

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI",10), padding=8)
style.configure("Title.TLabel", font=("Segoe UI",16,"bold"), background="#f5f6f7")

# ===============================
# CONTAINER
# ===============================

main = tk.Frame(janela,bg="#f5f6f7")
main.pack(fill="both",expand=True,padx=20,pady=20)

# ===============================
# FRAMES
# ===============================

frame_config1 = tk.Frame(main,bg="#f5f6f7")
frame_config2 = tk.Frame(main,bg="#f5f6f7")
frame_principal = tk.Frame(main,bg="#f5f6f7")

# ===============================
# FUNÇÃO TROCAR TELA
# ===============================

def mostrar(frame):

    for f in (frame_config1,frame_config2,frame_principal):
        f.pack_forget()

    frame.pack(fill="both",expand=True)

# ===============================
# CONFIG PASSO 1
# ===============================

ttk.Label(frame_config1,
          text="Passo 1 - Dados da Empresa",
          style="Title.TLabel").pack(anchor="w",pady=10)

entry_cnpj = ttk.Entry(frame_config1)
entry_token = ttk.Entry(frame_config1)
entry_api = ttk.Entry(frame_config1)

tk.Label(frame_config1,text="CNPJ",bg="#f5f6f7").pack(anchor="w")
entry_cnpj.pack(fill="x",pady=5)

tk.Label(frame_config1,text="Token",bg="#f5f6f7").pack(anchor="w")
entry_token.pack(fill="x",pady=5)

tk.Label(frame_config1,text="API",bg="#f5f6f7").pack(anchor="w")
entry_api.pack(fill="x",pady=5)

ttk.Button(frame_config1,
           text="Próximo →",
           command=lambda: mostrar(frame_config2)).pack(pady=20)

# ===============================
# CONFIG PASSO 2
# ===============================

ttk.Label(frame_config2,
          text="Passo 2 - Pasta XML",
          style="Title.TLabel").pack(anchor="w",pady=10)

entry_pasta = ttk.Entry(frame_config2)
entry_pasta.pack(fill="x",pady=10)

ttk.Button(frame_config2,
           text="📁 Procurar Pasta",
           command=escolher_pasta).pack()

def salvar_e_abrir():

    salvar_config()

    mostrar(frame_principal)

ttk.Button(frame_config2,
           text="💾 Salvar Configuração",
           command=salvar_e_abrir).pack(pady=20)

ttk.Button(frame_config2,
           text="← Voltar",
           command=lambda: mostrar(frame_config1)).pack()

# ===============================
# TELA PRINCIPAL
# ===============================

top_bar = tk.Frame(frame_principal,bg="#f5f6f7")
top_bar.pack(fill="x")

ttk.Label(top_bar,
          text="Agente de Integração Fiscal",
          style="Title.TLabel").pack(side="left")

ttk.Button(top_bar,
           text="⚙ Configurações",
           command=lambda: mostrar(frame_config1)).pack(side="right")

# BOTÕES

control = tk.Frame(frame_principal,bg="#f5f6f7")
control.pack(fill="x",pady=15)

ttk.Button(control,
           text="▶ Iniciar Agente",
           command=iniciar).pack(side="left",expand=True,fill="x",padx=5)

ttk.Button(control,
           text="■ Parar Agente",
           command=parar).pack(side="left",expand=True,fill="x",padx=5)

# LOG

log_frame = tk.Frame(frame_principal,bg="white",bd=1,relief="solid")
log_frame.pack(fill="both",expand=True)

texto_log = tk.Text(log_frame,
                    bg="#2d2d2d",
                    fg="#dcdcdc",
                    font=("Consolas",9))

texto_log.pack(side="left",fill="both",expand=True)

scroll = ttk.Scrollbar(log_frame,command=texto_log.yview)
scroll.pack(side="right",fill="y")

texto_log.configure(yscrollcommand=scroll.set)

# ===============================
# PRIMEIRA EXECUÇÃO OU NÃO
# ===============================

if os.path.exists("config.json"):
    mostrar(frame_principal)
else:
    mostrar(frame_config1)

janela.mainloop()