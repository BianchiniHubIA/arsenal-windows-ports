"""Launcher sem janela do gateway Experiential local (porta 8017).
Uso: pythonw start_gateway.pyw  (ou python start_gateway.pyw)
Chave do gateway: .exp/gateway_key.txt (Authorization: Bearer <chave>)."""
import os
import subprocess

ex = os.path.dirname(os.path.abspath(__file__))
py = os.path.join(ex, '.venv', 'Scripts', 'python.exe')
env = dict(os.environ)
env['OLLAMA_KEY'] = 'ollama'
subprocess.run([py, '-m', 'exp', 'run', '--port', '8017', '--non-interactive', '--ghost'],
               cwd=ex, env=env)
