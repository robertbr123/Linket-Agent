# Linket Agent — Rebrand Plan

Status doc para o rebrand `Hermes Agent` (Nous Research) → `Linket Agent`.
Atualize este arquivo a cada fase concluída. Branch principal do trabalho:
`rebrand/linket`.

## Decisões já travadas

- **Nome:** Linket Agent / pacote pip `linket-agent` / CLI `linket` / runtime `~/.linket/`
- **Domínio público:** `linket.com.br` (install: `https://linket.com.br/install.sh`)
- **Repo:** `github.com/robertbr123/Linket-Agent`
- **Estratégia de migração:** auto-copy `~/.hermes/` → `~/.linket/` no primeiro run (Fase 6)
- **Compat com nome antigo:** comandos `hermes` / `hermes-agent` / `hermes-acp` mantidos como aliases com deprecation warning (Fase 4) — drop após 2 minor releases.
- **Atribuição upstream:** `LICENSE` preserva copyright Nous Research + adiciona fork copyright. `NOTICE.md` completo na Fase 9.

## Status das fases

| Fase | Estado | Commit | Resumo |
|-----:|:------:|:-------|:-------|
| 0 | ✅ | `38ea1ec` | Baseline: snapshot upstream + `.gitignore` |
| 1 | ✅ | `34ef524` | `assets/banner.svg` + `assets/logo-mark.svg`; READMEs apontam pro novo banner |
| 2 | ✅ | `ad00955` | `pyproject.toml`, `package.json`, `flake.nix`, `docker-compose.yml`, `LICENSE` |
| 3 | ✅ | `fc51284` | `install.{sh,ps1,cmd}` repointados; `infra/redirect-worker.js` + guia |
|   – | ✅ | `b943f1b` | Limpeza: ignora duplicatas macOS/iCloud `* 2.*` |
| 4 | ✅ | `3a2a640` | CLI `hermes`→`linket` com deprecation shim; `_legacy_alias.py` |
| 5 | ⏸ adiado | — | **Rename do módulo Python `hermes_cli/` → `linket_cli/`** (ver detalhamento abaixo) |
| 6 | ✅ | `fcb82cf` | Runtime path `~/.linket` default + auto-migração `~/.hermes` → `~/.linket`; `LINKET_HOME` env var |
| 7 | ✅ | `<este>` | Skills, plugins, packaging, website/docs — `git mv` de 10+ paths + 127 cross-refs |
| 8 | ✅ | `<este>` | 580 .md/.mdx files rebranded (mass + manual READMEs); RELEASE_v*.md prefixados com nota histórica |
| 9 | ✅ | `<este>` | `NOTICE.md` com atribuição upstream completa |
| 10 | ⏳ | — | Verificação final (grep residual, imports, smoke test) |

## Tarefas externas (você, fora do código)

Estas dependências **bloqueiam o lançamento público** mas não bloqueiam continuar o código:

- [ ] Criar repo público `github.com/robertbr123/Linket-Agent`
- [ ] `git push origin rebrand/linket` quando estiver pronto pra revisão
- [ ] Mover repo local pra fora do iCloud (sugerido: `~/Code/Linket-Agent`) pra evitar nova rodada de duplicatas " 2.*"
- [ ] Apontar `linket.com.br` pro Cloudflare e deployar `infra/redirect-worker.js` (passo a passo em `infra/README.md`)
- [ ] Verificar redirects: `curl -fsSLI https://linket.com.br/install.sh` deve retornar `302` apontando pra raw.githubusercontent

---

## Fase 5 — Rename do módulo Python (detalhamento)

**Por que está adiada:** sem rodar `pytest` nessa máquina é voar cego em ~600 arquivos. A Fase 4 já entrega tudo que o usuário final vê (`linket` no CLI). O rename do módulo é higiene de codebase, não funcionalidade.

### Superfície real (medida em `b943f1b`)

| Categoria | Arquivos |
|-----------|---------:|
| `.py` que importam `hermes_cli` | 506 |
| `.py` que importam `hermes_state` / `_bootstrap` / `_constants` / `_time` / `_logging` | 214 |
| String-based imports (`importlib.import_module("hermes_cli.main")` etc.) já mapeados | 17 |
| Não-py (`*.yaml`, `*.nix`, `*.md`, `*.sh`, `*.toml`) | 47 |
| **Total estimado** | **~600** |

Arquivos a renomear:

```
hermes_cli/                 → linket_cli/
hermes_state.py             → linket_state.py
hermes_bootstrap.py         → linket_bootstrap.py
hermes_constants.py         → linket_constants.py
hermes_time.py              → linket_time.py
hermes_logging.py           → linket_logging.py
tests/hermes_cli/           → tests/linket_cli/
tests/hermes_state/         → tests/linket_state/
tests/test_hermes_*.py      → tests/test_linket_*.py
environments/hermes_base_env.py → environments/linket_base_env.py
environments/hermes_swe_env/   → environments/linket_swe_env/
environments/tool_call_parsers/hermes_parser.py → linket_parser.py
ui-tui/packages/hermes-ink/    → ui-tui/packages/linket-ink/
ui-tui/src/types/hermes-ink.d.ts → linket-ink.d.ts
```

### Riscos a olhar com lupa

1. **Plugin YAMLs** (`plugins/platforms/*/plugin.yaml`, `plugins/kanban/...`) — referenciam módulos por string. Erro de digitação aqui faz o plugin sumir silenciosamente em runtime sem traceback claro.
2. **String-based imports** — os 17 conhecidos via `importlib.import_module("hermes_cli.X")` são **mínimo**, não máximo. Pode haver f-strings, dict mappings, `getattr(module, "hermes_*")` que escapam de grep simples. Procurar com:
   ```bash
   grep -rn "hermes_" --include="*.py" | grep -E '"hermes_|"\.\.\.hermes_|f"hermes_'
   ```
3. **`nix/checks.nix`** e builds Nix — podem falhar em mensagens crípticas se algum atributo Nix referenciar `hermes_cli` por string.
4. **Tests com fixtures que mockam `hermes_*`** — alguns `monkeypatch.setattr("hermes_cli.config.foo", ...)` podem precisar update manual.
5. **Entry points em `pyproject.toml`** — Fase 4 deixou `linket = "hermes_cli.main:main"` apontando pro nome velho. Quando renomear o módulo, atualizar pra `linket_cli.main:main` E o `_main_deprecated_*` correspondente.
6. **`hermes_cli/_legacy_alias.py`** criado na Fase 4 — quando renomear, vira `linket_cli/_legacy_alias.py` e os imports dele em `main.py` / `run_agent.py` / `acp_adapter/entry.py` precisam acompanhar.

### Plano de execução proposto (quando der pra rodar pytest)

Cada bullet = um commit atômico. Se algum quebrar testes, descarta só ele.

```
5.0  Captura baseline: pytest tests/ → guarda lista de falhas pré-existentes
5.1  git mv hermes_cli linket_cli
     + sed -i '' 's/hermes_cli/linket_cli/g' em arquivos .py + .yaml + .toml + .md
     + atualiza [project.scripts] e [tool.setuptools.packages.find]
     pytest → deve igualar o baseline (zero novas falhas)
5.2  git mv hermes_state.py linket_state.py
     + sed s/hermes_state/linket_state/ em todos os .py
     pytest gate
5.3  hermes_bootstrap.py → linket_bootstrap.py            (mesmo padrão)
5.4  hermes_constants.py → linket_constants.py
5.5  hermes_time.py → linket_time.py
5.6  hermes_logging.py → linket_logging.py
5.7  tests/hermes_cli/ → tests/linket_cli/
     tests/test_hermes_*.py → tests/test_linket_*.py
5.8  environments/hermes_base_env.py + environments/hermes_swe_env/ + tool_call_parsers/hermes_parser.py
5.9  ui-tui/packages/hermes-ink/ → linket-ink/ (com npm install verificando)
5.10 Plugins YAML pass — busca manual em plugins/**/*.yaml por strings hermes_*
5.11 Verificação final: grep -rn "hermes_cli\|hermes_state\|hermes_bootstrap\|hermes_constants\|hermes_logging\|hermes_time" --include="*.py" --include="*.yaml" --include="*.toml" --include="*.nix" — deve retornar zero (exceto comentários históricos em RELEASE_*.md)
```

### Pré-requisitos pra rodar Fase 5

- [ ] Repo num diretório fora do iCloud
- [ ] `pip install -e ".[dev]"` rodando limpo (precisa `pytest`)
- [ ] `pytest tests/` capturado como baseline (lista de falhas pré-existentes)
- [ ] Backup ou branch `rebrand/linket-modules` separada (não direto na `rebrand/linket`)

---

## Fase 6 — Runtime path `~/.hermes/` → `~/.linket/`

**Quando:** depois da Fase 5, OU em paralelo se você topar (ela toca arquivos diferentes).

**Mudanças:**
- `hermes_constants.py` (que vira `linket_constants.py` na Fase 5): troca `HERMES_HOME = Path.home() / ".hermes"` → `.linket`
- `hermes_bootstrap.py` (idem): adiciona `_migrate_legacy_hermes_home()` rodando no primeiro startup. Lógica:
  - Se `~/.hermes/` existe E `~/.linket/` não, copia (não move) com aviso visível
  - Se ambos existem, prefere `~/.linket/` mas avisa que `~/.hermes/` ainda está lá
- `Dockerfile`: paths `/opt/hermes/` → `/opt/linket/`, user `hermes` (UID 10000) → `linket`, env `HERMES_UID/GID` → `LINKET_UID/GID` (com aliases env durante 1 release)
- `docker-compose.yml`: container_name, volumes `~/.hermes:/opt/data`, env vars
- `install.sh` (Fase 3 deixou pra cá): `HERMES_HOME` → `LINKET_HOME`, `INSTALL_DIR=$HERMES_HOME/hermes-agent` → `$LINKET_HOME/linket-agent`
- `install.ps1`: `$HermesHome` → `$LinketHome`, conteúdo do `SOUL.md` template (linha 970 — "Hermes Agent Persona")
- `skills/productivity/google-workspace/scripts/_hermes_home.py` → `_linket_home.py`

**Risco:** menor que Fase 5 (menos arquivos), mas a auto-migração precisa de testes manuais em 4 cenários: (a) só `~/.hermes/`, (b) só `~/.linket/`, (c) ambos, (d) nenhum.

---

## Fase 7 — Skills, plugins, environments (renomeio de paths)

```
skills/autonomous-ai-agents/hermes-agent/                       → linket-agent/
skills/software-development/hermes-agent-skill-authoring/       → linket-agent-skill-authoring/
skills/software-development/debugging-hermes-tui-commands/      → debugging-linket-tui-commands/
optional-skills/mlops/hermes-atropos-environments/              → linket-atropos-environments/
plugins/hermes-achievements/                                    → linket-achievements/
plugins/kanban/systemd/hermes-kanban-dispatcher.service         → linket-kanban-dispatcher.service
optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py → openclaw_to_linket.py
docs/hermes-kanban-v1-spec.pdf                                  → linket-kanban-v1-spec.pdf  (só rename, conteúdo mantém)
```

Procurar referências cruzadas em `*.yaml` e `*.json` de skills/plugins.

---

## Fase 8 — Documentação completa

- `README.md` e `README.zh-CN.md` — rebrand completo (texto, badges, links). Hoje só o banner e o one-liner foram trocados.
- `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`
- `website/docs/` inteiro (tem 4 guias com `hermes` no nome — renomear arquivos + atualizar links internos)
- `website/docusaurus.config.js` (título do site)
- `RELEASE_v0.*.md` — **NÃO mexer**. Adicionar nota só no topo do arquivo mais recente: "These release notes are from upstream Hermes Agent before the Linket fork."
- `hermes-already-has-routines.md` → `legacy-hermes-routines.md` com nota de origem.

---

## Fase 9 — Atribuição upstream (`NOTICE.md`)

Criar `NOTICE.md` na raiz documentando:
- Linket Agent é fork de Hermes Agent (Nous Research) sob MIT
- Link pro upstream original
- Lista de arquivos/diretórios que vieram da upstream com modificações substanciais
- Crédito a contribuidores externos importantes (rastreable via `git log` upstream)

`LICENSE` já tem ambos os copyrights desde a Fase 2.

---

## Fase 10 — Verificação final

```bash
# Resíduos aceitáveis: NOTICE.md, RELEASE_v0.*.md (history), comentários explicando origem
grep -rin "hermes\|nousresearch" --include="*.py" --include="*.toml" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.sh" --include="*.ps1" --include="*.md" --include="*.nix" \
  --exclude-dir=.git --exclude-dir=node_modules \
  --exclude="RELEASE_v*.md" --exclude="NOTICE.md" \
  | grep -v "^Binary file"

# Smoke test
python -c "import linket_state, linket_bootstrap, linket_logging, linket_cli.main"
pytest tests/ -x
./linket --help
./linket doctor

# Install fresh
mktemp -d /tmp/linket-test-XXXX
# (rodar install.sh dentro)
```

---

_Última atualização: 2026-05-09 — Fases 0–4, 6, 7, 8, 9 concluídas. Fase 5 adiada (depende de pytest); Fase 10 pendente._
