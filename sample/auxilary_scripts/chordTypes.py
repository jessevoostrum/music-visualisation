import collections



CHORD_TYPES = collections.OrderedDict([
    ('major',                       ['1,3,5', ['', 'M', 'maj']]),                # Y
    ('minor',                       ['1,-3,5', ['-', 'm', 'min']]),                   # Y
    ('augmented',                   ['1,3,#5', ['\,{{}}^\\#\!5', '+', 'aug']]),                   # Y
    ('diminished',                  ['1,-3,-5', ['\mathrm{o}', 'dim', 'o']]),                  # Y
    # sevenths
    ('dominant-seventh',            ['1,3,5,-7', ['7', 'dom7',]]),           # Y: 'dominant'
    ('major-seventh',               ['1,3,5,7', ['\Delta 7', 'maj7', 'M7']]),            # Y
    ('minor-major-seventh',         ['1,-3,5,7', ['- \Delta 7', 'mM7', 'm#7', 'minmaj7']]),  # Y: 'major-minor'
    ('minor-seventh',               ['1,-3,5,-7', ['-7', 'm7', 'min7']]),          # Y
    ('augmented-major seventh',     ['1,3,#5,7', ['\Delta 7 \,{{}}^\\#\!5', '+M7', 'augmaj7']]),       # N
    ('augmented-seventh',           ['1,3,#5,-7', ['7\,{{}}^\\#\!5', '7+', '+7', 'aug7']]),    # Y
    ('half-diminished-seventh',     ['1,-3,-5,-7', ['\\varnothing7', '/o7', 'm7b5']]),        # Y: 'half-diminished'
    ('diminished-seventh',          ['1,-3,-5,--7', ['\mathrm{o}7', 'dim7']]),        # Y
    ('seventh-flat-five',           ['1,3,-5,-7', ['7\,{{}}^b5', 'dom7dim5']]),            # N
    # sixths
    ('major-sixth',                 ['1,3,5,6', ['6']]),                         # Y
    ('minor-sixth',                 ['1,-3,5,6', ['-6', 'm6', 'min6']]),               # Y
    # ninths
    ('major-ninth',                 ['1,3,5,7,9', ['\Delta 9', 'M9', 'Maj9']]),              # Y
    ('dominant-ninth',              ['1,3,5,-7,9', ['9', 'dom9']]),              # Y
    ('minor-major-ninth',           ['1,-3,5,7,9', ['-\Delta9', 'mM9', 'minmaj9']]),         # N
    ('minor-ninth',                 ['1,-3,5,-7,9', ['-9', 'm9', 'min9']]),            # N
    ('augmented-major-ninth',       ['1,3,#5,7,9', ['\Delta9\,{{}}^\\#\!5', '+M9', 'augmaj9']]),         # Y
    ('augmented-dominant-ninth',    ['1,3,#5,-7,9', ['9\,{{}}^\\#\!5', '+9', 'aug9']]),     # N
    ('half-diminished-ninth',       ['1,-3,-5,-7,9', ['\\varnothing 9', '/o9']]),                  # N
    ('half-diminished-minor-ninth', ['1,-3,-5,-7,-9', ['\\varnothing {{}}^b9', '/ob9']]),                # N
    ('diminished-ninth',            ['1,-3,-5,--7,9', ['\mathrm{o}9', 'dim9']]),          # N
    ('diminished-minor-ninth',      ['1,-3,-5,--7,-9', ['\mathrm{o}{{}}^b9', 'dimb9']]),       # N
    # elevenths
    ('dominant-11th',               ['1,3,5,-7,9,11', ['11', 'dom11']]),         # Y
    ('major-11th',                  ['1,3,5,7,9,11', ['\Delta 11', 'M11', 'Maj11']]),         # Y
    ('minor-major-11th',            ['1,-3,5,7,9,11', ['-\Delta 11', 'mM11', 'minmaj11']]),    # N
    ('minor-11th',                  ['1,-3,5,-7,9,11', ['-11', 'm11', 'min11']]),       # Y
    ('augmented-major-11th',        ['1,3,#5,7,9,11', ['\Delta11 \,{{}}^\\#\!5', '+M11', 'augmaj11']]),    # N
    ('augmented-11th',              ['1,3,#5,-7,9,11', ['11 \,{{}}^\\#\!5', '+11', 'aug11']]),       # N
    ('half-diminished-11th',        ['1,-3,-5,-7,-9,11', ['\\varnothing 11', '/o11']]),             # N
    ('diminished-11th',             ['1,-3,-5,--7,-9,-11', ['\mathrm{o}11', 'o11', 'dim11']]),   # N
    # thirteenths
    ('major-13th',                  ['1,3,5,7,9,11,13', ['\Delta 13', 'M13', 'Maj13']]),      # Y
    ('dominant-13th',               ['1,3,5,-7,9,11,13', ['13', 'dom13']]),      # Y
    ('minor-major-13th',            ['1,-3,5,7,9,11,13', ['-\Delta 13', 'mM13', 'minmaj13']]),  # N
    ('minor-13th',                  ['1,-3,5,-7,9,11,13', ['-13', 'm13', 'min13']]),    # Y
    ('augmented-major-13th',        ['1,3,#5,7,9,11,13', ['\Delta 13 \,{{}}^\\#\!5', '+M13', 'augmaj13']]),  # N
    ('augmented-dominant-13th',     ['1,3,#5,-7,9,11,13', ['13 \,{{}}^\\#\!5', '+13', 'aug13']]),    # N
    ('half-diminished-13th',        ['1,-3,-5,-7,9,11,13', ['\\varnothing 13', '/o13']]),           # N
    # other
    ('suspended-second',            ['1,2,5', ['\mathrm{sus}2','sus2']]),                        # Y
    ('suspended-fourth',            ['1,4,5', ['\mathrm{sus}4','sus', 'sus4']]),                 # Y
    ('suspended-fourth-seventh',    ['1,4,5,-7', ['7\mathrm{sus}4','7sus', '7sus4']]),            # Y
    ('Neapolitan',                  ['1,2-,3,5-', ['N6']]),                      # Y
    ('Italian',                     ['1,#4,-6', ['It+6', 'It']]),                # Y
    ('French',                      ['1,2,#4,-6', ['Fr+6', 'Fr']]),              # Y
    ('German',                      ['1,-3,#4,-6', ['Gr+6', 'Ger']]),            # Y
    ('pedal',                       ['1', ['pedal']]),                           # Y
    ('power',                       ['1,5', ['power']]),                         # Y
    ('Tristan',                     ['1,#4,#6,#9', ['tristan']]),                # Y
    ])

def getAbbreviationListGivenChordType(chordType):
    '''
    Get the Abbreviation list (all allowed Abbreviations that map to this
    :class:`music21.harmony.ChordSymbol` object):

    >>> harmony.getAbbreviationListGivenChordType('minor-major-13th')
    ['mM13', 'minmaj13']

    '''
    return CHORD_TYPES[chordType][1]

if __name__ == '__main__':

    import numpy as np

    import matplotlib.pyplot as plt
    from matplotlib import rc

    rc('text.latex', preamble=r'\usepackage{amssymb}')

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.sans-serif": ['Computer Modern Sans serif']
        # "font.sans-serif": ['Helvetica']

    })


    fig, ax = plt.subplots(figsize=(10,10))

    ax.axis("off")
    ax.set_xlim(0, 1.2)

    nx, ny = (5, 10)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    xv, yv = np.meshgrid(x, y)
    xv = xv.flatten()
    yv = yv.flatten()[::-1]

    for i, type in enumerate(CHORD_TYPES.values()):
        chord = '$3^{' + type[1][0] + '}$'
        # chord = 'a'
        ax.text(xv[i], yv[i], chord, fontsize=30)

    fig.savefig('../../output/chords2.pdf')