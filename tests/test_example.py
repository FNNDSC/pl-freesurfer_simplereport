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


#options         = parser.parse_args(['--inputFilter', '*dcm'])


#def test_inputDir2File_do_skips_dirs_without_hits(tmp_path: Path):
    #inputdir    = tmp_path / 'inputdir'
    #outputdir   = tmp_path / 'outputdir'
    #inputdir.mkdir()
    #outputdir.mkdir()

    #file        = inputdir / 'file.txt'
    #file.write_text('I am not a DICOM file.')

    #assert inputDir2File_do(options, (inputdir, outputdir)) is None


#def test_inputDir2File_do_returns_a_dicom(tmp_path: Path):
    #inputdir    = tmp_path / 'inputdir'
    #outputdir   = tmp_path / 'outputdir'
    #inputdir.mkdir()
    #outputdir.mkdir()
    ## create example data
    #dicoms = {
        #inputdir / 'file1.dcm',
        #inputdir / 'file2.dcm',
        #inputdir / 'file3.dcm'
    #}

    #for dicom in dicoms:
        #dicom.touch()

    #actual = inputDir2File_do(options, (inputdir, outputdir))
    #assert actual is not None
    #actual_dicom, actual_outputdir = actual
    #assert actual_dicom in dicoms
    #assert actual_outputdir == outputdir

def test_main(mocker, tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir    = tmp_path / 'incoming'
    outputdir   = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    options     = parser.parse_args(['--verbosity', '1'])

    #mock_print  = mocker.patch('builtins.print')
    main(options, inputdir, outputdir)
    # mock_print.assert_has_calls([call(DISPLAY_TITLE), call("Option ")])

    expected_output_file = outputdir / 'success.txt'
    # assert expected_output_file.exists()
    # assert expected_output_file.read_text() == 'did nothing successfully!'
