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

## Executar em desenvolvimento

Use Python 3.11 ou superior com Tcl/Tk (incluído na instalação oficial para Windows).
Na pasta do projeto:

```console
python main.py
```

A aplicação não precisa instalar dependências externas. A implementação foi testada
com Python 3.14 no Windows. Resolução recomendada: 1100 × 700 ou maior;
a janela permite redução até 850 × 580.

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

Em desenvolvimento (`python main.py`), o local permanece
`%APPDATA%\TaskManager\dados.json`; fora do Windows, o fallback é `~/.config/TaskManager`.
O caminho efetivamente usado aparece em **Configurações**.
Para migrar da versão anterior, copie o JSON do AppData para a pasta do executável,
com o programa fechado e uma cópia de segurança guardada. Nenhum dado é migrado
automaticamente. Ao atualizar, substitua somente o executável, preservando seu JSON.

A primeira execução cria listas vazias. Cada alteração é gravada primeiro em um
arquivo temporário na mesma pasta e depois substitui o JSON. Uma falha de gravação
não aplica a alteração em memória. IDs incrementais são preservados após exclusões.
JSON inválido é copiado para `dados.corrompidos-<data-hora>.json` antes de reiniciar
as listas; o programa avisa onde a cópia foi salva. Não há recuperação automática
dos registros dessa cópia. Se o backup falhar, a inicialização é interrompida.

Para backup/restauração, feche a aplicação e copie/substitua `dados.json`.
Use uma instância por vez; alterações externas detectadas bloqueiam o salvamento
até reabrir o programa. Não há sincronização simultânea entre instâncias.

## Testes

```console
python -m unittest discover -s tests -v
```

Os testes usam pastas temporárias, sem dados fictícios na pasta do usuário.
Incluem CRUD, IDs, contadores, filtros, validação, agenda, reabertura,
JSON inválido, falha de escrita e operações reais dos widgets Tkinter.
O teste de interface requer uma sessão gráfica e abre janelas brevemente.

## Gerar o executável Windows

```console
build.bat
```

O script cria `.venv`, instala o PyInstaller, executa os testes e gera
**`dist\portatil\TaskManager.exe`**, em arquivo único e sem console, e o pacote
**`dist\TaskManager-portatil.zip`** com executável, JSON vazio e instruções. A primeira instalação
das ferramentas de build requer internet. O executável resultante não requer Python
instalado nem internet. O arquivo `.spec` inclui automaticamente Tcl/Tk pelo hook
do PyInstaller; `build_support.py` complementa a coleta de bibliotecas embutidas
via zipfs nas distribuições com Tcl/Tk 9. O pacote não embute dados pessoais.

Para compilar diretamente após instalar `requirements.txt`:

```console
.venv\Scripts\python.exe -m PyInstaller --noconfirm --workpath build\portatil --distpath dist\portatil TaskManager.spec
python package_release.py
```

Gere o executável no Windows para a arquitetura de destino. O binário desta entrega
é Windows x64. Windows 10/11 são os alvos; a validação local não substitui um teste
em uma máquina limpa de cada versão do Windows.

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

## Publicação

Publique no GitHub o código, os testes e a documentação. O `.gitignore` exclui
ambiente virtual, arquivos de build, distribuição e dados pessoais. Distribua
`dist/TaskManager-portatil.zip` pelo link de download escolhido. O pacote é criado
com dados vazios, sem copiar o nome ou os registros do desenvolvedor.
