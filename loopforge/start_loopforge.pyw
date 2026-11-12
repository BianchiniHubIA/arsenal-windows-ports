# -*- coding: utf-8 -*-
"""LoopForge Windows launcher: sobe MariaDB e o agentflow nativo, ambos ocultos.
Idempotente: so inicia o que nao estiver respondendo."""
import os, socket, subprocess, sys, time

LF = r'E:\REPOSITORIOS\_ARSENAL_OPEN_SOURCE\LoopForge'
LOCAL = os.path.join(LF, '.local')
LOG = os.path.join(LOCAL, 'launcher.log')

def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + msg + '\n')

def port_open(port):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(('127.0.0.1', port))
        s.close()
        return True
    except Exception:
        return False

def main():
    env = {}
    env_path = os.path.join(LOCAL, 'env.txt')
    if os.path.isfile(env_path):
        for line in open(env_path):
            k, _, v = line.strip().partition('=')
            if k:
                env[k] = v
    if not env:
        log('env.txt ausente; abortando')
        return

    bin_dir = os.path.join(LOCAL, 'mariadb', 'bin')
    datadir = os.path.join(LOCAL, 'mariadb-data')

    # 1. MariaDB
    if not port_open(33315):
        log('subindo mysqld...')
        subprocess.Popen([os.path.join(bin_dir, 'mysqld.exe'),
                          '--datadir=' + datadir, '--port=33315', '--bind-address=127.0.0.1'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        for _ in range(30):
            time.sleep(2)
            if port_open(33315):
                break
        log('mysqld pronto: %s' % port_open(33315))
    else:
        log('mysqld ja rodando')

    # 2. Agentflow
    if not port_open(8090):
        log('subindo agentflow...')
        workspaces = os.path.join(LOCAL, 'workspaces')
        os.makedirs(workspaces, exist_ok=True)
        exe = os.path.join(LF, 'bin', 'windows', 'agentflow.exe')
        run_env = dict(os.environ)
        run_env['AGENTFLOW_MYSQL_DSN'] = env['AGENTFLOW_MYSQL_DSN']
        run_env['AGENTFLOW_SESSION_SECRET'] = env['AGENTFLOW_SESSION_SECRET']
        run_env['AGENTFLOW_BROWSER'] = 'off'
        logf = open(os.path.join(LOCAL, 'agentflow.log'), 'a')
        subprocess.Popen([exe, '-addr', '127.0.0.1:8090', '-workspaces', workspaces],
                         env=run_env, stdout=logf, stderr=logf,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        for _ in range(40):
            time.sleep(2)
            if port_open(8090):
                break
        log('agentflow pronto: %s' % port_open(8090))
    else:
        log('agentflow ja rodando')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log('ERRO: %s' % e)
