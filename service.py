"""Regras de negócio independentes dos widgets."""
from copy import deepcopy
from datetime import datetime

from utils import validar, ordem, momento


class TaskService:
    def __init__(self, storage):
        self.storage = storage
        self.dados = storage.carregar()

    @property
    def nome_usuario(self):
        nome = self.dados.get("nome_usuario", "")
        return nome.strip() if isinstance(nome, str) and len(nome.strip()) <= 60 else ""

    def salvar_nome(self, nome):
        nome = " ".join(nome.split())
        if not nome or len(nome) > 60:
            raise ValueError("Informe seu nome com 1 a 60 caracteres.")
        novos = deepcopy(self.dados)
        novos["nome_usuario"] = nome
        self.storage.salvar(novos)
        self.dados = novos

    def salvar(self, tipo, valores, identificador=None):
        registro = validar(valores, tipo)
        novos = deepcopy(self.dados)
        if identificador is None:
            registro["id"] = novos["proximos_ids"][tipo]
            novos["proximos_ids"][tipo] += 1
            novos[tipo].append(registro)
        else:
            registro["id"] = identificador
            indice = next((i for i, item in enumerate(novos[tipo]) if item["id"] == identificador), None)
            if indice is None:
                raise ValueError("Registro não encontrado.")
            novos[tipo][indice] = registro
        self.storage.salvar(novos)
        self.dados = novos
        return registro["id"]

    def obter(self, tipo, identificador):
        for item in self.dados[tipo]:
            if item["id"] == identificador:
                return deepcopy(item)
        raise ValueError("Registro não encontrado.")

    def excluir(self, tipo, identificador):
        self.obter(tipo, identificador)
        novos = deepcopy(self.dados)
        novos[tipo] = [item for item in novos[tipo] if item["id"] != identificador]
        self.storage.salvar(novos)
        self.dados = novos

    def concluir(self, identificador):
        registro = self.obter("tarefas", identificador)
        if registro["status"] == "Concluída":
            return False
        registro["status"] = "Concluída"
        self.salvar("tarefas", registro, identificador)
        return True

    def tarefas(self, pesquisa="", prioridade="Todas", status="Todos"):
        busca = pesquisa.strip().casefold()
        return deepcopy(sorted((item for item in self.dados["tarefas"]
            if (busca in item["titulo"].casefold() or busca in item["responsavel"].casefold())
            and (prioridade == "Todas" or item["prioridade"] == prioridade)
            and (status == "Todos" or item["status"] == status)), key=ordem))

    def agenda(self, futuros=True, agora=None):
        agora = agora or datetime.now().replace(second=0, microsecond=0)
        return deepcopy(sorted((item for item in self.dados["agendamentos"]
            if not futuros or momento(item["data"], item["horario"]) >= agora), key=ordem))

    def contadores(self):
        total = len(self.dados["tarefas"])
        concluidas = sum(item["status"] == "Concluída" for item in self.dados["tarefas"])
        return total, total - concluidas, concluidas
