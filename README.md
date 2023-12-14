# InMemoryFileSystem
The file system primarily relies on the classes Directory and File. It has a currentDirectory pointer that always points to one of the directory in the file system tree. Every Directory and File object will have a parentDirectory pointer that points to another Directory object referring as its parent directory, except root that points to None.

![Frame 4](https://github.com/kausshh1k/InMemoryFileSystem/assets/120456820/719a5ecf-b512-4bc5-b558-4db0fe37403d)


## The file system has the following commands:
1. `mkdir`: Create a new directory.
2. `cd`: Changes the current directory. Support navigating to the parent directory using `..`, moving to the root directory using `/`, and navigating to a specified absolute path. Basically anything that you can do in a normal terminal. Since there is no user level implementation, ~ and / should take you to root.
3. `ls`: List the contents of the current directory or a specified directory.
4. `grep`: Search for a specified pattern in a file. **PS: Its a bonus**
5. `cat`: Display the contents of a file.
6. `touch`: Create a new empty file.
7. `echo`: Write text to a file. ex - `echo 'I am "Finding" difficult to write this to file' > file.txt`
8. `mv`: Move a file or directory to another location. ex - `mv /data/ice_cream/cassata.txt ./data/boring/ice_cream/mississippimudpie/`
9. `cp`: Copy a file or directory to another location. ex - `cp /data/ice_cream/cassata.txt .` **. For current directory **
10. `rm`: Remove a file or directory.

# Saving/Loading File System State
The file system uses pickle package to save and load the previously stored states from memory.
![Screenshot 2023-12-14 192814](https://github.com/kausshh1k/InMemoryFileSystem/assets/120456820/24907bf5-f90e-4b51-a527-6d2694e85087)
