str_about = '''
    A module/class to hold a report template. This template is derived
    from the mgz file and the lookup table, and then processed by the
    convert class to generate outputs.
'''

import  pandas  as      pd
import  pudb

class template:
    '''
    A class that holds the master report template
    '''

    def log(self, *args, **kwargs):
        if self.logger:
            self.logger(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        """Constructor
        """

        self.logger                 = None
        self.lut                    = None
        self.mgz                    = None
        self.initOK : bool          = False
        self.rep                    = None

        for k,v in kwargs.items():
            if k == 'log'       :   self.logger         = v
            if k == 'lut'       :   self.lut            = v
            if k == 'mgz'       :   self.mgz            = v

        self.log('Generating report master template')
        if self.lut and self.mgz:
            self.l_colheaders       : list  = ['Index', 'Label Name', 'Volume (cc)']
            self.rep                : DataFrame = pd.DataFrame(columns = self.l_colheaders)
            line_count              : int   = 1
            for k in sorted(self.mgz.Counter().keys()):
                self.log(f"\tcounting {k}", level = 2)
                self.df_cc  = self.lut.df_FSColorLUT.loc[self.lut.df_FSColorLUT['#No'] == str(k), ['LabelName']]
                self.log('\trecording vol...', level = 2)
                self.rep.loc[len(self.rep)] = [line_count, self.df_cc['LabelName'].to_string(index = False), round(self.mgz.Counter()[k]/1000,1)]
                str_annot = f'{self.rep.loc[len(self.rep)-1]}'
                self.log(" ".join(str_annot.split()), level = 3)
                line_count+=1
        else:
            if not self.lut: self.log("Lookup table not valid!", comms = 'error')
            if not self.mgz: self.log("Annotation data not valid!", comms = 'error')
        self.initOK     = True
