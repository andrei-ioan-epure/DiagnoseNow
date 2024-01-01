IPOTEZE = {'C', 'F', 'M', 'C19', 'N'}

REGULI = {
    'Febra': [
        (frozenset({'C', 'F'}), 0.5),
        (frozenset({'M'}), 0.2)
    ],
    'Greturi': [
        (frozenset({'C', 'F', 'N'}), 0.7)
    ],
    'Tuse': [
        (frozenset({'C'}), 0.4),
        (frozenset({'F', 'M'}), 0.3),
        (frozenset({'N'}), 0.1),
        (frozenset({'C', 'F', 'N'}), 0.2)
    ],
    'Dureri de cap': [
        (frozenset({'M'}), 0.5),
        (frozenset({'C', 'F', 'N'}), 0.3),
        (frozenset({'C', 'F', 'M'}), 0.2)
    ],
}

DENUMIRI = {
    'C': 'raceala',
    'F': 'gripa',
    'M': 'meningita',
    'C19': 'COVID-19',
    'N': 'nimic',
}