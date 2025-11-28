import tkinter as tk
from gui import StudentConcernApp

if __name__ == "__main__":
    # Initialize the main window
    root = tk.Tk()
    
    # Initialize the application logic from the GUI module
    app = StudentConcernApp(root)
    
    # Start the application loop
    root.mainloop()