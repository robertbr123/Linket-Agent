# Latest session handoff

Updated: 2026-05-12T03:30:01.856Z
Session: ses_1e799fa38ffewE2X30zOrwuWxl
Message: msg_e1a3921fb001DGscJJaKfNcCml

## User Request
vamos corrigir o update ok

## Assistant Result
Vou corrigir o fluxo de `update` para o fork de forma mínima e segura: primeiro mapear os pontos que ainda assumem `hermes`/upstream, depois ajustar URL, mensagens e comando recomendado, e por fim verificar os resíduos principais.
Já tenho os pontos críticos: o risco real está em `hermes_cli/main.py` e `hermes_cli/config.py`. Vou ajustar o comportamento do update para recomendar `linket update`, usar URLs do fork nos fallbacks e manter a lógica de sync com upstream só onde ela é intencional.
Encontrei o ponto mais perigoso: hoje o repo oficial do `update` ainda é tratado como `NousResearch/hermes-agent`, o que pode fazer um checkout do `Linket` parecer “fork” e puxar lógica de sync indevida. Vou ler só esse trecho final antes do patch para corrigir sem quebrar a intenção de upstream opcional.
Vou checar só um detalhe antes do patch: se existe alguma evidência no repo sobre nome do pacote/fórmula gerenciada (`linket-agent` vs `hermes-agent`) para eu não trocar isso no escuro.
Vou editar os arquivos centrais do update agora: `config.py`, `main.py` e as mensagens públicas relacionadas. A correção principal é fazer o update tratar `Linket-Agent` como repositório canônico e parar de baixar/sugerir o upstream errado no caminho normal.
O patch amplo bateu em contextos que já não casavam exatamente. Vou reabrir só os trechos-alvo e aplicar um patch menor e preciso.
Vou aplicar em blocos menores por arquivo para evitar conflito de contexto.
O núcleo do `update` já foi corrigido: comando recomendado, ZIP fallback, repo oficial detectado e mensagens principais agora apontam para `Linket`. Vou fazer uma verificação focada só na superfície de update para ver o que ainda sobrou e separar o que é compatibilidade interna do que ainda é bug real.
Agora tenho contexto suficiente. Vou ajustar só o que realmente ajuda quem usa `update`: help text do subparser e uma mensagem gerenciada que ainda recomendava `brew upgrade hermes-agent`. հետո encerro com o estado e os resíduos que ficaram fora do escopo.
Corrigi o fluxo principal de `update` para o fork.

Arquivos alterados:
- `hermes_cli/config.py`
- `hermes_cli/main.py`
- `hermes_cli/_parser.py`
- `hermes_cli/commands.py`
- `hermes_cli/setup.py`
- `hermes_cli/plugins_cmd.py`
- `hermes_cli/banner.py`

O que mudou:
- `recommended_update_command()` agora retorna `linket update`
- Homebrew gerenciado agora recomenda `brew upgrade linket-agent`
- `cmd_update()` agora se apresenta como `Update Linket Agent`
- mensagem de execução mudou para `⛓ Updating Linket Agent...`
- fallback de reinstall fora de git agora aponta para `https://linket.com.br/install.sh`
- fallback ZIP no Windows agora baixa do fork:
  - `https://github.com/robertbr123/Linket-Agent/archive/refs/heads/main.zip`
- detecção de repo “oficial” do update agora trata `robertbr123/Linket-Agent` como canônico
- prompts de upstream nesse fluxo agora falam de `Linket repository`
- help text e descrição do comando `update` agora usam `Linket Agent`
- mensagens que o

## Changed Files
(none)
