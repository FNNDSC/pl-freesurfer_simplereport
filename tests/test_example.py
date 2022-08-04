import sys
from pathlib import Path
from unittest.mock import call
import  pudb
from freesurfer_simplereport import parser, main, DISPLAY_TITLE

str_notes = '''

    Some trivial test. Note, be sure to run tests with

        pytest -s

    (this is also pudb.set_trace() safe)
'''

def test_main(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir    = tmp_path / 'incoming'
    outputdir   = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    inputfiles = {
        inputdir / 'FreeSurferColorLUT.txt',
        inputdir / 'file1.aparc.mgz',
        inputdir / 'file2.aparc.mgz',
        inputdir / 'file3.aparc.mgz'
    }

    for ifile in inputfiles:
        ifile.touch()

    options     = parser.parse_args(['--verbosity', '1'])
    # pudb.set_trace()
    # This doesn't really test much of anything.
    # main(options, inputdir, outputdir)

