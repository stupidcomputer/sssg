from sssg.site import Site
import sssg.liveupdate # circular dependency resolution

import sys
import os

def main(args=sys.argv):
    try:
        command = args[1]
    except IndexError:
        command = "nonexistent"

    if command == "rebuild":
        cwd = os.getcwd()
        site = Site.from_directory(cwd)
        site.rebuild()
    elif command == "deploy":
        os.execv('/bin/sh', ['/bin/sh', '.deploy'])
    elif command == "update":
        sssg.liveupdate.liveupdate()
    else:
        help_text = """
sssg - the stupid static site generator

usage: sssg [verb]

verb: one of
    rebuild -- rebuilds the static site into output/
    deploy -- executes the deploy script
    update -- rebuild the static site upon any change
"""

        print(help_text)
