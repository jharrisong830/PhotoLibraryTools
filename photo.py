class Photo:
    def __init__(self, basename: str, files: list[str], isGrouped: bool):
        self.basename = basename
        self.files = files
        self.isGrouped = isGrouped
    
    def __str__(self):
        sb = ""
        if not self.isGrouped: sb += "(NOT GROUPED) "
        sb += f"{self.basename}:\n"
        for file in self.files:
            sb += f"\t{file}\n"
        return sb
    
    def __repr__(self):
        sb = ""
        if not self.isGrouped: sb += "(NOT GROUPED) "
        sb += f"{self.basename}:\n"
        for file in self.files:
            sb += f"\t{file}\n"
        return sb
    
    def to_dict(self):
        return {
            "basename": self.basename,
            "files": self.files,
            "isGrouped": self.isGrouped
        }
