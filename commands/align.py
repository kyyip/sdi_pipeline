"""
align -- this module aligns sets of astronomical data
HISTORY
    Created/Substantially refactored on 2019-09-01
        Varun Iyer <varun_iyer@ucsb.edu>
"""
# general imports

import click
import sdi
import numpy as np
# types
from common import to_np, HDU_TYPES
from astropy.io.fits import PrimaryHDU, HDUList
#from sources import Source
import astroalign
from scripts import snr

@sdi.cli.command("align")
@click.option("-n", "--name", default="SCI", help="The HDU to be aligned.")
@sdi.operator
#TODO use CAT sources if they exist
def align(hduls, name="SCI", reference=None):
    """
    Aligns the source astronomical image(s) to the reference astronomical image
    \b
    :param hduls: list of fitsfiles
    :return: list of fistfiles with <name> HDU aligned
    """

    hduls_list = [hdul for hdul in hduls]
    sources = [hdul[name] for hdul in hduls_list]
    outputs = []

    if reference is None:
        reference = snr.snr(hduls_list, name)[name]
    # click.echo(reference.header["ORIGNAME"])
    # FIXME log ref name
    np_ref = to_np(reference, "Cannot align to unexpected type {}; expected numpy array or FITS HDU")

    for source in sources:
        np_src = to_np(source, "Cannot align unexpected type {}; expected numpy array or FITS HDU")
        # possibly unneccessary but unsure about scoping
        output = np.array([])

        output = astroalign.register(np_src, np_ref)[0]
        if isinstance(source, HDU_TYPES):
            output = PrimaryHDU(output, source.header)
        outputs.append(HDUList([output]))

    return (hdul for hdul in outputs)
