#! /usr/bin/env python3


import shutil
from subprocess import check_call
from os import path, getcwd

# Set up some useful strings
name = "temp_www"
src_gz = f'{name}-0.0.1.tar.gz'
here = getcwd()
src_target = path.join(path.expanduser('~'), 'rpmbuild', 'SOURCES', src_gz)


# collect the src data
check_call(['tar', 
            '--exclude', 'src/temp_srv/__pycache__',
            '--exclude', 'src/temp_srv/static/.webassets-cache',   
            '-cvzf', src_gz, 
            'src/temp_srv/', 
            'src/wsgi.py',
            'src/tmpsrv.ini',
            'src/config.py',
            f'src/{name}.sh',
            f'{name}.service'])

# Move the zip file to the rpmbuild SOURCES folder
shutil.move(src_gz,src_target)


# Call the packaging rpmbuild command
spec_path = path.join(here, f"{name}.spec")
check_call(["rpmbuild", "-bb", spec_path])

