# Import libraries
import Material
import Element
import Property
from write_salt_script import create_salt_script
import Node
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def ask_file_path():
    """Open a file dialog to ask the user for a file path."""

    # Hide the main tkinter window
    Tk().withdraw()

    # Open file browser and get file path
    file_path = askopenfilename(
        title="Select a file",
        filetypes=[("Input Files", "*.inp"), ("All Files", "*.*")]
    )

    if not file_path:
        raise FileNotFoundError("No file selected")
    else:
        return file_path
    
def ask_folder_path():
    """Open a folder dialog to ask the user for a folder path."""

    # Hide the main tkinter window
    Tk().withdraw()

    # Open folder browser and get folder path
    folder_path = askdirectory(
        title="Select a folder"
    )

    if not folder_path:
        raise FileNotFoundError("No folder selected")
    else:
        return folder_path

# Ask user for input file path
file_path = ask_file_path()

# Ask user for output SALT file path
output_folder = ask_folder_path()
output_file = output_folder + "/runme.salt"

# Extract nodes, elements, materials, and properties from the file
nodes_list = Node.Node.read_nodes(file_path)
elements_list = Element.Element.read_elements(file_path, nodes_list)
materials_list = Material.Material.read_materials(file_path)
properties_list = Property.Property.read_properties(file_path, materials_list, elements_list)

# Write to SALT file
create_salt_script(output_file, properties_list)
