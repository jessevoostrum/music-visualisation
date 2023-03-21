# music-visualisation

This library converts sheet music in musicxml format to visualisations that refer to notes and chords with their relative position within the key of the song. More about how this notational system works [here](https://integerbook.com/about). 

### running the code
From the root folder of the repository, run the following line in the terminal:

``` $ python run.py ```

This will convert the file "All_Of_Me.musicxml" located in the examples folder and place the result in the root folder of the repository. 

The most important options are the following:
- -s set song path (can be either .musicxml or .mxl file)
- -o set output directory  (without "/" at the end)

example: 
``` $ python run.py -s "/Users/jvo/Documents/music-visualisation/example/Summertime.musicxml" -o "/Users/jvo/Downloads/output" ```

Further options include:
- -b for bassline output
- -l for printing lyrics
- -c for colouring notes according to circle of fifths
- -r for realbook font (note that you first have to install the font (located in fonts folder))
- -cn for printing chord notes
- -cp for printing chord progressions (no melody, 8 measures per line)
- -d <path-to-settings-dictionary> can be used to pass a custom settings dictionary. (most flexible) See 'sample/settings.json' for the default settings.

### requirements
- music21
- matplotlib


### example musicxml files
In the folder example, there are some musicxml files that can be used to try out the program. 