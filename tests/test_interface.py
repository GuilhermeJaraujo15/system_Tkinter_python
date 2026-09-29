import tempfile
import unittest
from unittest.mock import patch

from interface import RecordForm, TaskManagerApp
from service import TaskService
from storage import Storage


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = TaskManagerApp(TaskService(Storage(self.temp.name)))
        self.addCleanup(self.app.destroy)
        self.app.update()

    def test_gui_workflow(self):
        app = self.app
        app.nome_digitado.set("Ana")
        app.salvar_nome(inicial=True)
        app.show("Tarefas")
        with patch("interface.messagebox.showwarning") as warning:
            app.action("tarefas", "editar")
            warning.assert_called_once()
        form = RecordForm(app, "tarefas")
        app.update()
        with patch("interface.messagebox.showwarning") as warning:
            form.salvar()
            warning.assert_called_once()
        form.vars["titulo"].set("Teste de interface")
        form.vars["status"].set("Concluída")
        self.assertTrue(form.concluida.get())
        form.concluida.set(False)
        form.toggle()
        self.assertEqual("Pendente", form.vars["status"].get())
        form.salvar()
        self.assertEqual(("1",), app.tree.get_children())
        app.tree.selection_set("1")
        app.action("tarefas", "editar")
        form = next(w for w in app.winfo_children() if isinstance(w, RecordForm))
        form.vars["titulo"].set("Título editado")
        form.salvar()
        self.assertEqual("Título editado", app.service.obter("tarefas", 1)["titulo"])
        app.search.set("inexistente")
        self.assertEqual((), app.tree.get_children())
        app.search.set("EDITADO")
        app.priority.set("Média")
        app.status.set("Pendente")
        self.assertEqual(("1",), app.tree.get_children())
        app.tree.selection_set("1")
        app.action("tarefas", "concluir")
        self.assertEqual((1, 0, 1), app.service.contadores())
        self.assertEqual((), app.tree.get_children())
        app.status.set("Todos")
        app.tree.selection_set("1")
        with patch("interface.messagebox.askyesno", return_value=False):
            app.action("tarefas", "excluir")
        self.assertEqual(1, len(app.service.tarefas()))
        with patch("interface.messagebox.askyesno", return_value=True):
            app.action("tarefas", "excluir")
        self.assertEqual((), app.tree.get_children())
        app.show("Agenda")
        form = RecordForm(app, "agendamentos")
        form.vars["titulo"].set("Reunião")
        form.vars["data"].set("01/01/2099")
        form.salvar()
        self.assertEqual(("1",), app.tree.get_children())
        form = RecordForm(app, "tarefas")
        form.vars["titulo"].set("Limpar")
        form.limpar()
        self.assertEqual("", form.vars["titulo"].get())
        form.cancelar()
        for page in ("Início", "Configurações", "Tarefas", "Agenda"):
            app.show(page)
            app.geometry("850x580")
            app.update()
            self.assertEqual(page, app.current)
        restored = TaskService(Storage(self.temp.name))
        self.assertEqual((0, 0, 0), restored.contadores())
        self.assertEqual(1, len(restored.agenda()))

    def test_welcome_and_saved_name(self):
        app = self.app
        self.assertEqual("Boas-vindas", app.current)
        self.assertEqual("Bem-vindo", app.saudacao.get())
        app.show("Tarefas")
        self.assertEqual("Boas-vindas", app.current)
        with patch("interface.messagebox.showwarning") as warning:
            app.nome_digitado.set("   ")
            app.salvar_nome(inicial=True)
            warning.assert_called_once()
        app.nome_digitado.set("  João   Silva  ")
        app.salvar_nome(inicial=True)
        self.assertEqual("Início", app.current)
        self.assertEqual("Olá, João Silva", app.saudacao.get())
        restored = TaskService(Storage(self.temp.name))
        self.assertEqual("João Silva", restored.nome_usuario)
        app.show("Configurações")
        app.nome_digitado.set("Maria")
        app.salvar_nome()
        self.assertEqual("Olá, Maria", app.saudacao.get())


if __name__ == "__main__":
    unittest.main()
