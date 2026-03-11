import tkinter as tk
from tkinter import ttk, filedialog
import os

from config.config_manager import salvar_config, carregar_config, config_existe
from core.monitor_xml import iniciar_monitoramento, parar_monitoramento
from tray.tray_icon import iniciar_tray


def iniciar_interface():

    janela = tk.Tk()
    janela.title("Agente de Integração Fiscal")
    janela.geometry("650x650")

    # ===============================
    # LOG
    # ===============================

    def log(msg):

        texto_log.insert(tk.END, msg + "\n")
        texto_log.see(tk.END)

    # ===============================
    # CONFIG
    # ===============================

    def escolher_pasta():

        pasta = filedialog.askdirectory()

        if pasta:
            entry_pasta.delete(0, tk.END)
            entry_pasta.insert(0, pasta)

    def salvar():

        config = {
            "cnpj": entry_cnpj.get(),
            "token": entry_token.get(),
            "api_url": entry_api.get(),
            "pasta_xml": entry_pasta.get()
        }

        salvar_config(config)

        log("Configuração salva")

        mostrar(frame_principal)

    # ===============================
    # AGENTE
    # ===============================

    def iniciar():

        config = carregar_config()

        iniciar_monitoramento(config, log)

    def parar():

        parar_monitoramento(log)

    # ===============================
    # ESCONDER JANELA
    # ===============================

    def esconder():

        janela.withdraw()

    def mostrar_janela():

        janela.deiconify()

    janela.protocol("WM_DELETE_WINDOW", esconder)

    iniciar_tray(mostrar_janela)

    # ===============================
    # FRAMES
    # ===============================

    main = tk.Frame(janela)
    main.pack(fill="both", expand=True, padx=20, pady=20)

    frame_config = tk.Frame(main)
    frame_principal = tk.Frame(main)

    def mostrar(frame):

        for f in (frame_config, frame_principal):
            f.pack_forget()

        frame.pack(fill="both", expand=True)

    # ===============================
    # CONFIG
    # ===============================

    ttk.Label(frame_config, text="Configuração Inicial", font=("Segoe UI",16)).pack(pady=10)

    entry_cnpj = ttk.Entry(frame_config)
    entry_token = ttk.Entry(frame_config)
    entry_api = ttk.Entry(frame_config)
    entry_pasta = ttk.Entry(frame_config)

    ttk.Label(frame_config,text="CNPJ").pack()
    entry_cnpj.pack(fill="x",pady=5)

    ttk.Label(frame_config,text="Token").pack()
    entry_token.pack(fill="x",pady=5)

    ttk.Label(frame_config,text="API URL").pack()
    entry_api.pack(fill="x",pady=5)

    ttk.Label(frame_config,text="Pasta XML").pack()
    entry_pasta.pack(fill="x",pady=5)

    ttk.Button(frame_config,text="Escolher Pasta",command=escolher_pasta).pack(pady=5)

    ttk.Button(frame_config,text="Salvar Configuração",command=salvar).pack(pady=10)

    # ===============================
    # PRINCIPAL
    # ===============================

    top = tk.Frame(frame_principal)
    top.pack(fill="x")

    ttk.Button(top,text="⚙ Configurações",command=lambda: mostrar(frame_config)).pack(side="right")

    control = tk.Frame(frame_principal)
    control.pack(fill="x", pady=10)

    ttk.Button(control,text="▶ Iniciar",command=iniciar).pack(side="left",expand=True,fill="x",padx=5)
    ttk.Button(control,text="■ Parar",command=parar).pack(side="left",expand=True,fill="x",padx=5)

    log_frame = tk.Frame(frame_principal)
    log_frame.pack(fill="both", expand=True)

    texto_log = tk.Text(log_frame,bg="#2d2d2d",fg="white",font=("Consolas",9))
    texto_log.pack(side="left",fill="both",expand=True)

    scroll = ttk.Scrollbar(log_frame,command=texto_log.yview)
    scroll.pack(side="right",fill="y")

    texto_log.configure(yscrollcommand=scroll.set)

    # ===============================
    # PRIMEIRA EXECUÇÃO
    # ===============================

    config = carregar_config()

    if config:

        entry_cnpj.insert(0, config["cnpj"])
        entry_token.insert(0, config["token"])
        entry_api.insert(0, config["api_url"])
        entry_pasta.insert(0, config["pasta_xml"])

        mostrar(frame_principal)

        iniciar()

    else:

        mostrar(frame_config)

    janela.mainloop()