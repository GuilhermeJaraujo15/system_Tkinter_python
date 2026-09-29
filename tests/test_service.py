import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from service import TaskService
from storage import Storage, StorageError, diretorio_dados
from utils import momento


def tarefa(**kwargs):
    return dict(titulo="Relatório mensal", descricao="Ação e revisão", responsavel="Ana",
                prioridade="Alta", data="30/09/2026", horario="14:30", status="Pendente", **kwargs)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.storage = Storage(self.temp.name)
        self.service = TaskService(self.storage)

    def test_crud_restart_and_ids(self):
        first = self.service.salvar("tarefas", tarefa())
        edited = tarefa()
        edited["titulo"] = "Revisar relatório"
        self.assertEqual(first, self.service.salvar("tarefas", edited, first))
        self.assertEqual((1, 1, 0), self.service.contadores())
        self.assertTrue(self.service.concluir(first))
        self.assertFalse(self.service.concluir(first))
        restored = TaskService(Storage(self.temp.name))
        self.assertEqual((1, 0, 1), restored.contadores())
        self.assertEqual("Revisar relatório", restored.obter("tarefas", first)["titulo"])
        self.service.excluir("tarefas", first)
        self.assertEqual([], TaskService(Storage(self.temp.name)).tarefas())
        self.assertGreater(self.service.salvar("tarefas", tarefa()), first)

    def test_validation(self):
        for key, value in (("titulo", " "), ("data", "31/02/2026"), ("data", "1/02/2026"),
                           ("horario", "25:90"), ("horario", "9:00"), ("prioridade", "Urgente"), ("status", "Finalizada")):
            with self.subTest(key=key, value=value):
                data = tarefa()
                data[key] = value
                with self.assertRaises(ValueError):
                    self.service.salvar("tarefas", data)
        self.assertEqual([], self.service.tarefas())
        self.assertEqual(29, momento("29/02/2024", "23:59").day)

    def test_combined_filters(self):
        self.service.salvar("tarefas", tarefa())
        other = tarefa()
        other.update(titulo="Reunião", responsavel="João", prioridade="Baixa", status="Em andamento")
        self.service.salvar("tarefas", other)
        self.assertEqual(1, len(self.service.tarefas("RELATÓRIO", "Alta", "Pendente")))
        self.assertEqual(1, len(self.service.tarefas("JOÃO")))
        self.assertEqual([], self.service.tarefas("relatório", "Baixa"))
        self.assertEqual(2, len(self.service.tarefas()))

    def test_agenda_chronological_and_restart(self):
        for date in ("01/10/2026", "30/09/2026", "01/01/2025"):
            self.service.salvar("agendamentos", dict(titulo="Reunião", descricao="", local="Sala", data=date, horario="10:00"))
        restored = TaskService(Storage(self.temp.name))
        self.assertEqual(["30/09/2026", "01/10/2026"], [r["data"] for r in restored.agenda(agora=datetime(2026, 9, 29))])
        self.assertEqual(3, len(restored.agenda(futuros=False)))
        with self.assertRaises(ValueError):
            restored.salvar("agendamentos", dict(titulo="", data="30/09/2026", horario="10:00"))
        for date, hour in (("31/02/2026", "10:00"), ("30/09/2026", "25:00")):
            with self.assertRaises(ValueError):
                restored.salvar("agendamentos", dict(titulo="Reunião", data=date, horario=hour))

    def test_corruption_preserved(self):
        self.storage.arquivo.write_bytes(b'{broken')
        restored = Storage(self.temp.name)
        self.assertEqual([], restored.carregar()["tarefas"])
        self.assertTrue(restored.aviso)
        self.assertEqual(b'{broken', next(Path(self.temp.name).glob("dados.corrompidos-*.json")).read_bytes())

    def test_empty_file(self):
        self.storage.arquivo.write_text("", encoding="utf-8")
        self.assertEqual((0, 0, 0), TaskService(Storage(self.temp.name)).contadores())

    def test_invalid_schema(self):
        self.storage.arquivo.write_text('{"versao":1,"tarefas":null}', encoding="utf-8")
        self.assertEqual([], Storage(self.temp.name).carregar()["tarefas"])

    def test_write_failure_rolls_back(self):
        original = self.storage.arquivo.read_bytes()
        with patch("storage.os.replace", side_effect=PermissionError("Falha simulada")):
            with self.assertRaises(StorageError):
                self.service.salvar("tarefas", tarefa())
        self.assertEqual([], self.service.tarefas())
        self.assertEqual(original, self.storage.arquivo.read_bytes())
        self.assertFalse(list(Path(self.temp.name).glob("*.tmp")))

    def test_external_change_detected(self):
        second = TaskService(Storage(self.temp.name))
        self.service.salvar("tarefas", tarefa())
        with self.assertRaises(StorageError):
            second.salvar("tarefas", tarefa())

    def test_name_preserves_records_and_rolls_back_on_failure(self):
        self.service.salvar("tarefas", tarefa())
        self.assertEqual("", self.service.nome_usuario)
        self.service.salvar_nome("João")
        restored = TaskService(Storage(self.temp.name))
        self.assertEqual("João", restored.nome_usuario)
        self.assertEqual(1, len(restored.tarefas()))
        with self.assertRaises(ValueError):
            self.service.salvar_nome("a" * 61)
        with patch("storage.os.replace", side_effect=PermissionError("Falha simulada")):
            with self.assertRaises(StorageError):
                self.service.salvar_nome("Maria")
        self.assertEqual("João", self.service.nome_usuario)

    def test_portable_path_and_persistence(self):
        pasta = Path(self.temp.name) / "portatil"
        pasta.mkdir()
        with patch("storage.sys.frozen", True, create=True), patch("storage.sys.executable", str(pasta / "TaskManager.exe")):
            self.assertEqual(pasta.resolve(), diretorio_dados())
            service = TaskService(Storage())
            service.salvar_nome("Ana")
            service.salvar("tarefas", tarefa())
            restored = TaskService(Storage())
            self.assertEqual("Ana", restored.nome_usuario)
            self.assertEqual(1, len(restored.tarefas()))
            self.assertTrue((pasta / "dados.json").is_file())

    def test_development_keeps_appdata(self):
        with patch("storage.sys.frozen", False, create=True), patch.dict("storage.os.environ", {"APPDATA": self.temp.name}):
            self.assertEqual(Path(self.temp.name) / "TaskManager", diretorio_dados())


if __name__ == "__main__":
    unittest.main()
