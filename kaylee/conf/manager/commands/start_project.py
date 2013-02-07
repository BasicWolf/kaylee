import os
import re
import argparse
import shutil
from jinja2 import Template
from kaylee.conf.manager import BaseCommand



VALID_NAME_RE = re.compile(r'\w+')

PROJECT_TEMPLATE_DIR = 'project_template'
PROJECT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),
                                     PROJECT_TEMPLATE_DIR)

TEMPLATE_FILES = [
    #(template file in PROJECT_TEMPLATE_DIR,
    # destination file name with {project} macro replacement)
    # e.g. ('client/project.coffee', 'client/{project}.coffee'),

    ('client/project.coffee', 'client/{project}.coffee'),
    ('server/__init__.py', 'server/__init__.py'),
    ('server/project.py', 'server/{project}.coffee'),
]


class StartProjectCommand(BaseCommand):
    name = 'startproject'
    help = 'Starts new Kaylee project'

    args = {
        'name' : {}
        ('-m', '--mode') : dict(choices=['manual', 'auto'], default='auto')
    }

    @staticmethod
    def execute(ns):
        if VALID_NAME_RE.match(ns.name) is None:
            raise ValueError('Invalid project name: {} ([A-Za-z0-9_])'
                             .format(ns.name))

        # build rendering environment constants
        render_env = {
            'project_file_name' : ns.name.lower(),
            'project_class_name' : (ns.name[0].upper() + ns.name[1:])
        }
        # copy project template to cwd
        dest_path = os.path.join(os.getcwd(), ns.name)
        shutil.copytree(PROJECT_TEMPLATE_PATH, dest_path)

        for fname, fname_template in TEMPLATE_FILES:
            # render template
            template_path = os.path.join(dest_path, fname)
            with open(template_path) as f:
                template_data = f.read()
            document_data = Template(template_data).render(**render_env)

            # remove the template file
            os.remove(template_path)

            # write to output file
            doc_fname = fname_template.format(project=ns.name)
            doc_path = os.path.join(dest_path, doc_fname)
            with open(doc_path, 'w') as f:
                f.write(document_data)

def expand_project_mode_opt(opt):
    if s == 'manual':
        return 'MANUAL_PROJECT_MODE'
    elif s == 'auto':
        return 'AUTO_PROJECT_MODE'
    else:
        raise ValueError('Invalid project mode option: {}'.format(opt))