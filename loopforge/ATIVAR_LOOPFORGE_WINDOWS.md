# Reconstruir LoopForge no Windows (receita atualizada 21/11/2026)

## Estado final (21/11/2026)
- LoopForge NATIVO no Windows (agentflow.exe em bin/windows), MariaDB portable em .local/mariadb (porta 33315), frontend embedado.
- Porta 8090 (127.0.0.1). Launcher idempotente: .local/start_loopforge.pyw (chamado pelo VBS da Startup).
- Reconstruido apos a pasta ser apagada na migracao de 17/11. Patch completo: loopforge_windows_port.patch neste repo.

## Passos de reconstrucao (na ordem)
1. Clonar o upstream: git clone https://github.com/tencent/loopforge.git F:\_ARSENAL_OPEN_SOURCE\LoopForge
2. Aplicar o patch: git apply --reject <arsenal-windows-ports>/loopforge/loopforge_windows_port.patch e tratar os .rej (imports removidos que o upstream mudou).
3. Frontend: cd chatbot && npm install && npm run build (gera web/native-chat exigido pelo embed).
4. Modulos Go: go get golang.org/x/crypto@latest golang.org/x/text@latest golang.org/x/sys@latest && go mod tidy.
   - SE o build reclamar "no required module provides package ... internal/...": go clean -cache (o build cache grudou um resultado de extracao incompleta) e conferir que os diretorios internos do GOMODCACHE nao estao vazios (extrair do zip manualmente se preciso).
5. Build: go build -o bin\windows\agentflow.exe .\cmd\agentflow
6. MariaDB: baixar https://archive.mariadb.org/mariadb-11.4.5/winx64-packages/mariadb-11.4.5-winx64.zip, extrair para .local\mariadb, rodar mysql_install_db.exe --datadir=.local\mariadb-data --password= (a pasta do datadir precisa existir vazia antes).
7. Subir o mysqld (porta 33315) e criar: CREATE DATABASE loopforge; CREATE USER loopforge/loopforge_local; GRANT ALL.
8. Criar .local/env.txt (DSN, SESSION_SECRET, AUTH_REQUIRED=false, BROWSER=off) e .local/start_loopforge.pyw (copiar do repo de patches).
9. VBS da Startup: loopforge-gateway.vbs -> pythonw start_loopforge.pyw (oculto).
10. Validar: HTTP 200 em / e /api/health na porta 8090.

## Notas
- O port nativo usa os helpers em internal/{runtime,httpapi,runner,preview}/port_*.go e procgroup_*.go com build tags windows/!windows.
- O build precisa do build cache limpo apos qualquer extracao parcial do GOMODCACHE (licao do dia 21/11).
- Sem Docker: deixar AGENTFLOW_LOCAL_SANDBOX ausente para cair no sandbox local de processo.
