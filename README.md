# music-visualisation

This library converts sheet music in musicxml format to visualisations that refer to notes and chords with their relative position within the key of the song. More about how this notational system works [here](https://integerbook.com/about). 

### installation

1. Download python
2. install the [integerbook package](https://pypi.org/project/integerbook/0.0.2/) using pip: ``` $ pip install integerbook ```
3. Download or copy the file ```run.py``` from the github repository to a folder on your computer, e.g. ```~/Documents/music-visualisation```.


### running the code
1. In the terminal, navigate to the folder where ```run.py``` is stored, e.g. ```~/Documents/music-visualisation```. 
2. In the terminal, type: ``` $ python run.py -s <path-to-song>```  e.g.   
``` $ python run.py -s "/Users/jvo/Documents/music-visualisation/example/Summertime.musicxml" ```

This will convert the musicxml file you specified to a pdf and store it in the current folder. 

Further options include:
- -o set output directory  (without "/" at the end)
- -b for bassline output
- -l for printing lyrics
- -c for colouring notes according to circle of fifths
- -cn for printing chord notes
- -cp for printing chord progressions (no melody, 8 measures per line)
- -d <path-to-settings-dictionary> can be used to pass a custom settings dictionary. (most flexible) See ```src/integerbok/settings.json``` for the default settings.


### example musicxml files
In the folder example, there are some musicxml files that can be used to try out the program. 