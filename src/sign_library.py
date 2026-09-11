import os

# Project root directory resolved relative to this module file
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ISL Sign Library mapping 40 ISL vocabulary words to project-relative video paths
SIGN_LIBRARY = {
    "BROTHER": "dataset/isl_40words/brother/brother.mp4",
    "COME": "dataset/isl_40words/come/come.mp4",
    "COMING": "dataset/isl_40words/come/come.mp4",
    "DRINK": "dataset/isl_40words/drink/drink.mp4",
    "DRINKING": "dataset/isl_40words/drink/drink.mp4",
    "EAT": "dataset/isl_40words/eat/eat.mp4",
    "EATING": "dataset/isl_40words/eat/eat.mp4",
    "FATHER": "dataset/isl_40words/father/father.mp4",
    "FOOD": "dataset/isl_40words/food/food.mp4",
    "FRIEND": "dataset/isl_40words/friend/friend.mp4",
    "GO": "dataset/isl_40words/go/go.mp4",
    "GOING": "dataset/isl_40words/go/go.mp4",
    "GOODBYE": "dataset/isl_40words/goodbye/goodbye.mp4",
    "HE": "dataset/isl_40words/he/he.mp4",
    "HELLO": "dataset/isl_40words/hello/hello.mp4",
    "HELP": "dataset/isl_40words/help/help.mp4",
    "HELPING": "dataset/isl_40words/help/help.mp4",
    "HOME": "dataset/isl_40words/home/home.mp4",
    "HOSPITAL": "dataset/isl_40words/hospital/hospital.mp4",
    "MARKET": "dataset/isl_40words/market/market.mp4",
    "ME": "dataset/isl_40words/me/me.mp4",
    "I": "dataset/isl_40words/me/me.mp4",
    "MOTHER": "dataset/isl_40words/mother/mother.mp4",
    "NO": "dataset/isl_40words/no/no.mp4",
    "OKAY": "dataset/isl_40words/okay/okay.mp4",
    "PLEASE": "dataset/isl_40words/please/please.mp4",
    "READ": "dataset/isl_40words/read/read.mp4",
    "READING": "dataset/isl_40words/read/read.mp4",
    "SCHOOL": "dataset/isl_40words/school/school.mp4",
    "COLLEGE": "dataset/isl_40words/school/school.mp4",
    "SHE": "dataset/isl_40words/she/she.mp4",
    "SISTER": "dataset/isl_40words/sister/sister.mp4",
    "SIT": "dataset/isl_40words/sit/sit.mp4",
    "SITTING": "dataset/isl_40words/sit/sit.mp4",
    "SORRY": "dataset/isl_40words/sorry/sorry.mp4",
    "STAND": "dataset/isl_40words/stand/stand.mp4",
    "STANDING": "dataset/isl_40words/stand/stand.mp4",
    "STOP": "dataset/isl_40words/stop/stop.mp4",
    "STOPPING": "dataset/isl_40words/stop/stop.mp4",
    "STUDENT": "dataset/isl_40words/student/student.mp4",
    "TEA": "dataset/isl_40words/tea/tea.mp4",
    "TEACHER": "dataset/isl_40words/teacher/teacher.mp4",
    "THANK_YOU": "dataset/isl_40words/thank_you/thank_you.mp4",
    "THANK YOU": "dataset/isl_40words/thank_you/thank_you.mp4",
    "TODAY": "dataset/isl_40words/today/today.mp4",
    "WATER": "dataset/isl_40words/water/water.mp4",
    "WHAT": "dataset/isl_40words/what/what.mp4",
    "WHEN": "dataset/isl_40words/when/when.mp4",
    "WHERE": "dataset/isl_40words/where/where.mp4",
    "WRITE": "dataset/isl_40words/write/write.mp4",
    "WRITING": "dataset/isl_40words/write/write.mp4",
    "YES": "dataset/isl_40words/yes/yes.mp4",
    "YOU": "dataset/isl_40words/you/you.mp4"
}


def get_sign(sign_word):
    """
    Returns project-relative video path for the given sign word, or None if not found.
    """
    key = str(sign_word).upper().replace("-", "_").strip()
    return SIGN_LIBRARY.get(key)


def get_absolute_sign_path(sign_word):
    """
    Resolves the absolute file path on the local system relative to PROJECT_ROOT.
    """
    rel_path = get_sign(sign_word)
    if rel_path:
        return os.path.normpath(os.path.join(PROJECT_ROOT, rel_path))
    return None