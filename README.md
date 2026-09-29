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

