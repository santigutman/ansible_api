# ejecutar_ansible.sh --vars {"tipo":"","servidor":"","base":"","nombreBD":"","parametros":{"query":""}}

from fastapi import FastAPI
from pydantic import BaseModel
import json, subprocess

app = FastAPI()

# Datos que vienen en el body
class Vars(BaseModel):
    tipo: str
    servidor: str
    base: str
    nombreBD: str
    parametros: dict

@app.post("/run-playbook/")
def run_playbook(vars: Vars):
    # Guardamos los parámetros en un archivo JSON temporal
    with open("vars.json", "w") as f:
        json.dump(vars.dict(), f, indent=4)

    # Ejecutamos ansible con ese archivo como extra-vars
    cmd = [
        "ansible-playbook", 
        "playbook.yml", 
        "--extra-vars", 
        "@vars.json"
    ]
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True
    )

    # Si ansible terminó bien
    if result.returncode == 0:
        return {"status": "OK"}
    else:
        return {
            "status": "ERROR",
            "stderr": result.stderr.splitlines()[-10:]  # últimas 10 líneas del error
        }
