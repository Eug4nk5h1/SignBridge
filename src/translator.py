def translate_to_asl(analysis):
    """
    Convert NLP analysis into an ASL-oriented sign sequence.
    """

    # Get the meaningful words identified by NLP
    keywords = analysis["keywords"]

    # Convert everything to uppercase
    signs = [word.upper() for word in keywords]

    return signs