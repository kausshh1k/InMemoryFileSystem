class Directory:
    def __init__(self, directory_name):
        self.directory_name = directory_name
        self.files = {}
        self.directories = {}
        self.parentDirectory = None