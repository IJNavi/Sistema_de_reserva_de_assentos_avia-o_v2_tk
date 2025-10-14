import logging
import threading
from datetime import datetime


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logging.basicConfig(
            filename='sistema_reservas.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def log(self, nivel, mensagem, cpf=None):
        with self._lock:
            if cpf:
                mensagem = f"CPF: {cpf} - {mensagem}"
            logging.log(nivel, mensagem)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}")