def translate_to_asl(subject, action, destination):
    sign_sequence = []

    if subject:
        sign_sequence.append(subject.upper())

    if destination:
        sign_sequence.append(destination.upper())

    if action:
        sign_sequence.append(action.upper())

    return sign_sequence


# Test
subject = "I"
action = "going"
destination = "college"

result = translate_to_asl(subject, action, destination)

print("ASL Sign Sequence:")
print(" → ".join(result))