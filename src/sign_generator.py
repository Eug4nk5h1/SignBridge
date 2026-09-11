from src.sign_library import get_sign


def retrieve_signs(sign_sequence):
    retrieved_signs = []

    for sign in sign_sequence:
        resource = get_sign(sign)

        if resource:
            retrieved_signs.append(resource)
        else:
            retrieved_signs.append("SIGN_NOT_FOUND")

    return retrieved_signs