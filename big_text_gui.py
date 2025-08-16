"""
Big Text GUI for Early Learners
------------------------------
This script creates a simple window with very large text and a big button for easy interaction.
Requires: tkinter (built-in with Python)
"""

import tkinter as tk

class BigTextApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learning App - Big Text Mode")
        self.configure(bg='#E6F7FF')
        self.geometry('800x400')

        self.label = tk.Label(self, text="WELCOME!", font=("Arial", 64, "bold"), fg="#005A9C", bg='#E6F7FF')
        self.label.pack(pady=40)

        self.button = tk.Button(self, text="NEXT", font=("Arial", 36, "bold"), bg="#FFD966", fg="#005A9C", command=self.on_next, height=2, width=10)
        self.button.pack(pady=30)

    def on_next(self):
        self.label.config(text="LET'S LEARN!")
        self.button.config(text="EXIT", command=self.destroy)

if __name__ == "__main__":
    app = BigTextApp()
    app.mainloop()