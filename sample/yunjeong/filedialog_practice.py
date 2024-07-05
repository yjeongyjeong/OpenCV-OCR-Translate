import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt the user to select a directory
selected_directory = filedialog.askdirectory()

# Print the selected directory (you can use it as needed)
print("Selected directory:", selected_directory)

if selected_directory:
    # User selected a directory
    print("Selected directory:", selected_directory)
else:
    # User canceled the dialog
    print("Directory selection canceled.")
