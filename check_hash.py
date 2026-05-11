from werkzeug.security import generate_password_hash, check_password_hash
h = generate_password_hash('admin123')
print(f'Hash: {h}')
print(f'Starts with pbkdf2:sha256: {h.startswith("pbkdf2:sha256")}')
print(f'Check: {check_password_hash(h, "admin123")}')
