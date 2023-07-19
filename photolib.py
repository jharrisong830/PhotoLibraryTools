import os
import re
import shutil
from photo import Photo
import json


class PhotoLibrary:
    def __init__(self, path: str):
        self.path = ""
        self.dirFiles = []
        self.photos = []
        self.setup(path)
        self.toJson()
    

    def __str__(self):
        sb = f"Photo Library @ {self.path}:\n\n"
        for photo in self.photos:
            sb += str(photo)
        return sb
    

    def __repr__(self):
        sb = f"Photo Library @ {self.path}:\n\n"
        for photo in self.photos:
            sb += str(photo)
        return sb
    

    def toJson(self):
        with open("photolib.json", "w") as f:
            json.dump({
                "loc": self.path,
                "items": [x.to_dict() for x in self.photos]
                }, f, indent=4)


    def setup(self, path):
        '''helper for __init__'''
        self.setPath(path)
        self.setDirFiles()
        self.setPhotos()


    def setPath(self, path):
        '''re-initializes the main directory for the photo library'''
        os.chdir(path)
        self.path = os.path.abspath(path)
    

    def setDirFiles(self):
        '''re-initializes file names'''
        self.dirFiles = os.listdir()
        if ".DS_Store" in self.dirFiles: self.dirFiles.remove(".DS_Store")
        if "photolib.json" in self.dirFiles: self.dirFiles.remove("photolib.json")
        self.aaeCorrections()


    def aaeCorrections(self):
        '''Removes extraneous "O" characters from .aae filenames'''
        for file in self.dirFiles:
            if re.search(r".aae$", file) != None:
                newName = re.sub(r"IMG_O", "IMG_", file)
                if newName != file:
                    print(f"RENAMING: {file} -> {newName}")
                    os.rename(file, newName)
        self.dirFiles = os.listdir()
        if ".DS_Store" in self.dirFiles: self.dirFiles.remove(".DS_Store")
        if "photolib.json" in self.dirFiles: self.dirFiles.remove("photolib.json")


    def setPhotos(self):
        '''initializes a table of file basenames and their corresponding files'''
        tempTable = {}
        self.photos = []
        for file in self.dirFiles:
            if os.path.isdir(file):
                self.photos.append(Photo(file, os.listdir(file), True))
            else:
                base = file.split('.')[0]
                if base not in tempTable:
                    tempTable[base] = [file]
                else: tempTable[base] += [file]
        for basename, files in tempTable.items():
            self.photos.append(Photo(basename, files, False))

    
    def separateImagesToFolders(self):
        '''For each file basename in self.filenameTable, create a subfolder and store all related files there'''
        for photo in self.photos:
            if not photo.isGrouped:
                os.mkdir(photo.basename)
                self.dirFiles.append(photo.basename)
                for file in photo.files:
                    shutil.move(f"./{file}", f"{photo.basename}/{file}")
                    self.dirFiles.remove(file)
                photo.isGrouped = True
        self.toJson()

    def ungroupAll(self):
        '''Ungroups all images, bringing them to the root of the library and removing their folders'''
        for photo in self.photos:
            if photo.isGrouped:
                for file in photo.files:
                    self.dirFiles.append(file)
                    shutil.move(f"{photo.basename}/{file}", f"./{file}")
                photo.isGrouped = False
                self.dirFiles.remove(photo.basename)
                os.rmdir(photo.basename)
        self.toJson()

