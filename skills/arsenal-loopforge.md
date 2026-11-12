# arsenal-loopforge (Tencent LoopForge, MIT)

Plataforma self-hosted de agentes de codigo: chat com Main Bot em sandboxes, SOPs (workflows repetiveis com gates humanos), CodeBuddy/Codex/Claude Code como executores.
**Estado 12/11/2026: RODANDO NATIVO NO WINDOWS, VALIDADO NO AR na porta 8090 (painel "LoopForge · Agent 编排平台", /api/health 200). Sem WSL, sem Docker, sem reboot.**

## Onde esta
- Repo: `E:\REPOSITORIOS\_ARSENAL_OPEN_SOURCE\LoopForge`
- Binarios Windows nativos: `LoopForge\bin\windows\` (agentflow.exe, agentflow-mcp.exe, agentflow-runner.exe, agentflow-gate-mcp.exe, loopforge-account.exe)
- Binarios Linux amd64: `bin\linux\` (preservados; port usa build tags, zero impacto no build Linux)
- Infra local (fora do git): `LoopForge\.local\` (mariadb, mariadb-data, env.txt, workspaces, launcher.log, agentflow.log)

## Port nativo Windows (feito em 12/11/2026)
Build tags `!windows`/`windows` adicionadas; codigo POSIX original intacto:
- `internal/runtime/lock_unix.go` + `lock_windows.go` (flock -> arquivo .held com PID + stale check via OpenProcess)
- `internal/runtime/browser_proc_unix.go` + `browser_proc_windows.go` (Setpgid/Kill -> taskkill /T /F + processGroupAttr nil)
- `internal/runtime/terminal_stop_unix.go` + `terminal_stop_windows.go` (TIOCGPGRP/SIGHUP -> killProcessGroup)
- `internal/runtime/fs_identity_unix.go` + `fs_identity_windows.go` (Stat_t Dev/Ino -> ByHandleFileInformation VolumeSerialNumber/FileIndex)
- `internal/preview/archive_nlink_unix.go` + `archive_nlink_windows.go` (Nlink -> NumberOfLinks via GetFileInformationByHandle)
- `internal/runner/runner_proc_unix.go` + `runner_proc_windows.go` (grupo de processo; Windows mata so o processo CLI)
- `internal/httpapi/session_lock_unix.go` + `session_lock_windows.go` (flock -> .held + PID)

## Como subir
- MariaDB 11.4.5 portable em `.local\mariadb` (zip oficial de archive.mariadb.org), porta 33315, DB `loopforge`, user `loopforge` (senha em `.local\env.txt`)
- `agentflow.exe -addr 127.0.0.1:8090 -workspaces .local\workspaces` com env `AGENTFLOW_MYSQL_DSN`, `AGENTFLOW_SESSION_SECRET` (geradas e gravadas em `.local\env.txt`), `AGENTFLOW_BROWSER=off` (sidecar docker de browser nao existe nativo)
- Seed aplicado: `migrations/seed/001_public_catalog.sql` + `002_welcome_project.sql`
- Autostart: `LoopForge\.local\start_loopforge.pyw` (idempotente, sobe so o que nao responde) + atalho `loopforge-gateway.vbs` na pasta Inicializar
- Frontend: `web\native-chat\` (build com Node >= 22; o agente ja serve o painel)

## Por que nao via WSL/Docker
- WSL2 exige Hyper-V; na maquina o VirtualMachinePlatform foi habilitado (12/11) mas exige reboot, e o componente legado WSL1 precisa de elevacao (UAC pendente). O port nativo eliminou a necessidade.
- Banco: "MySQL is the only data source" (`AGENTFLOW_MYSQL_DSN`); MariaDB portable resolve sem Docker.
- Sandbox: sem Docker, cai em sandbox local de processo (ok para uso local).

## Pendencias
- Docker ausente na maquina (opcional: sandboxes isoladas; sem ele, sandbox local).
- UAC do WSL ainda pendente de clique do Victor (nao e mais necessario para o LoopForge).
- Commit do port: os arquivos estao no working tree do repo clonado (branch local `windows-native-port` recomendado antes de qualquer push/fork).
