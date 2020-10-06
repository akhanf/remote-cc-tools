# remote-cc-tools
some tools for accessing compute canada resources remotely


## remote_jupyter

Running jupyter notebooks on compute canada (e.g. graham) can be cumbersome if `sshuttle` cannot be used (e.g. if you don't have sudo on your local machine), or you are not running linux/mac. Furthermore, you need to have a virtualenv set-up on the host machine, but the dependencies (e.g. pip install) can't be set-up on a compute node without internet access. 

This script does everything you need to initiate a `jupyter lab` session in an interactive job, setting up the ssh tunnel in the background, and also creating a virtualenv if one does not exist. 


### Dependencies:
  * Python3 installed on your local system
  * Access to a compute canada host
  
### Usage: 
Simply add the script to your path, and run: 

`remote_jupyter -u COMPUTE_CANADA_USERNAME`




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
