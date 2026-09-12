# Common phrase variations
PHRASE_NORMALIZATIONS = {
    ("GOOD", "BYE"): "GOODBYE",
}


def translate_to_asl(analysis):
    """
    Convert NLP analysis into an ASL-oriented sign sequence.
    """

    keywords = analysis["keywords"]

    signs = []
    i = 0

    while i < len(keywords):

        # Check whether the current word and next word
        # form a known phrase
        if i + 1 < len(keywords):

            pair = (
                keywords[i].upper(),
                keywords[i + 1].upper()
            )

            if pair in PHRASE_NORMALIZATIONS:
                signs.append(PHRASE_NORMALIZATIONS[pair])
                i += 2
                continue

        # Otherwise keep the individual word
        signs.append(keywords[i].upper())
        i += 1

    return signs