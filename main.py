from app.app import App
import os

if __name__ == "__main__":

    project_base = input("Ingresa la ruta de la carpeta del proyecto: ")
    if os.path.exists(project_base):
        app = App()
        app.project_comment(project_base)
        print("Proceso completado. Revisa los archivos comentados.")
    else:
        print(f"La carpeta '{project_base}' no existe.")
