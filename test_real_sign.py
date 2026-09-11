from src.sign_library import get_sign


sign = get_sign("COLLEGE")

print("Sign file:")
print(sign)

print("\nDoes the file exist?")
print(sign.exists())