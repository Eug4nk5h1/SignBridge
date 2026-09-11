from src.sign_library import get_sign


words = ["I", "YOU", "GO", "WHERE", "COLLEGE", "BOOK"]

for word in words:

    sign = get_sign(word)

    print(f"{word} → {sign}")