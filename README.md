# Arsenal Windows Ports

Ports nativos para Windows de ferramentas open source do arsenal Bianchini, rodando sem Docker, sem WSL e sem reboot.

## LoopForge (Tencent, MIT) - NATIVO WINDOWS, NO AR
Plataforma self-hosted de agentes de codigo (Main Bot em sandboxes, SOPs, CodeBuddy/Codex/Claude Code como executores).
- `loopforge/loopforge_windows_port.patch`: port completo via build tags (flock -> .held+PID, browser proc -> taskkill /T /F, fs identity -> ByHandleFileInformation, grupos de processo)
- `loopforge/start_loopforge.pyw`: launcher idempotente oculto (MariaDB 33315 + agentflow 8090)
- `loopforge/ATIVAR_LOOPFORGE_WINDOWS.md`: receita completa de ativacao (MariaDB 11.4.5 portable, env, seed, autostart)
- Estado: VALIDADO NO AR em 12/11/2026 (painel na 8090, /api/health 200, banco com schema completo)

## Experiential (Apache-2.0) - GATEWAY LOCAL, NO AR
Gateway e roteador de modelos OpenAI-compatible local (controla quem usa qual modelo, limites de gasto).
- `experiential/experiential_windows_port.patch`: patches Windows (shim termios, permissoes Unix condicionais, O_NOFOLLOW)
- `experiential/start_gateway.pyw`: launcher sem janela (porta 8017)
- Estado: VALIDADO NO AR em 12/11/2026 (POST /v1/chat/completions com model=nemotron via Ollama local -> 200; token invalido -> 401)

## Skills
- `skills/arsenal-loopforge.md`
- `skills/arsenal-experiential.md`

## Aviso
- Os repos de origem sao clonados direto dos upstreams (github.com/Tencent/LoopForge e github.com/experientiallabs/experiential); este repo preserva apenas os patches e scripts locais. Para reconstruir: clonar o upstream, aplicar o patch e seguir a receita.
