(EN)

# TaskManager

A Portuguese-language desktop manager for tasks and appointments, built with **Python, Tkinter, and ttk**. It runs entirely locally, requiring no server, database, or internet connection.

## Features

* **Dashboard**: Includes real-time counters, pending tasks, and upcoming appointments.
* **Task Management**: Register, edit, complete, and delete tasks with confirmation prompts.
* **Search & Filters**: Search by title/assignee and apply combined filters for priority and status.
* **Schedule**: Chronological schedule with registration, editing, deletion, and an option to view history.
* **Validations**: Validates dates, times, and mandatory fields; syncs task status directly with the checkbox.
* **Data Safety**: Automatically saves to UTF-8 JSON and recovers invalid files while preserving a backup copy.
* **UI/UX**: Resizable interface, scrollable tables, and a settings panel to configure the data path.

## How to Use

1. **First-time Setup**: When opening the app for the first time, enter your name and click *Começar* (Start). Your name will appear in the top-right corner and is saved to the same JSON file without affecting existing tasks.
2. **Subsequent Launches**: The program skips the setup and goes directly to the Dashboard. 
3. **Changing User Name**: Go to *Configurações* (Settings) → *Salvar nome* (Save name). There is no username or password required.
4. **Managing Tasks**: In *Tarefas* (Tasks), click *+ Nova tarefa* (+ New task), fill out the form, and save. Date and time use the DD/MM/YYYY and HH:MM formats. Assignee and description fields are optional.
5. **Editing/Deleting**: Select a row to edit, complete, or delete; double-clicking a row also opens the editor. 
6. **Filtering**: Combine the three available filters to refine the table view.
7. **Pending Tasks**: The Dashboard's pending count includes both *Pendente* (Pending) and *Em andamento* (In Progress) states, including overdue tasks.
8. **Schedule Management**: In *Agenda* (Schedule), register appointments and check *Incluir compromissos passados* (Include past appointments) to view your history. Upcoming appointments include the current minute.
9. **Real-time Updates**: The Dashboard and Schedule refresh automatically every minute to account for the passage of time.
10. **Shortcuts**: In forms, press `Ctrl+Enter` to save and `Esc` to cancel (asking for confirmation if there are unsaved changes). The *Limpar* (Clear) button resets fields without deleting the record currently being edited.

## Data Persistence

The executable is fully **portable**: user name, tasks, and appointments are stored in a `dados.json` file located right next to the `.exe`, regardless of your terminal's working directory. 

**Important:** Extract the entire ZIP file into a folder with write permissions (such as *Documents*) before running the program. To move your data, close the application and copy the entire folder.

## Structure

| File / Folder | Responsibility |
| :--- | :--- |
| `main.py` | Initialization and error handling when loading data |
| `interface.py` | Main window, pages, and forms |
| `service.py` | CRUD operations, filters, schedule, and counters |
| `storage.py` | Secure read/write operations and invalid JSON preservation |
| `utils.py` | Validations, constants, and time conversions |
| `tests/` | Unit tests for business rules, persistence, and interface |
| `TaskManager.spec`, `build.bat`, `requirements.txt` | Windows build configuration |
| `package_release.py` | Script to generate the distribution ZIP with an empty JSON |


(PT)

# TaskManager

Gerenciador desktop de tarefas e compromissos em português, feito com Python,
Tkinter e ttk. Funciona localmente, sem servidor, banco de dados ou conexão com a internet.

## Funcionalidades

- Dashboard com contadores reais, tarefas pendentes e compromissos futuros.
- Cadastro, edição, conclusão e exclusão de tarefas com confirmação.
- Pesquisa por título/responsável e filtros combinados por prioridade e status.
- Agenda cronológica com cadastro, edição, exclusão e opção de mostrar o histórico.
- Validação de datas, horários e campos obrigatórios; status sincronizado com o checkbox.
- Salvamento automático em JSON UTF-8 e recuperação de arquivos inválidos com cópia preservada.
- Interface redimensionável, tabelas com rolagem e configuração com caminho dos dados.

## Como utilizar

Na primeira abertura, informe seu nome e clique em **Começar**. O nome aparece no
canto superior direito e fica salvo no mesmo JSON, sem alterar tarefas existentes.
Nas próximas aberturas, o programa vai direto ao Dashboard. Para trocar o nome,
use **Configurações → Salvar nome**. Não há login nem senha.

Em **Tarefas**, clique em **+ Nova tarefa**, preencha o formulário e salve.
Data e horário usam `DD/MM/AAAA` e `HH:MM`. Responsável e descrição são opcionais.
Selecione uma linha para editar, concluir ou excluir; duplo clique também abre a edição.
Combine os três filtros para refinar a tabela. **Pendentes** no Dashboard inclui
os estados Pendente e Em andamento, inclusive tarefas atrasadas.

Em **Agenda**, cadastre compromissos e use **Incluir compromissos passados** para
consultar o histórico. Os compromissos futuros incluem o minuto atual.
O Dashboard e a agenda também atualizam a passagem do tempo a cada minuto.
Nos formulários, `Ctrl+Enter` salva e `Esc` cancela, confirmando o descarte quando há alterações.
**Limpar** redefine os campos sem excluir o registro em edição.

## Persistência dos dados

O executável é portátil: nome, tarefas e compromissos ficam em `dados.json` ao lado
do `.exe`, independentemente do diretório do terminal. Extraia todo o ZIP para uma
pasta com permissão de gravação (por exemplo, Documentos) antes de abrir o programa.
Para transportar seus dados, feche o aplicativo e leve a pasta inteira.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Inicialização e tratamento de erro ao abrir os dados |
| `interface.py` | Janela principal, páginas e formulários |
| `service.py` | CRUD, filtros, agenda e contadores |
| `storage.py` | Leitura, escrita segura e preservação de JSON inválido |
| `utils.py` | Validação, constantes e conversão temporal |
| `tests/` | Testes de regras, persistência e interface |
| `TaskManager.spec`, `build.bat`, `requirements.txt` | Build Windows |
| `package_release.py` | ZIP de distribuição com JSON vazio |

