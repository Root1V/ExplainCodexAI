from openai import OpenAI
from dotenv import load_dotenv
from app.config import Config
import os


class App:

    def __init__(self) -> None:
        self.config = Config.get_all()
        self.client = OpenAI()
        self.PROMPT = Config.load_prompt()

        print("PROMPT SYS:\n", self.PROMPT)

    def comment_code(self, code):
        """Envía el código al LLM para obtener comentarios."""
        prompt = f"Comenta el siguiente código Python:\n\n{code}"

        message = self.client.chat.completions.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[
                {
                    "role": "system",
                    "content": self.PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
        )

        return message.choices[0].message.content

    def file_process(self, path_file):
        """Lee el archivo, genera los comentarios y escribe la versión comentada."""
        with open(path_file, "r") as file:
            code = file.read()

        print(f"Generando comentarios para {path_file}...")
        comments_code = self.comment_code(code)

        # Guarda el código comentado en un nuevo archivo
        path_comment = path_file.replace(".py", "_comment.py")
        with open(path_comment, "w") as file_comment:
            file_comment.write(comments_code)

    def project_comment(self, folder_base):
        """Recorre todos los archivos Python en la carpeta y comenta el código."""
        for root_folder, sub_folder, files in os.walk(folder_base):

            if ".venv" in sub_folder:
                sub_folder.remove(".venv")

            folder_exclude = [".venv", "docs"]
            sub_folder[:] = [sub for sub in sub_folder if sub not in folder_exclude]

            for file in files:
                if file.endswith(".py"):
                    path_full = os.path.join(root_folder, file)
                    self.file_process(path_full)

    def generate_text(self, prompt):
        """Generar texto con el modelo LLM GTP-4o-mini"""

        message = self.client.chat.completions.create(
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=[
                {"role": "system", "content": "You are a smart AI assitant"},
                {"role": "user", "content": prompt},
            ],
        )
        return message.choices[0].message.content


if __name__ == "__main__":
    load_dotenv()
