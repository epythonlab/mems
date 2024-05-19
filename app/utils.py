# utils.py

import random
import string

def generate_random_password(length=12):
    # Define the characters to use for generating the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate the random password
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password
