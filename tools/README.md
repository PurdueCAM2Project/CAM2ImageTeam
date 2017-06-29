<link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet"> 
<div markdown="1" style="font-family: 'Ubuntu', sans-serif">

# Image Team Tools

## DirectoryToFile *(directorytofile.py)*
Writes the filenames inside a specified directory to an output file, 1 line at a time. Useful for creating lists of images in a batch to pass to an object detector.  You can also use the Python API from this tool.

### Terminal Usage
```
python directorytofile.py [PATH TO DIRECTORY] [OUTPUT FILE PATH]
```
The output file's format on each line will be:
```[ABSOLUTE PATH TO DIRECTORY]/filename.filetype```

Optionally:
```
python directorytofile.py [PATH TO DIRECTORY] [OUTPUT FILE PATH] [PREFIX]
```
In which case, each line in the output file will follow this format:
```[PREFIX]/filename.filetype```

</div>
