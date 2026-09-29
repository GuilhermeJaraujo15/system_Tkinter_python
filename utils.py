"""Validação e ordenação compartilhadas pela interface e persistência."""
import re
from datetime import datetime

PRIORIDADES = ("Alta", "Média", "Baixa")
STATUS = ("Pendente", "Em andamento", "Concluída")


def momento(data, horario):
    if not isinstance(data, str) or not re.fullmatch(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", data):
        raise ValueError("Informe a data no formato DD/MM/AAAA.")
    if not isinstance(horario, str) or not re.fullmatch(r"[0-9]{2}:[0-9]{2}", horario):
        raise ValueError("Informe o horário no formato HH:MM.")
    try:
        return datetime.strptime(f"{data} {horario}", "%d/%m/%Y %H:%M")
    except ValueError:
        raise ValueError("Data ou horário inválido. Confira o calendário e use horas entre 00:00 e 23:59.") from None


def validar(registro, tipo):
    campos = ("titulo", "descricao", "data", "horario")
    campos += ("responsavel", "prioridade", "status") if tipo == "tarefas" else ("local",)
    resultado = {}
    for campo in campos:
        valor = registro.get(campo, "")
        if not isinstance(valor, str):
            raise ValueError(f"O campo {campo} deve ser texto.")
        resultado[campo] = valor.strip()
    if not resultado["titulo"]:
        raise ValueError("Informe o título.")
    momento(resultado["data"], resultado["horario"])
    if tipo == "tarefas":
        if resultado["prioridade"] not in PRIORIDADES:
            raise ValueError("Selecione uma prioridade válida.")
        if resultado["status"] not in STATUS:
            raise ValueError("Selecione um status válido.")
    return resultado


def ordem(registro):
    return momento(registro["data"], registro["horario"]), registro["id"]
