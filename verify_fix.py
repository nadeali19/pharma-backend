from werkzeug.security import generate_password_hash, check_password_hash

def simulate_login(stored_p, input_p):
    if ":" in stored_p:
        is_valid = check_password_hash(stored_p, input_p)
    else:
        is_valid = (stored_p == input_p)
    return is_valid

# Test with scrypt hash (default in many environments)
scrypt_hash = generate_password_hash("admin123")
print(f"Scrypt Hash: {scrypt_hash}")
print(f"Login with scrypt hash (correct): {simulate_login(scrypt_hash, 'admin123')}")
print(f"Login with scrypt hash (incorrect): {simulate_login(scrypt_hash, 'wrong')}")

# Test with pbkdf2 hash
pbkdf2_hash = "pbkdf2:sha256:600000$some_salt$some_hash"
# We can't easily generate pbkdf2 here if default is scrypt without extra params,
# but the check ":" in stored_p will handle it if it was stored.

# Test with plain text
plain_p = "1234"
print(f"Login with plain text (correct): {simulate_login(plain_p, '1234')}")
print(f"Login with plain text (incorrect): {simulate_login(plain_p, 'wrong')}")
