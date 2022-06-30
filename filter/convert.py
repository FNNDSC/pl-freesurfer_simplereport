str_about = """
    A module that handles conversions to various output formats.
"""

class format:
    '''
    Depending on some condition, format a data object in a variety
    of ways.
    '''

    def log(self, *args, **kwargs):
        if self.logger:
            self.logger(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        """Constructor
        """

        self.logger                 = None

        for k,v in kwargs.items():
            if k == 'log'       :   self.logger         = v
