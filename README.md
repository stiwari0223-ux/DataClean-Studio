# DataClean Studio — Streamlit Data Cleaning App

An interactive application for exploring and cleaning CSV and Excel datasets.

## Features
- Upload CSV, XLSX, and XLS files
- Preview data, inspect data types, missing values, unique values, and descriptive statistics
- Handle missing values using drop, mean, median, mode, or a custom value
- Remove duplicate rows
- Rename and delete columns
- Convert columns to string, integer, float, or datetime
- Detect and remove numeric outliers using the IQR method
- Visualize numeric columns and missing values
- Export cleaned data to CSV or Excel
- Reset the working dataset to the original upload

## Setup

Python 3.10 or newer is recommended.

```bash
# Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## Project structure

```text
dataclean_streamlit/
├── app.py
├── requirements.txt
└── README.md
```

## Notes
- The uploaded original is not modified; cleaning operations affect an in-session working copy.
- Download a backup before applying destructive operations.
- Excel support uses openpyxl.
- IQR outlier detection is a statistical heuristic; review flagged rows before removing them.
