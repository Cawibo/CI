import os
import subprocess
import shutil
import time
import stat

def flatten_data(data):
    """Flattens a POST request JSON to allow for easier access of fields."""
    res = {}
    res['branch'] = data['pull_request']['head']['ref']
    res['repo'] = data['pull_request']['head']['repo']['name']
    res['ssh_url'] = data['pull_request']['base']['repo']['ssh_url']
    res['timestamp'] = data['pull_request']['updated_at'].replace(':', '_')
    return res

def clone_repo(data, cwd='./tmp/'):
    """Clones the repo and branch defined in data-parameter into cwd path."""
    command = 'git clone --depth=1 -b {branch} {ssh_url}'.format(
        branch=data['branch'],
        ssh_url=data['ssh_url']
    )
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, shell=True)
    process.communicate()[0].strip()
    process.kill()

def setup_logs(path):
    """Creates the log folder structure if one doesn't already exist."""
    os.makedirs(path, exist_ok=True)

def get_paths(data):
    """Formats the relevant path strings."""
    tmp = './tmp/'
    return tmp, './logs/{repo}/{branch}/'.format(repo=data['repo'], branch=data['branch']), tmp+data['repo']

def run_flake8(data, path, log_path):
    """Executes the flake8 linter on the cloned repo."""
    command = 'python -m flake8 --output-file="{log_path}" --count {path}'.format(
        log_path=log_path, path=path
    )

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    total_count = int(process.communicate()[0].strip())
    process.kill()
    
    return total_count

def clear_tmp(path):
    """Removes all content from the tmp-folder."""
    #https://stackoverflow.com/questions/55717798/how-to-delete-directory-with-git-folder-in-python
    def on_rm_error(func, path, exc_info):
        #from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    shutil.rmtree(path, onerror=on_rm_error)