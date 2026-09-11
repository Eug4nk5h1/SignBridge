def translate_to_asl(analysis):

    sentence_type = analysis["sentence_type"]
    question_type = analysis["question_type"]

    subject = analysis["subject"]
    verb = analysis["verb"]
    object_ = analysis["object"]
    location = analysis["location"]
    time = analysis["time"]

    signs = []

    # -------------------------
    # QUESTIONS
    # -------------------------

    if sentence_type == "QUESTION":

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

    # -------------------------
    # STATEMENTS
    # -------------------------

    if time:
        signs.append(time)

    if subject:
        signs.append(subject)

    if object_:
        signs.append(object_)

    if location:
        signs.append(location)

    if verb:
        signs.append(verb)

    return signs