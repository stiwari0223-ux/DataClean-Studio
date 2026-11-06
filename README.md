
# DataClean Studio

An interactive web-based data cleaning and preprocessing application built using Python, Streamlit, Pandas, NumPy, and Plotly.

Clean, analyze, visualize, and transform datasets through a simple and intuitive interface without writing complex code.

## Live Demo

**Try the application here:**

[Launch DataClean Studio](https://dataclean-studio-stream.streamlit.app/)

## Overview

DataClean Studio is designed to simplify the data preprocessing workflow. It provides an interactive environment where users can upload datasets, identify data quality issues, apply cleaning operations, visualize patterns, and download processed datasets.

Whether you are a student, data analyst, or beginner in machine learning, DataClean Studio helps make data preparation easier and faster.

## Features

### 1. Dataset Upload
- Upload CSV files.
- Upload Excel files (XLS and XLSX).
- Preview uploaded datasets.

### 2. Data Exploration
- View dataset dimensions (rows and columns).
- Check missing values.
- Identify duplicate records.
- Explore column information.
- Generate descriptive statistics.

### 3. Data Cleaning
- Handle missing values using mean, median, mode, or custom values.
- Remove rows containing missing values.
- Detect and remove duplicate records.
- Rename columns.
- Delete unnecessary columns.
- Convert column data types.

### 4. Outlier Detection
- Detect outliers using the IQR method.
- Visualize outliers using box plots.
- Remove detected outliers.

### 5. Data Visualization
- Histograms.
- Box plots.
- Line charts.
- Missing-value visualizations.

### 6. Export and History
- Download cleaned datasets as CSV.
- Export cleaned datasets as Excel.
- Track cleaning operations through cleaning history.
- Reset the dataset to its original state.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Plotly | Interactive data visualization |
| OpenPyXL | Excel file processing |

## Project Structure

```text
DataClean-Studio/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── student_performance.csv
```

## Installation and Setup

Follow these steps to run DataClean Studio locally.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/DataClean-Studio.git
```

### 2. Navigate to the Project Directory

```bash
cd DataClean-Studio
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```powershell
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## Sample Dataset

A sample Student Performance Dataset is included in this repository:

`student_performance.csv`

You can use it to test the application's data cleaning, preprocessing, and visualization features.

## Use Cases

- Data preprocessing for machine learning.
- Exploratory data analysis (EDA).
- Handling missing and duplicate values.
- Dataset quality assessment.
- Learning practical data cleaning workflows.

## Future Improvements

- Automated data quality reports.
- Additional outlier detection techniques.
- More visualization options.
- Machine learning-based data cleaning suggestions.
- Support for additional file formats.
- Automated preprocessing pipelines.

## Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## Author

**Sudhanshu Tiwari**

B.Tech Computer Science and Engineering

## License

This project is open-source and available under the MIT License.
