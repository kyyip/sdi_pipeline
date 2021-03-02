import click
import sdi
from astropy.io import fits
import glob

@sdi.cli.command("read")
@click.option('-d', '--directory', type=str, help="Specify path to directory of fitsfiles.", required=True)
@sdi.generator
def read(directory):
    paths = glob.glob("{}/*.fits*".format(directory))
    hduls = [fits.open(p) for p in paths]
    return hduls

@sdi.cli.command("write")
@click.option('-d', '--directory', type=str, help="Specify path to directory to save fitsfiles.", default="./")
@click.option('-f', '--format', type=str, help="Specify string format for filename.", default="{number}.fits")
@sdi.operator
def write(hduls, directory, format):
    for i, h in enumerate(hduls):
        print((directory + format).format(number=i))
        h.writeto((directory + format).format(number=i))
    return hduls
