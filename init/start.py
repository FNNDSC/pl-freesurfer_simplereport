str_about = '''
    Simply module to provide some startup initializations.
'''

import  sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


from    pathlib                 import Path
from    argparse                import Namespace

import  pfmisc
from    pfmisc._colors          import Colors

from    chris_plugin            import chris_plugin, PathMapper

from    lut                     import lookuptable

import  pudb

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
