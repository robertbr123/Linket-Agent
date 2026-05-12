# Latest session handoff

Updated: 2026-05-12T04:53:05.625Z
Session: ses_1e799fa38ffewE2X30zOrwuWxl
Message: msg_e1a87c645001xit8HYURskHPX3

## User Request
como eu ja tinha instalado antes desse update eu devo rodar irm https://raw.githubusercontent.com/robertbr123/Linket-Agent/refs/heads/main/scripts/install.ps1 | iex no meu windows denovo para atualizar com esses novos updates?

## Assistant Result
Não precisa `obrigatoriamente`.

Melhor ordem:

1. Tente primeiro:
```powershell
linket update
```

2. Reinstale com:
```powershell
irm https://raw.githubusercontent.com/robertbr123/Linket-Agent/refs/heads/main/scripts/install.ps1 | iex
```
só se acontecer um destes casos:
- `linket update` falhar
- sua instalação estiver sem `.git`
- o update cair no fallback antigo do Windows
- você quiser o caminho mais “limpo” para garantir tudo atualizado

Minha leitura hoje:
- se sua instalação atual é um checkout git normal, `linket update` deve bastar para puxar esse fix
- no Windows, se você quiser evitar surpresa com o update antigo que estava aí antes, rodar o `install.ps1` de novo é um caminho seguro também

Resumo curto:
- `normalmente`: use `linket update`
- `se quiser o caminho mais seguro no Windows`: pode rodar o `install.ps1` de novo

Se quiser, eu posso te dizer `qual dos dois eu recomendo no seu caso exato` se você me mostrar o que sai de:
```powershell
linket --version
git -C "$HOME\\.linket\\linket-agent" remote -v
```

## Changed Files
(none)
