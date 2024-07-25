# CloudScanner

## Description

CloudScanner is a Python tool designed to extract inventory data from Google Cloud Platform (GCP) and generate reports in various formats, including Migration Portfolio Assessment (MPA) compatible spreadsheets.

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Cloud SDK installed and configured

### Virtual Environment Setup

1. **Create a virtual environment:**

```bash
python3 -m venv venv
```

### Activate the virtual environment:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Usage
To run the program, analyze the file main.py. For example, you can call the tool like this:

```bash
./venv/bin/python src/index.py --project sites-web-273920 --output_format mpa
```
### Arguments:

* --project: Your GCP project ID.
* --output_format: The desired output format. Currently supported formats:
    * mpa: Generates an MPA-compatible spreadsheet.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
