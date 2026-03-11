from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.enviar_xml import enviar_xml

observer = None

class XMLHandler(FileSystemEventHandler):

    def __init__(self, config, log):
        self.config = config
        self.log = log

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".xml"):
            return

        self.log(f"XML detectado: {event.src_path}")

        enviar_xml(event.src_path, self.config, self.log)


def iniciar_monitoramento(config, log):

    global observer

    pasta = config["pasta_xml"]

    handler = XMLHandler(config, log)

    observer = Observer()
    observer.schedule(handler, pasta, recursive=False)

    observer.start()

    log("Monitorando pasta: " + pasta)


def parar_monitoramento(log):

    global observer

    if observer:

        observer.stop()
        observer.join()

        log("Monitoramento parado")