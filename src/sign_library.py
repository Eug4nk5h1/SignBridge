from pathlib import Path


SIGN_LIBRARY = {
    "COLLEGE": "college.mp4"
}


SIGNS_FOLDER = Path(__file__).parent.parent / "assets" / "signs"


def get_sign(sign_word):
    filename = SIGN_LIBRARY.get(sign_word.upper())

    if filename is None:
        return None

    return SIGNS_FOLDER / filename