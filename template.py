import os, logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

proj_name = "network_security"
proj_data_folder = "network_security_data"
list_of_files = [
    ".github/workflows/.gitkeep",        # CI/CD
    ".github/workflows/main.yaml",
    

    f"src/{proj_name}/__init__.py",
    f"src/{proj_name}/components/__init__.py",  # core ML logic
    f"src/{proj_name}/constants/__init__.py",
    f"src/{proj_name}/exception/__init__.py",
    f"src/{proj_name}/cloud/__init__.py",
    f"src/{proj_name}/logging/__init__.py",
    
    
    f"src/{proj_name}/config/__init__.py",
    f"src/{proj_name}/config/configuration.py",

    f"src/{proj_name}/utils/__init__.py",       # helper functions
    f"src/{proj_name}/utils/common.py",

    f"src/{proj_name}/pipeline/__init__.py",    # training & prediction flow
    f"src/{proj_name}/entity/__init__.py",      # config dataclasses
    f"src/{proj_name}/entity/entity_config.py",

    "config/config.yaml",   # paths & settings
    "params.yaml",          # hyperparameters
    "schema.yaml",          # data schema
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "notebooks/research.ipynb",  # EDA & experiments
    "templates/index.html"       # Flask UI
]

for file in list_of_files:
    file_path = Path(file)
    file_dir ,file_name = os.path.split(file_path)
    
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory: {file_dir} for file: {file_name}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
            logging.info(f"Creating empty file: {file_path}")
    else:
        logging.info(f"{file_path} already exists")