#!/usr/bin/env python
from __future__ import division
import math
import tkinter as tk
from tkinter import ttk
import re
import random
import pyperclip

# Initialize policies dictionary
policies = {'Uppercase characters': 0,
            'Lowercase characters': 0,
            'Special characters': 0,
            'Numbers': 0}

entropies = {'Uppercase characters': 26,
             'Lowercase characters': 26,
             'Special characters': 33,
             'Numbers': 15}

def calculate_combinations(password_length, char_set_size):
    return math.pow(char_set_size, password_length)

def classify_strength(entropy, pass_len):
    if entropy < 50 or pass_len < 8:
        return "Very Weak"
    elif 50 <= entropy < 70 or 8 <= pass_len < 10:
        return "Weak"
    elif 70 <= entropy < 90 or 10 <= pass_len < 12:
        return "Moderate"
    elif 90 <= entropy < 120 or 12 <= pass_len < 14:
        return "Strong"
    elif entropy >= 120 and pass_len >= 14:
        return "Very Strong"
    else:
        return "Indestructible"

def generate_strong_password():
    char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=[]{}|;:,.<>?`~"
    password_length = len(password_entry.get())
    strong_password = ''.join(random.choice(char_set) for _ in range(password_length + 4))
    suggested_label.config(text=f"Suggested Strong Password: {strong_password}")

def generate_new_password():
    original_password = password_entry.get()
    new_password = ''.join(original_password[i] + random.choice("0123456789!@#$%^&*()_-+=[]{}|;:,.<>?`~") for i in range(len(original_password)))
    new_password_label.config(text=f"Generated New Password: {new_password}")
    copy_button.config(state="normal")  # Enable the copy button

def copy_to_clipboard():
    generated_password = new_password_label.cget("text").split(": ")[1]
    pyperclip.copy(generated_password)

def evaluate_password():
    # Reset counts and entropy to zero before evaluating the new password
    for key in policies:
        policies[key] = 0
    entropy = 0

    crack_speed = 20000  # Default

    password = password_entry.get()
    pass_len = len(password)

    for char in password:
        if re.match("[0-9]", char):
            policies["Numbers"] += 1
        elif re.match("[a-z]", char):
            policies["Lowercase characters"] += 1
        elif re.match("[A-Z]", char):
            policies["Uppercase characters"] += 1
        else:
            policies["Special characters"] += 1

    for policy in policies.keys():
        num = policies[policy] if policies[policy] > 0 else '-'
        result_label.config(text=f"{policy}: {num}")

        if policies[policy] > 0:
            entropy += entropies[policy]

    password_length_label.config(text=f"Password length: {pass_len}")
    entropy_label.config(text=f"Password entropy: {entropy}")

    char_set_size = sum(policies.values())
    total_combinations = calculate_combinations(pass_len, char_set_size)

    # Calculate time to crack based on combinations
    cracked = total_combinations / crack_speed  # in seconds

    time_ = "seconds"
    if cracked > 60:
        cracked = cracked / 60
        time_ = "minutes"

    if cracked > 60:
        cracked = cracked / 60
        time_ = "hours"

    if cracked > 24:
        cracked = cracked / 24
        time_ = "days"

    if cracked > 365:
        cracked = cracked / 365
        time_ = "years"

    time_label.config(text=f"Time to crack password: {cracked:.2f} {time_}")

    # Classify password strength based on both entropy and password length
    strength = classify_strength(entropy, pass_len)
    strength_label.config(text=f"Password Strength: {strength}")

    # Disable the copy button initially
    copy_button.config(state="disabled")

    # Clear the password entry after evaluation
    password_entry.delete(0, 'end')

# GUI setup
root = tk.Tk()
root.title("Password Strength Evaluator")

# Password Entry
password_label = ttk.Label(root, text="Enter Password:")
password_label.pack(pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=5)

# Evaluate Button
evaluate_button = ttk.Button(root, text="Evaluate", command=evaluate_password)
evaluate_button.pack(pady=10)

# Generate Strong Password Button
generate_button = ttk.Button(root, text="Generate Strong Password", command=generate_strong_password)
generate_button.pack(pady=10)

# Generate New Password Button
generate_new_button = ttk.Button(root, text="Generate New Password", command=generate_new_password)
generate_new_button.pack(pady=10)

# Copy to Clipboard Button
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, state="disabled")
copy_button.pack(pady=10)

# Result Labels
password_length_label = ttk.Label(root, text="")
password_length_label.pack(pady=5)

result_label = ttk.Label(root, text="")
result_label.pack(pady=5)

entropy_label = ttk.Label(root, text="")
entropy_label.pack(pady=5)

time_label = ttk.Label(root, text="")
time_label.pack(pady=5)

# New label for password strength classification
strength_label = ttk.Label(root, text="")
strength_label.pack(pady=5)

# New label for suggested strong password
suggested_label = ttk.Label(root, text="")
suggested_label.pack(pady=5)

# New label for generated new password
new_password_label = ttk.Label(root, text="")
new_password_label.pack(pady=5)

root.mainloop()
