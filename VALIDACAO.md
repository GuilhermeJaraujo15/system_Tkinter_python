# Validação da entrega

Ambiente: Windows 11 x64, Python 3.14.7, PyInstaller 6.22.3.

- `python -m unittest discover -s tests -v`: 14 testes aprovados após inclusão do nome e modo portátil.
- Boas-vindas com nome obrigatório, saudação personalizada, alteração em Configurações
  e reabertura do nome salvo. Compatibilidade com JSON antigo, preservação das tarefas
  e falha de escrita do nome também verificadas.
- Fluxo da interface executado em widgets reais: cadastro, validação de título,
  edição mantendo ID, sincronização status/checkbox, pesquisa e filtros,
  conclusão, cancelamento/confirmação de exclusão, agenda, limpeza e navegação.
- Regras testadas: datas/horários inválidos, prioridades/status, IDs após exclusão,
  contadores, ordenação cronológica e persistência ao criar outra instância do serviço.
- Persistência testada: arquivo ausente/vazio, JSON inválido e estrutura inválida,
  cópia do arquivo corrompido, alteração externa e falha de escrita simulada.
- `python main.py`: janela TaskManager aberta e encerrada, sem saída de erro.
- `dist/TaskManager.exe`: aberto, fechado normalmente e reaberto com sucesso.
  Dashboard inspecionado visualmente; arquivo JSON vazio criado na pasta isolada
  `build/smoke-data/TaskManager` durante a validação.
- Binário confirmado com subsistema PE Windows GUI (2), sem console.
- Formulário de tarefas conferido em 560 × 570, sem widgets ultrapassando o limite inferior.
- Navegação testada com janela reduzida para 850 × 580.

A primeira compilação revelou ausência dos scripts Tcl/Tk 9 embutidos em zipfs.
`build_support.py` corrige a coleta e a segunda compilação foi validada executando
o binário. Os avisos restantes do PyInstaller listam imports opcionais/plataformas
alternativas e `collections.abc`; não impediram a inicialização validada.

Não foi realizado teste em outra máquina sem Python nem em Windows 10.
Os testes de CRUD completos foram executados pela interface em Python; no binário,
foi validada inicialização, criação do armazenamento, encerramento e reabertura.
Todos os registros fictícios ficaram isolados em diretórios temporários dos testes.

## Distribuição portátil

- Executável recompilado em `dist/portatil/TaskManager.exe`.
- `dist/TaskManager-portatil.zip` contém o executável, JSON vazio e instruções.
- Integridade do ZIP e ausência de dados pessoais no JSON verificadas.
- Executável extraído aberto com diretório de trabalho diferente da sua pasta.
  A janela respondeu e encerrou normalmente; um JSON ausente foi criado ao lado
  do executável, sem usar AppData.
- Testes de serviço verificam nome e tarefas preservados ao reabrir no modo portátil.
  Execução por `python main.py` continua usando o AppData.
