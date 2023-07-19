from sys import argv
import os
from photolib import PhotoLibrary

USAGE = f"Usage: {os.path.basename(argv[0])} <path/to/photolib> [folders | ungroup | print]"
OPTS = ["folders", "print", "ungroup"]
        

        

if __name__ == "__main__":
    if len(argv) != 3:
        print(USAGE)
        exit(0) if len(argv) == 1 else exit(1)
    if argv[2] not in OPTS:
        print(USAGE)
        exit(1)
    if not os.path.exists(argv[1]):
        print("Invalid Directory")
        print(USAGE)
        exit(1)

    pl = PhotoLibrary(argv[1])
    if argv[2] == "folders":
        pl.separateImagesToFolders()
    elif argv[2] == "print":
        print(pl)
    elif argv[2] == "ungroup":
        pl.ungroupAll()
    exit(0)  
    

