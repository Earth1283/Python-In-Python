import tkinter as tk
from tkinter import scrolledtext, simpledialog
import sys
import tempfile
import os
import subprocess
from io import StringIO

# Function to execute Python code from text box, handle input, and use temporary file
def run_python_code():
    code = code_input.get("1.0", tk.END)  # Get the input code from the text widget

    # Clear the output box before running the code
    output_box.delete("1.0", tk.END)

    # Create a temporary file to save the code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
        tmp_file.write(code.encode('utf-8'))
        tmp_file.close()  # Close the file to allow execution

        # Create a custom input function to handle user input
        def custom_input(prompt):
            # Popup input dialog to get user input
            return simpledialog.askstring("Input", prompt)

        # Redirect standard output and error to capture printed messages
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()  # Capture the output to display in the output box
        sys.stderr = StringIO()

        try:
            # Run the temporary Python file and capture output
            result = subprocess.run(
                [sys.executable, tmp_file.name],  # Use sys.executable for the Python interpreter
                text=True,                       # Capture text output
                input=None,                      # Default input, handled by custom_input
                capture_output=True             # Capture stdout and stderr
            )
            # Get the captured output from the result
            output = result.stdout + "\n" + result.stderr
            output_box.insert(tk.END, output)  # Display the output in the output box
        except Exception as e:
            output_box.insert(tk.END, f"Error: {e}\n")
        finally:
            # Restore the standard output and error
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Delete the temporary file after use
            os.remove(tmp_file.name)

# Create the main window
root = tk.Tk()
root.title("Python Code Executor")

# Create a Label
label = tk.Label(root, text="Enter Python code below:")
label.pack(pady=10)

# Create a ScrolledText widget for code input
code_input = scrolledtext.ScrolledText(root, width=50, height=10)
code_input.pack(padx=10, pady=10)

# Create a Button to run the code
run_button = tk.Button(root, text="Run Code", command=run_python_code)
run_button.pack(pady=10)

# Create a ScrolledText widget for output
output_label = tk.Label(root, text="Output:")
output_label.pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=50, height=10)
output_box.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
