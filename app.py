from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def validate_password(password):
    errors = []
    
    if len(password) <= 12:
        errors.append("Password must be more than 12 characters.")
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter.")
    if not any(char in '!@#$%^&*()-_=+[]{}|;:",.<>?/\\' for char in password):
        errors.append("Password must contain at least one special symbol.")
    
    return errors

def suggest_password(password):
    # Ensure password is more than 12 characters
    if len(password) <= 12:
        additional_length = 13 - len(password)
        password += ''.join(random.choices(string.ascii_letters + string.digits, k=additional_length))
    
    # Ensure at least one uppercase letter
    if not any(char.isupper() for char in password):
        password = replace_first(password, string.ascii_lowercase, string.ascii_uppercase)
    
    # Ensure at least one lowercase letter
    if not any(char.islower() for char in password):
        password = replace_first(password, string.ascii_uppercase, string.ascii_lowercase)
    
    # Ensure at least one special symbol
    if not any(char in '!@#$%^&*()-_=+[]{}|;:",.<>?/\\' for char in password):
        password += random.choice('!@#$%^&*()-_=+[]{}|;:",.<>?/\\')
    
    return password

def replace_first(password, from_chars, to_chars):
    password_list = list(password)
    for i, char in enumerate(password_list):
        if char in from_chars:
            password_list[i] = random.choice(to_chars)
            break
    return ''.join(password_list)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form.get('password')
        errors = validate_password(password)
        
        if errors:
            suggested_password = suggest_password(password)
            return render_template('index.html', errors=errors, password=password, suggested_password=suggested_password)
        else:
            return render_template('index.html', success=True, password=password)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
