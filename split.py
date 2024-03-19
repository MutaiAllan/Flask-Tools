import os
import random
import string
import time

def generate_new_filename(filename):
    """
    Generate a new filename with timestamp and random string
    """
    timestamp = int(time.time())
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    name, extension = os.path.splitext(filename)
    return f"{name}_{timestamp}_{random_string}{extension}"

new_filename = generate_new_filename("filename.png")
print(new_filename)