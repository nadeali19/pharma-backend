from werkzeug.security import check_password_hash
try:
    print(f'Check plain text: {check_password_hash("admin123", "admin123")}')
except Exception as e:
    print(f'Error: {e}')
