# music-visualisation

This library converts sheet music in musicxml format to visualisations that refer to notes and chords with their relative position within the key of the song. More about how this notational system works [here](https://jessevoostrum.github.io/music-visualisation/). 

### running the code
From the root folder of the repository, run the following line in the terminal:

``` $ python run.py <path to song> <output directory> ```

```<path to song>``` should be the absolute path to the musicxml file, that you wish to convert. (can be either .mxl or .musicxml) 
```<output directory>``` is the location where you would like the output pdf file to be stored. 

### requirements
- music21
- matplotlib


### example musicxml files
In the folder example, there are some musicxml files that can be used to try out the program. 