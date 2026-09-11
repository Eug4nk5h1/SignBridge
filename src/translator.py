def translate_to_asl(analysis):
    """
    Convert the structured NLP analysis into
    an ASL-oriented sign sequence.
    """

    sentence_type = analysis["sentence_type"]
    question_type = analysis["question_type"]

    subject = analysis["subject"]
    verb = analysis["verb"]
    object_ = analysis["object"]
    location = analysis["location"]
    time = analysis["time"]

    signs = []

    # ----------------------------------------
    # WH-QUESTIONS
    # ----------------------------------------

    if sentence_type == "QUESTION":

        # Put the WH-question concept first
        if question_type:
            signs.append(question_type)

        if subject:
            signs.append(subject)

        if object_:
            signs.append(object_)

        if location:
            signs.append(location)

        if time:
            signs.append(time)

        if verb:
            signs.append(verb)

        return signs

    # ----------------------------------------
    # STATEMENTS
    # ----------------------------------------

    # Time information first when available
    if time:
        signs.append(time)

    # Subject
    if subject:
        signs.append(subject)

    # Object
    if object_:
        signs.append(object_)

    # Location
    if location:
        signs.append(location)

    # Main action
    if verb:
        signs.append(verb)

    return signs