import sdi
import click
import ois
import os
from astropy.io import fits
from common import to_np

@sdi.cli.command("subtract")
@sdi.operator
def subtract(hduls):
    """
    Returns differences of a set of images from a template image
    Arguments:
        hduls --list of fits hdul's where the last image is the template 
        image that the other images will be subtracted from
    """
    hduls_list = [hdul for hdul in hduls]
    output = []
    outputs = []
    template = to_np(hduls_list[-1][0])
    for hdu in hduls[:-1]:
        diff = ois.optimal_system(image=hdu["SCI"].data, refimage=template, method='Bramich')
        output.append(diff)     

    for array_set in output:
        for item in array_set:
            hdu = fits.PrimaryHDU(item)
            outputs.append(fits.HDUList([hdu])) 
    return (hdul for hdul in outputs)
