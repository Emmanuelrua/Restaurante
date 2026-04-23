from dotenv import load_dotenv

load_dotenv()  # carga .env antes de que los módulos CLI instancien el storage

from src.mi_app.cli.app import app

if __name__ == "__main__":
    app()