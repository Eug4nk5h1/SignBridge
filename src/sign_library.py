from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Folder containing ASL sign videos
SIGNS_FOLDER = PROJECT_ROOT / "assets" / "signs"


def get_sign(sign_word):
    """
    Find the ASL video corresponding to a sign word.

    Example:
        HELLO -> assets/signs/hello.mp4
        COLLEGE -> assets/signs/college.mp4
    """

    if not sign_word:
        return None

    sign_word = str(sign_word).strip().lower()

    # Try common video extensions
    for extension in [".mp4", ".avi", ".mov", ".mkv"]:
        video_path = SIGNS_FOLDER / f"{sign_word}{extension}"

        if video_path.exists():
            return video_path

    return None


def get_absolute_sign_path(sign_word):
    """
    Return the absolute path of the ASL sign video.
    """

    sign_path = get_sign(sign_word)

    if sign_path is None:
        return None

    return sign_path.resolve()