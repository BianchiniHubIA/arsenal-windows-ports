# Ativar LoopForge no Windows (pos-reboot)

## Estado atual (12/11/2026)
- Frontend chatbot: BUILDADO (`web/native-chat/` gerado).
- Binarios Linux amd64: prontos em `bin/linux/` (agentflow, agentflow-mcp, agentflow-runner, agentflow-gate-mcp).
- WSL 2.7.3 instalado, mas a virtualizacao (Plataforma de Maquina Virtual) foi habilitada e so vale apos REINICIAR o Windows.
- Docker NAO esta instalado (o sandbox de agentes do LoopForge usa Docker; sem ele, o LoopForge usa sandbox local de processo).

## Apos o reboot, rodar (na ordem)
1. Instalar a distro (baixa ~500 MB, uma vez):
   wsl --install -d Ubuntu --no-launch
2. Instalar MariaDB dentro do WSL:
   wsl -d Ubuntu -- bash -lc "sudo apt-get update -y && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server && sudo service mariadb start"
3. Criar banco e usuario:
   wsl -d Ubuntu -- bash -lc "sudo mysql -e \"CREATE DATABASE IF NOT EXISTS loopforge; CREATE USER IF NOT EXISTS 'loopforge'@'localhost' IDENTIFIED BY 'loopforge_local'; GRANT ALL ON loopforge.* TO 'loopforge'@'localhost'; FLUSH PRIVILEGES;\""
4. Subir o servidor (os binarios ficam acessiveis em /mnt/e/REPOSITORIOS/_ARSENAL_OPEN_SOURCE/LoopForge/bin/linux):
   wsl -d Ubuntu -- bash -lc "cd /mnt/e/REPOSITORIOS/_ARSENAL_OPEN_SOURCE/LoopForge && AGENTFLOW_MYSQL_DSN='loopforge:loopforge_local@tcp(127.0.0.1:3306)/loopforge' AGENTFLOW_HTTP_PORT=8080 AGENTFLOW_SESSION_SECRET='local-dev-secret' AGENTFLOW_AUTH_REQUIRED=false nohup ./bin/linux/agentflow -workspaces /tmp/lf-workspaces > /tmp/agentflow.log 2>&1 &"
5. Validar: HTTP 200 em http://127.0.0.1:8090 (WSL2 encaminha localhost para o Windows automaticamente).
6. OBS: sem Docker, AGENTFLOW_LOCAL_SANDBOX NAO pode ser "docker"; deixar a env ausente para cair no sandbox local de processo.

## Por que nao roda nativo no Windows
O runtime usa syscalls POSIX (syscall.Flock, syscall.Setpgid, syscall.Kill, syscall.Stat_t) em internal/runtime (workspace_lock.go, browser.go). Port nativo exigiria reescrever esses trechos para a API do Windows; os autores do projeto (Tencent) publicam a stack para Docker/Linux (compose.yaml com mysql:8.4 + imagem ghcr.io/tencent/loopforge).
