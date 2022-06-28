#!/usr/bin/env python

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


DISPLAY_TITLE = r"""
       _         __                                __              _                 _                                _   
      | |       / _|                              / _|            (_)               | |                              | |  
 _ __ | |______| |_ _ __ ___  ___  ___ _   _ _ __| |_ ___ _ __ ___ _ _ __ ___  _ __ | | ___ _ __ ___ _ __   ___  _ __| |_ 
| '_ \| |______|  _| '__/ _ \/ _ \/ __| | | | '__|  _/ _ \ '__/ __| | '_ ` _ \| '_ \| |/ _ \ '__/ _ \ '_ \ / _ \| '__| __|
| |_) | |      | | | | |  __/  __/\__ \ |_| | |  | ||  __/ |  \__ \ | | | | | | |_) | |  __/ | |  __/ |_) | (_) | |  | |_ 
| .__/|_|      |_| |_|  \___|\___||___/\__,_|_|  |_| \___|_|  |___/_|_| |_| |_| .__/|_|\___|_|  \___| .__/ \___/|_|   \__|
| |                                                      ______               | |                   | |                   
|_|                                                     |______|              |_|                   |_|                   
"""


parser = ArgumentParser(description='A ChRIS DS plugin that generates a report table (in various formats) off a FreeSurfer annotation/segmentation volume',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-e', '--example', default='jelly',
                    help='argument which does not do anything')
parser.add_argument('-V', '--version', action='version',
                    version=f'$(prog)s {__version__}')


# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title='FreeSurfer Simple Reporting',
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='100Mi',    # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr)
    print(f'Option: {options.example}', file=sys.stderr)


if __name__ == '__main__':
    main()

