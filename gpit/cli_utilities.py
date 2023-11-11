import subprocess
import tempfile
import os

def edit_message_in_editor(message):
    """Open the message in a text editor (Nano) for editing."""
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False, mode='w+') as tf:
        tf_path = tf.name
        tf.write(message)
        tf.flush()

    editor = os.getenv('EDITOR', 'nano')  # Use Nano or the default editor set in the environment
    subprocess.call([editor, tf_path])

    with open(tf_path, "r") as tf:
        edited_message = tf.read()

    os.remove(tf_path)  # Clean up the temporary file
    return edited_message

def print_warnings(warnings):
    """Prints warnings in a formatted manner."""
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("\n✅ No warnings.")