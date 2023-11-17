#!/usr/bin/env python
from __future__ import division
import math
import tkinter as tk
from tkinter import ttk
import re

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

def evaluate_password():
    # Reset counts and entropy to zero before evaluating the new password
    for key in policies:
        policies[key] = 0
    entropy = 0

    crack_speed = 20000000000  # Default

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

# Result Labels
password_length_label = ttk.Label(root, text="")
password_length_label.pack(pady=5)

result_label = ttk.Label(root, text="")
result_label.pack(pady=5)

entropy_label = ttk.Label(root, text="")
entropy_label.pack(pady=5)

time_label = ttk.Label(root, text="")
time_label.pack(pady=5)

root.mainloop()

