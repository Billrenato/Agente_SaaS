import requests
import os

def enviar_xml(caminho, config, log):

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

        log(f"{os.path.basename(caminho)} enviado -> {r.text}")

    except Exception as e:

        log(f"Erro envio: {e}")