#!/usr/bin/env python

import argparse
import os.path
import platform
import subprocess
import errno
import shutil
import logging
import sys

def parse_path(value):
    """Returns the given path with ~ and environment variables expanded."""
    return os.path.expanduser(os.path.expandvars(value))

def export_recipes(factorio_data_dir, output_data_dir):
    export_path = os.path.abspath('export')
    recipes_dir_path = os.path.join(factorio_data_dir, 'base/prototypes/recipe')
    recipe_files_paths = []

    for root, dirs, files in os.walk(recipes_dir_path):
        recipe_files_paths.extend(os.path.join(root, f) for f in files)

    recipe_json_path = os.path.join(output_data_dir, 'recipes.json')
    args = [os.path.join(export_path, 'export_recipes.lua')] + recipe_files_paths
    with open(recipe_json_path, 'w') as recipe_json_file:    
        logging.info('Exporting recipes from %r to %r...',
                     recipes_dir_path,
                     recipe_json_path)
        export = subprocess.Popen(
                args=args,
                cwd=export_path,
                stdout=recipe_json_file.fileno())
        if export.wait() != 0:
            raise Exception('crap')

def export_icons(factorio_data_dir, output_data_dir):
    source_icon_path = os.path.join(factorio_data_dir, 'base/graphics/icons')
    target_icon_path = os.path.join(output_data_dir, 'icons')
    if os.path.exists(target_icon_path):
        if os.path.isdir(target_icon_path):
            shutil.rmtree(target_icon_path)
        else:
            raise Exception('unexpected file at %r' % target_icon_path)

    logging.info('Copying %r to %r...', source_icon_path, target_icon_path)
    shutil.copytree(source_icon_path,
                    target_icon_path)

# TODO(brian@sweetapp.com): Extract item names from:
# base/locale/en/base.cfg

def create_output_data_dir(path):
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            return
        else:
            raise e


def main():
    if platform.system() == 'Darwin':
        default_data_path = '/Applications/factorio.app/Contents/data'
    else:
        default_data_path = None

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '--factorio_data_path', metavar='PATH',
        default=default_data_path,
        type=parse_path,
        help='path to the data (datastore, blobstore, etc.) associated with the '
        'application.')
    parser.add_argument(
        '--output_data_path', metavar='PATH',
        default=os.path.abspath('factorio-data'),
        type=parse_path,
        help='path to the data (datastore, blobstore, etc.) associated with the '
        'application.')

    args = parser.parse_args()

    factorio_data_path = os.path.abspath(args.factorio_data_path)
    output_path = args.output_data_path

    sys.stderr.write(
        'Extracting data\nfrom: %s\nto:   %s\n' % (factorio_data_path,
                                                   output_path))

    create_output_data_dir(output_path)

    export_recipes(factorio_data_path, output_path)
    export_icons(factorio_data_path, output_path)
    sys.stderr.write('Done!\n')
# "./Contents/data/base/locale/en/base.cfg"


if __name__ == '__main__':
    main()
