#!/usr/bin/env python

import subprocess
import re
import argparse
import sys


def execute_capture_stderrout(cmd):
    popen = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


parser = argparse.ArgumentParser()

parser.add_argument('--user',help='remote server username  (default: %(default)s)',default='akhanf')
parser.add_argument('--host',help='remote server hostname (default: %(default)s)', default='graham.sharcnet.ca')
parser.add_argument('--time',help='interactive job time (default: %(default)s)', default='3:00:00')
parser.add_argument('--port',help='local port to use (default: %(default)s)', default='8888')
parser.add_argument('--ncpus',help='interactive job ncpus (default: %(default)s)', default='4')
parser.add_argument('--mem',help='interactive job memory (default: %(default)s)', default='8gb')
parser.add_argument('--account',help='interactive job account (default: %(default)s)', default='ctb-akhanf')
parser.add_argument('--venv',help='path to remote virtualenv (default: %(default)s)', default='/project/6050199/akhanf/opt/virtualenvs/snakemake')


args = parser.parse_args()


remote_script = '~/.remote_jupyter_script'

remote_script_contents = '#!/bin/bash\n'\
             'unset XDG_RUNTIME_DIR\n'\
             f'{args.venv}/bin/jupyter lab --ip $(hostname -f) --no-browser\n'

print(f'Creating remote script to launch jupyter lab in {remote_script}...')
print(remote_script_contents)
gen_remote_script = ['ssh',f'{args.user}@{args.host}','-T',f'cat > {remote_script} && chmod a+x {remote_script}'] 
subprocess.run(gen_remote_script,encoding='ascii',input=remote_script_contents)
print('')


#set-up regex for capturing host & token
host_token_regex = '   http:\/\/(?!127)([\w\d.]+):([0-9]+)\/\?token=([\w\d]+)'
host_token_pattern = re.compile(host_token_regex)
salloc_regex = 'salloc'
salloc_pattern = re.compile(salloc_regex)


ssh_cmd = ['ssh',f'{args.user}@{args.host}','salloc',f'--time={args.time}',f'--cpus-per-task={args.ncpus}',f'--ntasks=1',f'--mem={args.mem}',f'--account={args.account}','srun',f'{remote_script}']

print('Submitting remote interactive job...')
print(' '.join(ssh_cmd))
print('')

for line in execute_capture_stderrout(ssh_cmd):

    #debug: print line of salloc output (exclude other lines)
    if (re.search(salloc_pattern,line) != None):
        print(line, end="")


    #check if the host/port/token from stderr is in the line
    host_token_match = re.search(host_token_pattern,line)
    if host_token_match != None:
        host,port,token = host_token_match.group(1,2,3)
        #debug, print match:
        #print(f'Matched pattern, host: {host}, port: {port}, token: {token}')
        break

print('')

#now, spawn the ssh process for tunnelling:
tunnel_cmd = ['ssh','-L', f'{args.port}:{host}:{port}', f'{args.user}@{args.host}','-N']

print('Starting ssh tunnel...  CTRL-C to kill tunnel')
print(' '.join(tunnel_cmd))
print('')

#run tunnel
p = subprocess.Popen(tunnel_cmd)


print('')
print('Open the following link in your web browser:')
print(f'http://localhost:{args.port}/?token={token}')
print('')


try:
    p.wait()
except KeyboardInterrupt:
    try:
       print('Killing ssh tunnel on 8888..')
       p.terminate()
    except OSError:
       pass
    p.wait()


