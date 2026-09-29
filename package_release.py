"""Gera o ZIP público sempre com dados vazios, sem ler arquivos pessoais."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from storage import vazio

INSTRUCOES = """TaskManager — versão portátil para Windows x64

1. Extraia TODO o ZIP para uma pasta sua, como Documentos/TaskManager.
2. Abra TaskManager.exe e informe seu nome.
3. Mantenha dados.json ao lado do executável. Não é necessário instalar Python.

Nome, tarefas e compromissos são salvos em dados.json nessa mesma pasta.
Não execute diretamente de dentro do ZIP. A pasta precisa permitir gravação.
Para transportar ou fazer backup, feche o programa e copie a pasta inteira.
Ao atualizar o aplicativo, substitua somente TaskManager.exe; preserve seu JSON.
Use apenas uma instância por vez.

Este pacote contém dados vazios, sem registros pessoais do desenvolvedor.
Para importar registros de uma versão anterior, feche o programa e copie seu
%APPDATA%/TaskManager/dados.json para o lado deste executável, substituindo apenas
o JSON vazio do pacote. Guarde uma cópia de segurança antes da substituição.
"""


def criar_zip():
    pasta = Path(__file__).resolve().parent / "dist"
    executavel = pasta / "portatil" / "TaskManager.exe"
    destino = pasta / "TaskManager-portatil.zip"
    with ZipFile(destino, "w", ZIP_DEFLATED) as arquivo:
        arquivo.write(executavel, "TaskManager/TaskManager.exe")
        arquivo.writestr("TaskManager/dados.json", json.dumps(vazio(), ensure_ascii=False, indent=2) + "\n")
        arquivo.writestr("TaskManager/LEIA-ME.txt", INSTRUCOES)
    return destino


if __name__ == "__main__":
    print(criar_zip())
