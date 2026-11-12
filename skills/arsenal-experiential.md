# arsenal-experiential (Experiential Labs, Apache-2.0)

Gateway e roteador de modelos OpenAI-compatible, local. Controla quem usa qual modelo, com limites de gasto, e vira roteador customizado a partir do trafego.
**Estado: FUNCIONAL NO WINDOWS, VALIDADO NO AR em 12/11/2026.**

## Onde esta
- Repo: `E:\REPOSITORIOS\_ARSENAL_OPEN_SOURCE\Experiential` (venv em `.venv`, gerenciado com uv)
- Estado do gateway: `.exp\` (org "Bianchini", chave em `.exp\gateway_key.txt`)

## Patches Windows aplicados (obrigatorios; reaplicar apos git pull ou reinstalar o venv)
1. **Shim termios**: `termios.py` criado em `.venv\Lib\site-packages\` (modulo Unix-only; funcoes no-op seguras).
2. **Permissoes Unix puladas no Windows**: validacoes `stat.S_IMODE(...)`/`st_mode` contra `0o600/0o700/0o077/0o777` ganharam prefixo `os.name != "nt" and` nos arquivos `exp/cli/gateway/key_output.py`, `exp/common/project/database.py`, `exp/runtime/gateway/auth.py`, `exp/runtime/gateway/sqlite/migrations.py` (source `exp/` e `.venv\Lib\site-packages\exp\`). Cuidado: NAO tocar em chamadas `chmod(...)` (falso positivo ja aconteceu e foi revertido em `exp/common/core/files.py`).
3. **O_NOFOLLOW**: `os.O_NOFOLLOW` trocado por `getattr(os, "O_NOFOLLOW", 0)` em `key_output.py`, `artifact_files.py`, `bundle.py`, `database.py`, `snapshot_file.py`, `journal.py`.

## Subir o gateway
- Launcher sem janela: `E:\REPOSITORIOS\_ARSENAL_OPEN_SOURCE\Experiential\start_gateway.pyw` (porta 8017)
- Manual: `.venv\Scripts\python.exe -m exp run --port 8017 --non-interactive --ghost`
- Chave: ler `E:\REPOSITORIOS\_ARSENAL_OPEN_SOURCE\Experiential\.exp\gateway_key.txt`
- Endpoints: `GET /v1/models`, `POST /v1/chat/completions` com `Authorization: Bearer <chave>` e `"model": "nemotron"`

## Config atual (criada em 12/11/2026)
- Provider `ollama`: `openai-compatible`, base `http://127.0.0.1:11434/v1`, env `OLLAMA_KEY=ollama`
- Alias `nemotron` -> deployment `ollama:nemotron` (tag sem ":" criada com `ollama cp nemotron-bolt:e4b nemotron`; a validacao de IDs do exp nao aceita ":")
- Identity `default`, grant `default:nemotron`, chaves `local-01/02/03`
- CLI: `.venv\Scripts\python.exe -m exp <comando>`; comandos: `eval`, `build`, `run`, `code`, `login`, `config`, `capture`, `optimize`

## Validacao real (12/11/2026)
`POST /v1/chat/completions` (model=nemotron, max_tokens 1024) => HTTP 200 em 11s, resposta em portugues do Nemotron-Bolt 7.5B Q4 via Ollama local, finish_reason=stop, campo `reasoning` separado.
ATENCAO: e modelo de raciocinio; com `max_tokens < ~100` o `content` vem null (gasta o teto pensando). Usar max_tokens >= 256.

## Limitacoes upstream
- `exp code`: quebra (pacote npm `exp-code@0.1.2` removido do registry pelos autores).
- `exp login` / `exp capture`: dependem de conta Experiential Cloud.
- `exp build` / `exp optimize`: precisam de traces locais exportados.
