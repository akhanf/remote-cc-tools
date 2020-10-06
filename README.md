# remote-cc-tools
some tools for accessing compute canada resources remotely


## remote_jupyter

```
usage: remote_jupyter [-h] -u USER [--host HOST] [--time TIME] [--ncpus NCPUS]
                      [--mem MEM] [--account ACCOUNT] [--use_login_node]
                      [--port PORT] [--venv VENV] [--create_remote_venv]
                      [--pip_install PIP_INSTALL] [--verbose]

Launches JupyterLab in an interactive compute canada job, creating the
required ssh tunnel.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Remote server username
  --host HOST           Remote server hostname (default: graham.sharcnet.ca)
  --time TIME           Interactive job time (default: 3:00:00)
  --ncpus NCPUS         Interactive job ncpus (default: 4)
  --mem MEM             Interactive job memory (default: 8gb)
  --account ACCOUNT     Interactive job account (default: ctb-akhanf)
  --use_login_node      Use the login node directly, instead of submitting
                        interactive job. You cannot use this for long jobs or
                        those requiring more resources) (default: False)
  --port PORT           Local port to use for jupyter (default: 8888)
  --venv VENV           Path to remote virtualenv (default: ~/venv_jupyterlab)
  --create_remote_venv  Create the remote virtualenv and pip install
                        jupyterlab on it (default: False)
  --pip_install PIP_INSTALL
                        Install packages to existing virtualenv using pip
  --verbose             Display verbose output (default: False)
  ```
