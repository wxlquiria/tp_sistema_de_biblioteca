API de Biblioteca

API REST para gestionar una biblioteca: autores, libros, socios y préstamos. Hecha con FastAPI y SQLModel.

Autora: Salcedo Walquiria · Materia: Programacion 4.

Requisitos:
Python 3.10 o superior (desarrollado con Python 3.14)
pip

Instalación:
git clone <URL-DEL-REPOSITORIO>
cd <carpeta-del-repositorio>
python -m venv venv

windows
venv\Scripts\Activate.ps1
linux/macOs
source venv/bin/activate

pip install -r requirements.txt

Cómo correr la aplicación
Desde la carpeta raíz del proyecto, con el entorno virtual activado:
fastapi dev main.py
(alternativa: uvicorn main:app --reload)

La documentación interactiva, donde se puede probar cada endpoint, queda en http://127.0.0.1:8000/docs.

Al arrancar por primera vez la app crea las tablas en biblioteca.db y carga datos de ejemplo (autores, libros y socios). Para empezar de cero, borrar el archivo biblioteca.db y volver a arrancar.

Cómo correr los tests:
pytest

Con reporte de cobertura:
pytest --cov --cov-report=term-missing
