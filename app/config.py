import json
import os


class Config:
    _config = None
    PROMPT_DIR = "app/programmer_sys.txt"

    @classmethod
    def get_all(cls, filepath="app/config-model.json"):
        """Carga y devuelve todos los valores del archivo config-model.json."""
        if cls._config is None:
            with open(filepath, "r") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def load_prompt(cls):
        """Carga y devuelve el contenido del prompt.txt"""

        if not os.path.exists(cls.PROMPT_DIR):
            raise FileNotFoundError(f"El archivo {cls.PROMPT_DIR} no existe.")

        with open(cls.PROMPT_DIR, "r") as file:
            return file.read()
