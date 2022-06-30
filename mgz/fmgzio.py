str_about = """
    An mgz interpreting module.
"""

from    pathlib                 import Path
from    argparse                import Namespace

import  pfmisc
from    pfmisc._colors          import Colors

import  pudb

import  nibabel                 as nib
import  numpy                   as np
import  collections

class mgz:
    '''
    Read/load and process mgz files, also providing some
    data related services.
    '''

    def log(self, *args, **kwargs):
        if self.logger:
            self.logger(*args, **kwargs)

    def Counter(self, *args):
        if len(args):
            self.counter    = args[0]
        return self.counter

    def __init__(self, mgzFile: Path, *args, **kwargs):

        self.logger                 = None
        self.b_loadOK       : bool  = False
        self.initOK         : bool  = False

        self.fmgz                   = None
        self.vol_data               = None
        self.vect_data              = None
        self.counter                = None
        self.logger                 = None

        for k,v in kwargs.items():
            if k == 'log'   :   self.logger     = v

        self.log(f"Reading input mgz file {mgzFile}...")
        try:
            self.fmgz       = nib.load(str(mgzFile))
            self.b_loadOK   = True
        except:
            self.log(f"Could not read file {mgzFile}!", comms = 'error')
        if self.b_loadOK:
            self.log(f"\textracting volume...")
            self.vol_data   = self.fmgz.get_fdata().astype(np.uint32)
            self.log(f"\tvectorizing volume...")
            self.vect_data  = self.vol_data.flatten()
            self.log(f"\tgenerating counter...")
            self.counter    = collections.Counter(self.vect_data)
            self.initOK     = True
        else:
            self.initOK     = False
        self.log(f"mgz initialization {self.initOK}")