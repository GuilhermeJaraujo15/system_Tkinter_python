"""Telas e formulários Tkinter do TaskManager."""
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from storage import StorageError
from utils import PRIORIDADES, STATUS

BG = "#f3f5f9"
INK = "#18263d"
BLUE = "#2563eb"


class RecordForm(tk.Toplevel):
    def __init__(self, app, tipo, registro=None):
        super().__init__(app)
        self.app, self.tipo, self.registro = app, tipo, registro
        self.title(("Editar " if registro else "Novo cadastro — ") + ("tarefa" if tipo == "tarefas" else "compromisso"))
        self.configure(bg=BG)
        self.transient(app)
        self.resizable(True, True)
        self.minsize(480, 510)
        self.geometry(f"560x570+{app.winfo_rootx() + 100}+{max(0, app.winfo_rooty() + 25)}")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        corpo = ttk.Frame(self, padding=22)
        corpo.grid(sticky="nsew")
        corpo.columnconfigure(0, weight=1)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(7, weight=1)
        self.vars = {}
        self.inputs = {}
        self.field(corpo, "titulo", "Título *", 0, 0, span=2)
        extra = "responsavel" if tipo == "tarefas" else "local"
        self.field(corpo, extra, "Responsável" if tipo == "tarefas" else "Local", 2, 0, span=2)
        self.field(corpo, "data", "Data * (DD/MM/AAAA)", 4, 0)
        self.field(corpo, "horario", "Horário * (HH:MM)", 4, 1)
        ttk.Label(corpo, text="Descrição").grid(row=6, column=0, sticky="w", pady=(10, 4))
        self.descricao = tk.Text(corpo, height=4, wrap="word", font=("Segoe UI", 10), relief="solid", bd=1, undo=True)
        self.descricao.grid(row=7, column=0, columnspan=2, sticky="nsew")
        if tipo == "tarefas":
            self.field(corpo, "prioridade", "Prioridade *", 8, 0, choices=PRIORIDADES)
            self.field(corpo, "status", "Status *", 8, 1, choices=STATUS)
            self.concluida = tk.BooleanVar(self)
            tk.Checkbutton(corpo, text="Marcar tarefa como concluída", variable=self.concluida,
                           command=self.toggle, bg=BG, activebackground=BG,
                           font=("Segoe UI", 10)).grid(row=10, column=0, columnspan=2, sticky="w", pady=10)
            self.vars["status"].trace_add("write", self.sync)
        acoes = ttk.Frame(corpo)
        acoes.grid(row=11, column=0, columnspan=2, sticky="e", pady=(16, 0))
        ttk.Button(acoes, text="Cancelar", command=self.cancelar).pack(side="left", padx=4)
        ttk.Button(acoes, text="Limpar", command=self.limpar).pack(side="left", padx=4)
        ttk.Button(acoes, text="Salvar tarefa" if tipo == "tarefas" else "Agendar" if not registro else "Salvar compromisso",
                   style="Primary.TButton", command=self.salvar).pack(side="left", padx=4)
        self.limpar()
        if registro:
            for campo, var in self.vars.items():
                var.set(registro[campo])
            self.descricao.insert("1.0", registro["descricao"])
        self.original = self.valores()
        self.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.bind("<Escape>", lambda event: self.cancelar())
        self.bind("<Control-Return>", lambda event: self.salvar())
        self.grab_set()
        self.after(60, self.inputs["titulo"].focus_set)

    def field(self, parent, campo, label, row, col, span=1, choices=None):
        ttk.Label(parent, text=label).grid(row=row, column=col, columnspan=span, sticky="w", pady=(10, 4))
        var = tk.StringVar(self)
        self.vars[campo] = var
        if choices:
            widget = ttk.Combobox(parent, textvariable=var, values=choices, state="readonly")
        else:
            widget = tk.Entry(parent, textvariable=var, font=("Segoe UI", 11), relief="solid", bd=1)
        widget.grid(row=row + 1, column=col, columnspan=span, sticky="ew", ipady=4, padx=(0, 8 if span == 1 and col == 0 else 0))
        self.inputs[campo] = widget

    def toggle(self):
        self.vars["status"].set("Concluída" if self.concluida.get() else "Pendente")

    def sync(self, *_):
        self.concluida.set(self.vars["status"].get() == "Concluída")

    def limpar(self):
        for var in self.vars.values():
            var.set("")
        self.vars["data"].set(datetime.now().strftime("%d/%m/%Y"))
        self.vars["horario"].set("09:00")
        if self.tipo == "tarefas":
            self.vars["prioridade"].set("Média")
            self.vars["status"].set("Pendente")
        self.descricao.delete("1.0", "end")
        self.inputs["titulo"].focus_set()

    def valores(self):
        return {**{key: var.get() for key, var in self.vars.items()}, "descricao": self.descricao.get("1.0", "end-1c")}

    def cancelar(self):
        if self.valores() != self.original and not messagebox.askyesno("Descartar alterações", "Descartar as alterações deste formulário?", parent=self):
            return
        self.destroy()

    def salvar(self):
        try:
            self.app.service.salvar(self.tipo, self.valores(), self.registro["id"] if self.registro else None)
        except ValueError as erro:
            messagebox.showwarning("Confira os campos", str(erro), parent=self)
            return
        except StorageError as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self)
            return
        self.app.refresh()
        self.app.feedback.set("Tarefa salva com sucesso." if self.tipo == "tarefas" else "Compromisso salvo com sucesso.")
        self.destroy()


class TaskManagerApp(tk.Tk):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.title("TaskManager")
        self.configure(bg=BG)
        width, height = min(1100, self.winfo_screenwidth()), min(700, self.winfo_screenheight() - 60)
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{max(0, (self.winfo_screenheight()-height)//2-25)}")
        self.minsize(850, 580)
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.style()
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        header = tk.Frame(self, bg="white", padx=24, pady=14)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(header, text="TaskManager", bg="white", fg=INK, font=("Segoe UI", 19, "bold")).pack(side="left")
        self.saudacao = tk.StringVar(self, f"Olá, {service.nome_usuario}" if service.nome_usuario else "Bem-vindo")
        tk.Label(header, textvariable=self.saudacao, bg="white", fg="#64748b", font=("Segoe UI", 10)).pack(side="right")
        sidebar = tk.Frame(self, bg=INK, width=176, padx=12, pady=25)
        sidebar.grid(row=1, column=0, rowspan=2, sticky="ns")
        sidebar.grid_propagate(False)
        self.nav = {}
        for i, nome in enumerate(("Início", "Tarefas", "Agenda", "Configurações")):
            button = tk.Button(sidebar, text=nome, anchor="w", width=17, padx=12, pady=12,
                               relief="flat", bd=0, fg="white", bg=INK, activebackground=BLUE,
                               activeforeground="white", font=("Segoe UI", 11), cursor="hand2",
                               command=lambda nome=nome: self.show(nome))
            button.grid(row=i, column=0, sticky="ew", pady=3)
            button.bind("<Enter>", lambda event, nome=nome: self.nav[nome].configure(bg=BLUE if self.current == nome else "#2c3e58"))
            button.bind("<Leave>", lambda event, nome=nome: self.nav[nome].configure(bg=BLUE if self.current == nome else INK))
            self.nav[nome] = button
        self.content = ttk.Frame(self, padding=24)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.feedback = tk.StringVar(self, "Tudo pronto. Seus dados são salvos após cada alteração.")
        ttk.Label(self, textvariable=self.feedback, padding=(24, 8)).grid(row=2, column=1, sticky="ew")
        self.search = tk.StringVar(self)
        self.priority = tk.StringVar(self, "Todas")
        self.status = tk.StringVar(self, "Todos")
        self.historico = tk.BooleanVar(self, False)
        for var in (self.search, self.priority, self.status):
            var.trace_add("write", lambda *_: self.fill_tasks() if self.current == "Tarefas" else None)
        self.current = ""
        self.show("Início")
        self.after(1000, self.tick)
        if service.storage.aviso:
            self.after(100, lambda: messagebox.showwarning("Dados recuperados", service.storage.aviso, parent=self))

    def style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=INK)
        style.configure("Heading.TLabel", font=("Segoe UI", 23, "bold"))
        style.configure("Muted.TLabel", foreground="#64748b")
        style.configure("TButton", padding=(12, 8))
        style.configure("Primary.TButton", background=BLUE, foreground="white")
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("Treeview", rowheight=33, background="white", fieldbackground="white", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview", background=[("selected", BLUE)], foreground=[("selected", "white")])

    def show(self, nome):
        if not self.service.nome_usuario:
            self.welcome()
            return
        self.current = nome
        for key, button in self.nav.items():
            button.configure(bg=BLUE if key == nome else INK)
        for child in self.content.winfo_children():
            child.destroy()
        ttk.Label(self.content, text=nome, style="Heading.TLabel").pack(anchor="w")
        {"Início": self.dashboard, "Tarefas": self.tasks_page, "Agenda": self.agenda_page,
         "Configurações": self.settings}[nome]()

    def welcome(self):
        self.current = "Boas-vindas"
        for child in self.content.winfo_children():
            child.destroy()
        ttk.Label(self.content, text="Bem-vindo ao TaskManager", style="Heading.TLabel").pack(anchor="w", pady=(24, 12))
        ttk.Label(self.content, text="Como você gostaria de ser chamado?\nInforme seu nome para começar. Ele será lembrado nas próximas aberturas.",
                  style="Muted.TLabel").pack(anchor="w", pady=(0, 24))
        self.name_field("Começar", inicial=True)
        self.feedback.set("Preencha seu nome para começar.")

    def name_field(self, button_text, inicial=False):
        ttk.Label(self.content, text="Seu nome (até 60 caracteres)").pack(anchor="w", pady=(12, 4))
        self.nome_digitado = tk.StringVar(self, self.service.nome_usuario)
        entry = ttk.Entry(self.content, textvariable=self.nome_digitado, width=40)
        entry.pack(anchor="w", ipady=5)
        ttk.Button(self.content, text=button_text, style="Primary.TButton",
                   command=lambda: self.salvar_nome(inicial)).pack(anchor="w", pady=12)
        entry.bind("<Return>", lambda event: self.salvar_nome(inicial))
        if inicial:
            entry.focus_set()

    def salvar_nome(self, inicial=False):
        try:
            self.service.salvar_nome(self.nome_digitado.get())
        except ValueError as erro:
            messagebox.showwarning("Confira seu nome", str(erro), parent=self)
            return
        except StorageError as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self)
            return
        self.saudacao.set(f"Olá, {self.service.nome_usuario}")
        self.feedback.set("Nome salvo com sucesso.")
        if inicial:
            self.show("Início")

    def refresh(self):
        if self.current == "Tarefas":
            self.fill_tasks()
        elif self.current == "Agenda":
            self.fill_agenda()
        else:
            self.show(self.current)

    def tick(self):
        if self.current in ("Início", "Agenda"):
            self.refresh()
        self.after(60000, self.tick)

    def dashboard(self):
        ttk.Label(self.content, text="Uma visão geral do seu trabalho e dos próximos compromissos.", style="Muted.TLabel").pack(anchor="w", pady=(4, 20))
        cards = ttk.Frame(self.content)
        cards.pack(fill="x")
        for i, (label, value) in enumerate(zip(("Total de tarefas", "Pendentes", "Concluídas"), self.service.contadores())):
            cards.columnconfigure(i, weight=1)
            card = tk.Frame(cards, bg="white", padx=20, pady=14, highlightthickness=1, highlightbackground="#e2e8f0")
            card.grid(row=0, column=i, sticky="ew", padx=(0, 12 if i < 2 else 0))
            tk.Label(card, text=str(value), bg="white", fg=BLUE, font=("Segoe UI", 28, "bold")).pack(anchor="w")
            tk.Label(card, text=label, bg="white", fg=INK, font=("Segoe UI", 11)).pack(anchor="w")
        ttk.Label(self.content, text="Pendentes inclui tarefas em andamento.", style="Muted.TLabel").pack(anchor="w", pady=(8, 5))
        for titulo, registros, command in (
            ("Próximas tarefas", [r for r in self.service.tarefas() if r["status"] != "Concluída"][:3], lambda: self.show("Tarefas")),
            ("Próximos compromissos", self.service.agenda()[:3], lambda: self.show("Agenda"))):
            row = ttk.Frame(self.content)
            row.pack(fill="x", pady=(12, 4))
            ttk.Label(row, text=titulo, font=("Segoe UI", 13, "bold")).pack(side="left")
            ttk.Button(row, text="Ver todos", command=command).pack(side="right")
            if not registros:
                ttk.Label(self.content, text="Nenhum registro para exibir.", style="Muted.TLabel").pack(anchor="w", pady=5)
            for registro in registros:
                text = f'{registro["data"]}  {registro["horario"]}   •   {registro["titulo"]}'
                ttk.Label(self.content, text=text, anchor="w").pack(fill="x", pady=3)

    def toolbar(self, tipo):
        bar = ttk.Frame(self.content)
        bar.pack(fill="x", pady=(16, 12))
        ttk.Button(bar, text="+ Nova tarefa" if tipo == "tarefas" else "+ Novo compromisso", style="Primary.TButton",
                   command=lambda: RecordForm(self, tipo)).pack(side="left", padx=(0, 8))
        for text, action in (("Editar", "editar"), ("Concluir", "concluir"), ("Excluir", "excluir")):
            if tipo != "tarefas" and action == "concluir":
                continue
            ttk.Button(bar, text=text, command=lambda action=action: self.action(tipo, action)).pack(side="left", padx=4)

    def table(self, columns):
        frame = ttk.Frame(self.content)
        frame.pack(fill="both", expand=True, pady=(12, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings", selectmode="browse")
        for key, title, width in columns:
            tree.heading(key, text=title)
            tree.column(key, width=width, minwidth=width, stretch=key in ("titulo", "local", "responsavel"), anchor="w")
        tree.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        horizontal.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tree.tag_configure("Concluída", foreground="#47745d")
        tree.tag_configure("Alta", foreground="#a44032")
        self.count = tk.StringVar(self)
        ttk.Label(self.content, textvariable=self.count, style="Muted.TLabel").pack(anchor="w", pady=(8, 0))
        return tree

    def tasks_page(self):
        self.toolbar("tarefas")
        filters = ttk.Frame(self.content)
        filters.pack(fill="x")
        filters.columnconfigure(0, weight=1)
        for i, (label, var, choices) in enumerate((("Pesquisar título ou responsável", self.search, None),
                    ("Prioridade", self.priority, ("Todas", *PRIORIDADES)), ("Status", self.status, ("Todos", *STATUS)))):
            ttk.Label(filters, text=label).grid(row=0, column=i, sticky="w")
            widget = ttk.Combobox(filters, textvariable=var, values=choices, state="readonly", width=16) if choices else ttk.Entry(filters, textvariable=var)
            widget.grid(row=1, column=i, sticky="ew", padx=(0, 8), pady=(4, 0))
        self.tree = self.table((("id", "ID", 45), ("titulo", "Tarefa", 190), ("responsavel", "Responsável", 115),
                                ("prioridade", "Prioridade", 85), ("data", "Data", 100), ("horario", "Horário", 70), ("status", "Status", 115)))
        self.tree.bind("<Double-1>", lambda event: self.action("tarefas", "editar") if self.tree.identify_row(event.y) else None)
        self.tree.bind("<Return>", lambda event: self.action("tarefas", "editar"))
        self.fill_tasks()

    def fill(self, registros):
        selection = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        for item in registros:
            self.tree.insert("", "end", iid=str(item["id"]), values=[item[key] for key in self.tree["columns"]],
                             tags=(item.get("status") if item.get("status") == "Concluída" else item.get("prioridade", ""),))
        if selection and self.tree.exists(selection[0]):
            self.tree.selection_set(selection[0])
        self.count.set(f"{len(registros)} registro(s) exibido(s)." if registros else "Nenhum registro encontrado. Cadastre um item ou ajuste os filtros.")

    def fill_tasks(self):
        self.fill(self.service.tarefas(self.search.get(), self.priority.get(), self.status.get()))

    def agenda_page(self):
        self.toolbar("agendamentos")
        ttk.Label(self.content, text="Próximos agendamentos • em ordem cronológica", style="Muted.TLabel").pack(anchor="w")
        ttk.Checkbutton(self.content, text="Incluir compromissos passados", variable=self.historico,
                        command=self.fill_agenda).pack(anchor="w", pady=(8, 0))
        self.tree = self.table((("id", "ID", 45), ("data", "Data", 100), ("horario", "Horário", 75),
                                ("titulo", "Compromisso", 230), ("local", "Local", 160)))
        self.tree.bind("<Double-1>", lambda event: self.action("agendamentos", "editar") if self.tree.identify_row(event.y) else None)
        self.fill_agenda()

    def fill_agenda(self):
        self.fill(self.service.agenda(futuros=not self.historico.get()))

    def action(self, tipo, action):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selecione um registro", "Selecione uma tarefa primeiro." if tipo == "tarefas" else "Selecione um compromisso primeiro.", parent=self)
            return
        identificador = int(selection[0])
        try:
            if action == "editar":
                RecordForm(self, tipo, self.service.obter(tipo, identificador))
                return
            if action == "excluir":
                registro = self.service.obter(tipo, identificador)
                if not messagebox.askyesno("Excluir registro", f'Excluir “{registro["titulo"]}”? Esta ação não pode ser desfeita.', parent=self):
                    return
                self.service.excluir(tipo, identificador)
                self.feedback.set("Registro excluído.")
            elif action == "concluir":
                if not self.service.concluir(identificador):
                    messagebox.showinfo("Tarefa concluída", "Esta tarefa já está concluída.", parent=self)
                self.feedback.set("Tarefa concluída.")
            self.refresh()
        except (ValueError, StorageError) as erro:
            messagebox.showerror("Operação não realizada", str(erro), parent=self)

    def settings(self):
        self.name_field("Salvar nome")
        for text in ("TaskManager • Versão 1.0.0", "Gerenciador local de tarefas e compromissos.",
                     "Tecnologias: Python, Tkinter e ttk. Não requer conexão com a internet.",
                     "Armazenamento dos dados:"):
            ttk.Label(self.content, text=text, wraplength=620).pack(anchor="w", pady=(8, 0))
        path = ttk.Entry(self.content)
        path.insert(0, str(self.service.storage.arquivo))
        path.configure(state="readonly")
        path.pack(fill="x", pady=10)
        ttk.Label(self.content, text="Os dados são salvos automaticamente após cada alteração.\nPara fazer backup, feche o programa e copie dados.json para um local seguro.\nPara restaurar, feche o programa e substitua esse arquivo pelo backup.\nUse apenas uma instância do programa por vez.",
                  wraplength=620, style="Muted.TLabel").pack(anchor="w", pady=10)

    def fechar(self):
        for child in self.winfo_children():
            if isinstance(child, RecordForm):
                child.cancelar()
                if child.winfo_exists():
                    return
        self.destroy()
