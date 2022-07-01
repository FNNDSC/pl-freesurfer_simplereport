str_about = """
    A module that handles conversions to various output formats.
"""

import  pudb
from    pathlib import Path
from    yattag  import Doc
import  weasyprint

import  logging
weasylog = logging.getLogger("weasyprint")
weasylog.setLevel(logging.CRITICAL)
fontlog = logging.getLogger("fontTools")
fontlog.setLevel(logging.CRITICAL)

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
        self.template               = None
        self.format         : str   = ''
        self.reportprefix   : str   = ''
        self.fh                     = None

        for k,v in kwargs.items():
            if k == 'log'       :   self.logger         = v
            if k == 'template'  :   self.template       = v
            if k == 'basename'  :   self.reportprefix   = v
            if k == 'format'    :   self.format         = v

    def do(self, outputpath : Path) -> list:
        """Main entry point for generating the reports.
        """
        ld_ret   : list   = []
        for reporttype in self.format.split(','):
            if 'json' in reporttype.lower():    d_save = self.format_save(outputpath, self.template.rep.to_json(orient = 'index'), 'json')
            if 'csv'  in reporttype.lower():    d_save = self.format_save(outputpath, self.template.rep.to_csv(index = False), 'csv')
            if 'txt'  in reporttype.lower():    d_save = self.format_save(outputpath, self.template.rep.to_string(index = False), 'txt')
            if 'html' in reporttype.lower():    d_save = self.format_save(outputpath, self.html_generate(), 'html')
            if 'pdf'  in reporttype.lower():    d_save = self.format_save(outputpath, self.pdf_generate(), 'pdf')
            ld_ret.append(d_save)

    def fullyQualifiedOuputReportFile_createName(self, outputpath : Path, ext : str) -> Path:
        """Generate a fully qualified output report filename

        Args:
            outputpath (Path): outputpath (corresponding to inputpath file location)
            ext (str): string extension

        Returns:
            Path: the actual Path name of the output file
        """
        if ext[0] != '.': ext = '.' + ext

        prefix  : str   = str(outputpath.parent / Path(self.reportprefix + '_'))
        full    : str   = prefix + str(outputpath.name) + ext

        FQ : Path = Path(full)
        return FQ

    def html_generate(self):
        """Generate an html report
        """
        doc, tag, text  = Doc().tagtext()
        line_count      = 1
        with tag('html'):
            with tag('head'):
                with tag('link',rel='stylesheet' ,href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css"):
                    with tag('style'):
                        text('body{margin:0 100; background:whitesmoke;}')
            with tag('body'):
                with tag('h1'):
                    text('Brain Segmentation Report')
                with tag('table', id = 'main', klass='table table-striped table-hover',text='report'):
                    with tag('thead',klass='thead-dark'):
                        with tag('tr'):
                            with tag('th',scope='col'):
                                text('Index')
                            with tag('th',scope='col'):
                                text('Label Name')
                            with tag('th',scope='col'):
                                text('Volume (in cc)')
                    for k in sorted(self.template.mgz.counter.keys()):
                        res_df = self.template.lut.df_FSColorLUT.loc[self.template.lut.df_FSColorLUT['#No'] == str(k),['LabelName']]
                        with tag('tr'):
                            with tag('td'):
                                text(line_count)
                            with tag('td'):
                                text(res_df['LabelName'].to_string(index=False))
                            with tag('td'):
                                text(round(self.template.mgz.counter[k]/1000,1))
                        line_count = line_count + 1
        return doc.getvalue()

    def pdf_generate(self):
        """Generate a PDF by first creating an HTML document and then converting it.
        """
        doc_pdf = weasyprint.HTML(string=self.html_generate())
        return doc_pdf

    def format_save(self, outputpath : Path, fconvert, ext: str) -> dict:
        """The main saving method. It provides idiomatic operations on determining
        the outuput file location, and then calls the passed `fconvert` to
        do the actual saving.

        Args:
            outputpath (Path): the original ouptut path location
            fconvert (any type): the payload to save
            ext (str): the extension string

        Returns:
            dict: a status dictionary
        """
        FQ: Path    = self.fullyQualifiedOuputReportFile_createName(outputpath, ext)
        self.logger(f"Saving:  {FQ.parent / FQ.name}")
        self.fh     = open(FQ, 'a')
        self.fh.truncate(0)
        if ext == 'pdf':
            fconvert.write_pdf(FQ)
        else:
            self.fh.write(fconvert)
        self.fh.close()
        return {
            'status':   True,
            'path':     FQ
        }
