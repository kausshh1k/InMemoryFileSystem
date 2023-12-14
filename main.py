import json
import pickle

from file import File
from directory import Directory



class InMemoryFileSystem:
    def __init__(self):
        self.root = Directory('tatti')
        self.currentDirectory = self.root

    
    
    def mkdir(self, path):
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]))
            self.currentDirectory = temp
            directory_name = path.split('/')[-1]
            if not check:
                return
            elif directory_name in curr.directories:
                print(f'Directory {directory_name} already exist.')
            else:
                new_directory = Directory(directory_name)
                curr.directories[directory_name] = new_directory
                new_directory.parentDirectory = curr
        
        else:
            directory_name = path
            if directory_name in self.currentDirectory.directories:
                print(f'Directory {directory_name} already exist.')
            else:
                new_directory = Directory(directory_name)
                self.currentDirectory.directories[directory_name] = new_directory
                new_directory.parentDirectory = self.currentDirectory
                
    
    def cd(self, path, prompt=True):
        if path == '~' or path == '/':
            self.currentDirectory = self.root
            return
        elif path.startswith('/'):
            path = path[1:].split('/')
            curr = self.root
            for directory in path:
                if directory not in curr.directories:
                    if prompt: print('Path does not exist.')
                    return [False, None]
                else:
                    curr = curr.directories[directory]
            self.currentDirectory = curr
            return [True, curr]

        else:
            path = path.strip('/').split('/')
            curr = self.currentDirectory
            for directory in path:
                if directory == '..':
                    if curr == self.root:
                        print('Path does not exist.')
                        return [False, None]
                    curr = curr.parentDirectory
                elif directory not in curr.directories:
                    print('Path does not exist.')
                    return[False, None]
                else:
                    curr = curr.directories[directory]
            self.currentDirectory = curr
            return [True, curr]
    
    def ls(self, path=None):
        if not path:
            for directory in self.currentDirectory.directories:
                print(f'{self.currentDirectory.directories[directory].directory_name}/')
            for file in self.currentDirectory.files:
                print(self.currentDirectory.files[file].file_name)
        else:
            temp = self.currentDirectory
            check, curr = self.cd(path)
            # print(check, curr)
            self.currentDirectory = temp
            if not check: return
            else:
                for directory in curr.directories:
                    print(f'{curr.directories[directory].directory_name}/')
                for file in curr.files:
                    print(curr.files[file].file_name)
    
    def grep(self, pattern, path):
        pass
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]))
            self.currentDirectory = temp
            file_name = path.split('/')[-1]
            if not check:
                return
            elif file_name not in curr.files:
                print(f'File {file_name} does not exist.')
            else:
                file = curr.files[file_name]
                for idx, line in enumerate(file.content):
                    if pattern in line:
                        print(idx, line)

        
        else:
            file_name = path
            if file_name not in self.currentDirectory.files:
                print(f'File {file_name} does not exist.')
            else:
                file = self.currentDirectory.files[file_name]
                for idx, line in enumerate(file.content):
                    if pattern in line:
                        print(idx, line)

    
    def cat(self, path):
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]))
            self.currentDirectory = temp
            file_name = path.split('/')[-1]
            if not check:
                return
            elif file_name not in curr.files:
                print(f'File {file_name} does not exist.')
            else:
                file = curr.files[file_name]
                for line in file.content:
                    print(line)
        else:
            file_name = path
            if file_name not in self.currentDirectory.files:
                print(f'File {file_name} does not exist.')
            else:
                file = self.currentDirectory.files[file_name]
                for line in file.content:
                    print(line)
    
    def touch(self, path):
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]))
            self.currentDirectory = temp
            file_name = path.split('/')[-1]
            if not check:
                return
            elif file_name in curr.files:
                print(f'File {file_name} already exist.')
            else:
                new_file = File(file_name)
                curr.files[file_name] = new_file
                new_file.parentDirectory = curr
        
        else:
            file_name = path
            if file_name in self.currentDirectory.files:
                print(f'File {file_name} already exist.')
            else:
                new_file = File(file_name)
                self.currentDirectory.files[file_name] = new_file
                new_file.parentDirectory = self.currentDirectory

    def echo(self, line, path):
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]))
            self.currentDirectory = temp
            file_name = path.split('/')[-1]
            if not check:
                return
            elif file_name not in curr.files:
                print(f'File {file_name} does not exist.')
            else:
                file = curr.files[file_name]
                file.content.append(line)
        else:
            file_name = path
            if file_name not in self.currentDirectory.files:
                print(f'File {file_name} does not exist.')
            else:
                file = self.currentDirectory.files[file_name]
                file.content.append(line)
    
    def mv(self, path1, path2):
        temp = self.currentDirectory
        check1, curr1 = self.cd(path1, False)
        check2, curr2 = self.cd(path2, False)
        self.currentDirectory = temp

        if not check1 or not check2:
            if not check1:
                print(f'Path {path1} does not exist.')
            if not check2:
                print(f'Path {path2} does not exist.')
            return
        
        fileOrDirectory = path1.split('/')[-1]
        if fileOrDirectory not in curr1.files and fileOrDirectory not in curr1.directories:
            print(f'File/Directory does not exist at {path1}.')
            return
        elif fileOrDirectory in curr1.files:
            curr2.files[fileOrDirectory] = curr1.files[fileOrDirectory]
            del curr1.files[fileOrDirectory]
        else:
            curr2.directories[fileOrDirectory] = curr1.directories[fileOrDirectory]
            del curr1.directories[fileOrDirectory]
    
    def cp(self, path1, path2):
        temp = self.currentDirectory
        check1, curr1 = self.cd(path1, False)
        check2, curr2 = self.cd(path2, False)
        self.currentDirectory = temp

        if not check1 or not check2:
            if not check1:
                print(f'Path {path1} does not exist.')
            if not check2:
                print(f'Path {path2} does not exist.')
            return
        
        fileOrDirectory = path1.split('/')[-1]
        if fileOrDirectory not in curr1.files and fileOrDirectory not in curr1.directories:
            print(f'File/Directory does not exist at {path1}.')
            return
        elif fileOrDirectory in curr1.files:
            curr2.files[fileOrDirectory] = curr1.files[fileOrDirectory]
        else:
            curr2.directories[fileOrDirectory] = curr1.directories[fileOrDirectory]
    
    def rm(self, path):
        if len(path.split('/')) > 1:
            temp = self.currentDirectory
            check, curr = self.cd('/'.join(path.split('/')[:-1]), False)
            self.currentDirectory = temp
            fileOrDirectory = path.split('/')[-1]
            if not check:
                return
            elif fileOrDirectory not in curr.files and fileOrDirectory not in curr.directories:
                print('File/Directory does not exist.')
            else:
                if fileOrDirectory in curr.files:
                    del curr.files[fileOrDirectory]
                elif fileOrDirectory in curr.directories:
                    del curr.directories[fileOrDirectory]
        
        else:
            fileOrDirectory = path
            if fileOrDirectory not in self.currentDirectory.files and fileOrDirectory not in self.currentDirectory.directories:
                print('File/Directory does not exist.')
            else:
                if fileOrDirectory in self.currentDirectory.files:
                    del self.currentDirectory.files[fileOrDirectory]
                elif fileOrDirectory in self.currentDirectory.directories:
                    del self.currentDirectory.directories[fileOrDirectory]
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    # def save_state(self, file_path):
    #     with open(file_path, 'w') as f:
    #         json.dump()

    # def load_state(self, path):
    #     pass

def main():
    fs = InMemoryFileSystem()
    while True:
        curr_path = []
        curr = fs.currentDirectory
        while curr:
            curr_path.append(curr.directory_name)
            curr = curr.parentDirectory
        
        command = input(f'{'/' + '/'.join(curr_path[::-1])} ~ ').strip().split()

        method = command[0]
        args = command[1:]
        if method == 'exit':
            break
        elif method == 'mkdir':
            if not args:
                continue
            fs.mkdir(args[0])
        elif method == 'cd':
            if not args:
                continue
            fs.cd(args[0])
        elif method == 'ls':
            if not args:
                fs.ls()
            else:
                fs.ls(args[0])
        elif method == 'grep':
            if not args:
                continue
            if len(args) < 2:
                continue
            fs.grep(args[0], args[1])
        elif method == 'cat':
            if not args:
                continue
            fs.cat(args[0])
        elif method == 'touch':
            if not args:
                continue
            fs.touch(args[0])
        elif method == 'echo':
            if not args:
                continue
            if len(args) < 2:
                continue
            text = ''
            if args[-2] == '>':
                text = ' '.join(args[0:-2])
            else:
                text = ' '.join(args[0:-1])
            fs.echo(text, args[-1])
        elif method == 'mv':
            if not args: continue
            fs.mv(*args)
        elif method == 'cp':
            if not args: continue
            fs.cp(*args)
        elif method == 'rm':
            if not args: continue
            fs.rm(*args)
        elif method == 'save':
            if not args: continue
            try:
                print(args[0], type(args[0]))
                with open(args[0], 'wb') as f:
                    pickle.dump(fs.root, f)
            except FileNotFoundError as e:
                print(e)
        elif method == 'load':
            if not args: continue
            try:
                with open(args[0], 'rb') as f:
                    fs.root = pickle.load(f)
                    fs.currentDirectory = fs.root
                    print(fs.root.directory_name, type(fs.root))
            except:
                print('Path does not exist.')
        else:
            print(f"Command not recognized: {method}")

main()