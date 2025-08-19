import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class PlaybookParams(BaseModel):
    tipo: str
    servidor: str
    base: str
    nombreBD: str
    parametros: dict

@app.post("/run-playbook/")
def run_playbook(params: PlaybookParams):
    # Construir path dinámico según tipo
    playbook_file = f"playbooks/{params.tipo}.yml"

    # Verificar que el playbook exista
    if not os.path.exists(playbook_file):
        raise HTTPException(status_code=400, detail=f"Playbook '{params.tipo}' no encontrado")

    # Armar comando de Ansible
    cmd = [
        "ansible-playbook",
        playbook_file,
        "--extra-vars",
        f"tipo={params.tipo} servidor={params.servidor} base={params.base} nombreBD={params.nombreBD} parametros='{params.parametros}'"
    ]

    # Ejecutar y capturar salida
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Imprimir en consola
    print(result.stdout)
    print(result.stderr)

    # Devolver salida en JSON
    return {
        "status": "OK" if result.returncode == 0 else "ERROR",
        "stdout": result.stdout,
        "stderr": result.stderr
    }

