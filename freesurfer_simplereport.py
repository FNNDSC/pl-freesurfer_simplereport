#!/usr/bin/env python

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from importlib.metadata import Distribution

from chris_plugin import chris_plugin, PathMapper

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version


import os
from importlib.resources import files
import sys

import  pfmisc
from    pfmisc._colors          import Colors

import  pudb

from    init                    import start
from    mgz                     import fmgzio
from    report                  import template
from    filter                  import convert

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
parser.add_argument(
                        '--annotation', '-a',
                        default     = '**/*aparc*mgz',
                        help        = '''
                        FreeSurfer annotation volume (or glob) to analyze.
                        These are typically in mgz format and have a string
                        'aparc' and/or 'aseg' in their file names. If you
                        only want to report on one annotation file, specify
                        that file explicitly.
                        '''
)
parser.add_argument(
                        '--report_name', '-r',
                        default     = 'volumetric_report',
                        help        = '''
                        Basename of the report file. Note, the annotation
                        file is appended to this basename.
                        '''
)
parser.add_argument(
                        '--report_types', '-t',
                        default     = 'txt,html,pdf,csv',
                        help        = 'comma separated list of report types to generate'
)
parser.add_argument(
                        '--internalLUTpath',
                        default     = '/usr/local/src/pl-freesurfer_simplereport',
                        help        = '''
                        A path to a (typically in-container) freesurfer color
                        lookup table.
                        '''
)
parser.add_argument(
                        '--lut', '-l',
                        default     = '**/FreeSurferColorLUT.txt',
                        help        = '''Lookup table filename; if "__lut__" then
                        use internal/built-in lookup table, otherwise use first
                        hit in input file space; built-in lookup table is hard coded
                        to be

                                <internalLUTpath>/FreeSurferColorLUT.txt
                        '''
)
parser.add_argument(
                        '-v', '--verbosity',
                        default = '0',
                        help    = 'verbosity level of app'
)
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


def segmentation_process(options: Namespace, inputfile: Path, outputfile: Path) -> dict:
    """Main entry point for generating a report in various formats based
    off a FreeSurfer annotation file. For each identified annotation volume,
    read the volume, generate a report template (i.e. a structure that
    contains the report data), and then convert to the required output
    format.

    Args:
        options (Namespace): The option space, needed to determine report types.
        inputfile (Path): The input file to process
        outputfile (Path): The corresponding outputfile path
    """

    start.LOG(f"Processing {inputfile}...")
    annot           = fmgzio.mgz(inputfile, log     = start.LOG)
    masterreport    = template.template(mgz         = annot,
                                        lut         = start.LUT,
                                        log         = start.LOG)
    convertreport   = convert.format(   template    = masterreport,
                                        format      = options.report_types,
                                        basename    = options.report_name,
                                        log         = start.LOG)
    return convertreport.do(outputfile)

# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser              = parser,
    title               = 'FreeSurfer Simple Reporting',
    category            = '',                   # ref. https://chrisstore.co/plugins
    min_memory_limit    = '8Gi',                # supported units: Mi, Gi
    min_cpu_limit       = '1000m',              # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit       = 0                     # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr)
    print(f'Options: {options}', file=sys.stderr)

    ld_result   : list  = []
    if start.init(options, inputdir, outputdir)['isOK']:
        mapper = PathMapper.file_mapper(inputdir, outputdir,
                            glob    = options.annotation
        )
        for input, output in mapper:
            ld_result.append(segmentation_process(options, input, output))


if __name__ == '__main__':
    main()

