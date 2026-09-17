# FEMAP to RTMWorx Converter

A Python tool to convert FEMAP Abaqus input files (`.inp`) to RTMWorx SALT scripts for composite resin transfer molding simulations.

## Overview

This converter reads FEMAP-generated Abaqus input files containing composite layup definitions and converts them into RTMWorx SALT script format for flow simulation analysis.

## Features

- **Parse Abaqus Input Files**: Extracts nodes, elements, materials, and composite layup properties
- **Material Properties**: Reads fiber volume fraction (Vf), permeability (K11, K22)
- **Composite Layups**: Processes shell sections with ply definitions (thickness, angle, material)
- **Element Sets**: Maintains element set associations for proper ply assignments
- **Interactive File Selection**: GUI dialogs for file and folder selection
- **SALT Script Generation**: Outputs ready-to-use RTMWorx SALT scripts

## Project Structure

```
femap-rtmworx/
├── main.py              # Main entry point with file dialogs
├── Node.py              # Node class and reader
├── Element.py           # Element class and reader
├── Material.py          # Material class and reader
├── Property.py          # Property class with layup definitions
├── Ply.py               # Ply class for individual layers
├── write_salt_script.py # SALT script generator
├── Runner.py            # Runner utilities
├── requirements.txt     # Python dependency declaration
└── README.md
```

## Requirements

- Python 3.6+
- tkinter, including the Tk GUI components

This project has no third-party Python dependencies. The `requirements.txt` file is
provided for standard Python project setup, but does not currently install any
packages. On some Linux distributions, tkinter must be installed separately through
the operating system package manager.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AhaanBhosale/femap-rtmworx.git
cd femap-rtmworx
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Select your FEMAP Abaqus input file (`.inp`) when prompted

3. Select the output folder for the generated SALT script

4. The tool will generate `runme.salt` in the selected folder. The generated SALT
	script opens `runme.wrx` and saves the resulting model as `Test.wrx`, so those
	filenames must match the files available to RTMWorx.

## Input File Format

The converter expects Abaqus input files with the following sections:

- `*NODE` - Node coordinates
- `*ELEMENT` - Element connectivity with ELSET definitions
- `*MATERIAL` - A material whose next section line contains `LAMINA`, followed by
	a numeric property line containing at least four comma-separated values. The
	parser reads K11 from the first value, K22 from the second, and Vf from the
	fourth value.
- `*SHELL SECTION` - Composite layup definitions
- `*BEAM SECTION` - Runner definitions; the following line supplies the runner
	radius, which the converter doubles to obtain the diameter

### Example Input:
```
*NODE
1, 0.0, 0.0, 0.0
2, 1.0, 0.0, 0.0

*ELEMENT, TYPE=S3, ELSET=P1
1, 1, 2, 3

*MATERIAL, NAME=CARBON_FIBER
*LAMINA
1.2e-10, 8.5e-11, 0.0, 0.6

*SHELL SECTION, ELSET=P1, COMPOSITE
0.25, , CARBON_FIBER, 0.0
0.25, , CARBON_FIBER, 45.0
```

## Classes

### Node
- Stores X, Y, Z coordinates
- Reads node definitions from input file

### Element
- Contains node connectivity and element set name
- Extracts ELSET information from element definitions

### Material
- Stores material name and RTM properties (Vf, K11, K22)
- Parses material sections from input file

### Property
- Groups elements by ELSET
- Contains multiple Ply objects for layup definition

### Ply
- Individual ply layer with thickness, angle, and material
- Associated with an element set through its containing Property

### Runner
- Reads beam sections and associates their elements with a runner
- Writes circular runner geometry and diameter information to the SALT script

## Development

### Setting Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies (there are currently no third-party packages)
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Authors

- Ahaan Bhosale

## Acknowledgments

- FEMAP for FEA preprocessing
- RTMWorx for composite flow simulation
