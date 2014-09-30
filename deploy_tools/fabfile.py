from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/rfj001/TDD-With-Python.git'

def deploy():
    # env.host will contain the address of the server we've specified
    # at the command line
    # env.use will contain the username you're using to log in to the server
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        # run says "run this shell command"
        # mkdir -p can create directories several levels deep, and only
        # if necessary
        run('mkdir -p %s/%s' % (site_folder, subfolder))
        
def _get_latest_source(source_folder):
    # Check if .git exists to see if the repo has already been cloned in that
    # folder
    if exists(source_folder + '/.git'):
        # change to correct directory and pull down all the latest commits
        run('cd %s && git fetch' % (source_folder,))
    else:
        # Alternatively, clone the git repo to bring down a fresh source tree
        run('git clone %s %s' % (REPO_URL, source_folder))
    # On local machine, capture output from git log to get the hash of the 
    # current commit so that the server ends up with whatever code is currently
    # checked out on your machine
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # Reset --hard to that commit, erasing any current changes in server's code
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))
    
def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    # sed command does a string substitution in a file
    # Changes DEBUG in settings from True to False
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # Adjust ALLOWED_HOSTS, using a regex to match the right line
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    # Django uses SECRET_KEY for some of its crypto-cookies and CSRF protection
    # Good practice to make sure the secret key on the server is different from
    # the one in your (possibly public) source code repo.
    # This code generates a new key to import into settings, if there isn't one
    # there already.
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    # Relative import used here to be absolutely sure we're importing the local
    # module
    # Some people recommend using environment variables to set things like
    # secret keys. Do whatever you feel is most secure in your environment.
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    
def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))
    
def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))
    
def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder,
    ))