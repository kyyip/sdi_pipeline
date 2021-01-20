from functools import update_wrapper
import click
from inspect import signature, _empty

@click.group(chain=True)
def cli():
    """
    The overall chaned click group
    """

@cli.resultcallback()
def run_pipeline(operators):
    """
    Callback is invoked with an iterable of all subcommands
    """
    # a list of fitsfiles passed through the whole pipeline
    hduls = ()
    for operator in operators:
        hduls = operator(hduls)

    for _ in hduls:
        # do necessary things on overall outputs
        pass

def operator(func):
    """
    Decorator which wraps commands so that they return functions after being
    run by click.
    All of the returned functions are passed as an iterable
    into run_pipeline.
    """
    @cli.command(func.__name__)
    def new_func(*args, **kwargs):
        def operator(hduls):
            # args and kwargs are subcommand-specific
            return func(hduls, *args, **kwargs)
        return operator

    # basically return new_func, but better
    return update_wrapper(new_func, func)

def generator(func):
    """
    Does what operator does, but for the first thing in the series, like
    opening the hduls.
    Works with sub-funcs that do not have 'hduls' as the first argument.
    """
    def new_func(hduls, *args, **kwargs):
        yield from hduls
        yield from func(*args, **kwargs)
    return operator(update_wrapper(new_func, func))