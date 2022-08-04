import sys
from pathlib import Path
from unittest.mock import call
import  pudb
from freesurfer_simplereport import parser, main, DISPLAY_TITLE

str_notes = '''

    Some tests for diff_unpack.py. Note, if you want to debug tests
    with `pudb`, make sure to

        pytest -s

'''

def test_main(tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir    = tmp_path / 'incoming'
    outputdir   = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options     = parser.parse_args(['--verbosity', '1'])

    # This doesn't really test much of anything.
    main(options, inputdir, outputdir)

