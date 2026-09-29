"""JSON atômico, recuperação conservadora e proteção contra edições concorrentes."""
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from utils import validar


def diretorio_dados():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(os.environ.get("APPDATA", Path.home() / ".config")) / "TaskManager"


def vazio():
    return {"versao": 1, "tarefas": [], "agendamentos": [],
            "proximos_ids": {"tarefas": 1, "agendamentos": 1}}


class StorageError(Exception):
    pass


class Storage:
    def __init__(self, pasta=None):
        self.pasta = Path(pasta) if pasta is not None else diretorio_dados()
        self.arquivo = self.pasta / "dados.json"
        self.aviso = ""
        self._original = None

    def carregar(self):
        try:
            self.pasta.mkdir(parents=True, exist_ok=True)
            self._original = self.arquivo.read_bytes() if self.arquivo.exists() else None
            if not self._original or not self._original.strip():
                dados = vazio()
                self.salvar(dados)
                return dados
            dados = json.loads(self._original.decode("utf-8-sig"))
            self._validar_documento(dados)
            return dados
        except (ValueError, TypeError, KeyError, UnicodeError) as erro:
            backup = self.pasta / f"dados.corrompidos-{datetime.now():%Y%m%d-%H%M%S-%f}.json"
            try:
                backup.write_bytes(self._original)
                dados = vazio()
                self.salvar(dados)
            except OSError as falha:
                raise StorageError(f"Não foi possível preservar os dados: {falha}") from falha
            self.aviso = f"O arquivo de dados estava inválido ({erro}). Uma cópia foi preservada em:\n{backup}\n\nO programa iniciou com listas vazias."
            return dados
        except OSError as erro:
            raise StorageError(f"Não foi possível acessar os dados: {erro}") from erro

    @staticmethod
    def _validar_documento(dados):
        if not isinstance(dados, dict) or dados.get("versao") != 1:
            raise ValueError("Formato de arquivo desconhecido")
        for tipo in ("tarefas", "agendamentos"):
            if not isinstance(dados[tipo], list):
                raise ValueError("Lista de registros inválida")
            ids = set()
            for registro in dados[tipo]:
                if not isinstance(registro, dict):
                    raise ValueError("Registro inválido")
                identificador = registro["id"]
                if type(identificador) is not int or identificador < 1 or identificador in ids:
                    raise ValueError("Identificador inválido ou duplicado")
                ids.add(identificador)
                validar(registro, tipo)
            proximo = dados["proximos_ids"][tipo]
            if type(proximo) is not int or proximo <= max(ids, default=0):
                raise ValueError("Contador de identificadores inválido")

    def salvar(self, dados):
        temporario = None
        try:
            atual = self.arquivo.read_bytes() if self.arquivo.exists() else None
            if atual != self._original:
                raise StorageError("Os dados foram alterados por outra instância. Feche e reabra o programa antes de salvar.")
            conteudo = (json.dumps(dados, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            with tempfile.NamedTemporaryFile(dir=self.pasta, delete=False, suffix=".tmp") as arquivo:
                temporario = Path(arquivo.name)
                arquivo.write(conteudo)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, self.arquivo)
            self._original = conteudo
        except OSError as erro:
            raise StorageError(f"Não foi possível salvar. A alteração não foi aplicada.\n{erro}") from erro
        finally:
            if temporario and temporario.exists():
                temporario.unlink(missing_ok=True)
