from sssg.site import Site
import sssg.liveupdate # circular dependency resolution

import sys
import os

def main(args=sys.argv):
    command = args[1]

    if command == "rebuild":
        cwd = os.getcwd()
        site = Site.from_directory(cwd)
        site.rebuild()
    elif command == "deploy":
        os.execv('/bin/sh', ['/bin/sh', '.deploy'])
    elif command == "update":
        sssg.liveupdate.liveupdate()
