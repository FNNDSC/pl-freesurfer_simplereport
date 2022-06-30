str_about = '''
    The lookuptable module provides abstractions on handling/using
    a FreeSurfer lookup table for mapping indices in a volume file
    to named structures (as well as their rendering color).
'''

from pathlib import Path
import pandas as pd
import re

class lookuptable:
    '''
    A class that handles lookuptables and provides some useful
    functionality.
    '''

    def log(self, *args):
        if self.logger:
            self.logger(*args)

    def __init__(self, *args, **kwargs):
        """Constructor
        """

        self.path_lutfile   : Path  = None
        self.l_colheaders   : list  = [ "#No", "LabelName", "R", "G", "B" ]
        self.df_FSColorLUT          = pd.DataFrame(columns=self.l_colheaders)
        self.logger                 = None

        for k,v in kwargs.items():
            if k == 'lut'       :   self.path_lutfile   = v
            if k == 'log'       :   self.logger         = v

        if self.path_lutfile.exists():
            with open(self.path_lutfile) as f:
                for line in f:
                    if line and line[0].isdigit():
                        line        = re.sub(' +', ' ', line)
                        l_line      = line.split(' ')
                        l_labels    = l_line[:5]
                        self.df_FSColorLUT.loc[len(self.df_FSColorLUT)] = l_labels

        self.log("Lookup file read")
