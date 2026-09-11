from src.sign_generator import retrieve_signs


sign_sequence = ["WHERE", "YOU", "GO"]

result = retrieve_signs(sign_sequence)

print("Sign sequence:")
print(" → ".join(sign_sequence))

print("\nRetrieved resources:")
print(result)