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
import nibabel as nib
import numpy as np
import collections
import re
import pandas as pd
from yattag import Doc
import pdfkit
from fpdf import FPDF

import  pfmisc
from    pfmisc._colors          import Colors

import  pudb

import  lut
from    lut                     import lookuptable

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


PFMlogger       = None
LOG             = None
LUT             = None

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
                        default     = '/usr/local/freesurfer',
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


def init(options: Namespace, inputdir: Path, outputdir: Path) -> dict:
    """Perform some initializations, most notably verify/check on the
    FreeSurfer lookup table file.

    Args:
        options (Namespace): CLI namespace
        inputdir (Path): the plugin inputdir
        outputdir (Path): the plugin outputdir

    Returns:
        dictionary: initialization status and lookup table file location.
    """

    global PFMlogger, LOG, LUT

    d_ret               = {
        'isOK':             True,
        'lookupTableFile':  None
    }
    path_lutfile        : Path = None
    PFMlogger           = pfmisc.debug(
                                            verbosity   = int(options.verbosity),
                                            within      = 'main',
                                            syslog      = True
                                        )
    LOG                 = PFMlogger.qprint
    LOG("initializing...")
    for k,v in options.__dict__.items():
         LOG("%25s:  [%s]" % (k, v))
    LOG("")
    pudb.set_trace()
    if len(options.internalLUTpath):
        inputdir    = Path(options.internalLUTpath)
    if inputdir.is_dir():
        LOG("lookup table inputdir  = %s" % str(inputdir))
        LOG("checking on lookup table file... ")
        try:
            lutmapper = PathMapper.file_mapper(inputdir, outputdir, glob = options.lut)
        except Exception as e:
            LOG(f"{e}", comms = "error")
            d_ret['isOK'] = False
        if not lutmapper.is_empty():
            for path_lutfile, path_outlut in lutmapper: pass
        else:
            LOG(f"I could not find {options.lut} in the input space", comms = 'error')
            d_ret['isOK'] = False
    else:
        LOG(f"Lookup table parent directory {inputdir} not found!", comms = 'error')
        d_ret['isOK'] = False
    if path_lutfile:
        LOG(path_lutfile)
        d_ret['lookupTableFile']    = path_lutfile
        LUT = lookuptable.lookuptable(lut = path_lutfile, log = LOG)
    else:
        LOG(f"No lookup table file found!", comms = 'error')
    return d_ret

def report_generate(options: Namespace, inputfile: Path, outputfile: Path):
    """Main entry point for generating a report in various formats based
    off a FreeSurfer annotation file.

    Args:
        options (Namespace): The option space, needed to determine report types.
        inputfile (Path): The input file to process
        outputfile (Path): The corresponding outputfile path
    """
    LOG(f"Generating a report off {inputfile}")


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
    print(f'Options: {options}', file=sys.stderr)

    if init(options, inputdir, outputdir)['isOK']:
        mapper = PathMapper.file_mapper(inputdir, outputdir,
                            glob    = options.annotation
        )
        for input, output in mapper:
            report_generate(options, input, output)


if __name__ == '__main__':
    main()

