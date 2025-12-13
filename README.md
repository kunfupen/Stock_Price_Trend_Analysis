# Stock Price Trend Analysis

## Overview
This project analyzes historical stock price data to identify trends and patterns. It utilizes various statistical methods and visualization techniques to help investors make informed decisions.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Data Collection](#data-collection)
    - [Data Cleaning](#data-cleaning)
    - [Data Analysis](#data-analysis)
    - [Data Visualization](#data-visualization)
- [Getting Data](#getting-data)
- [Cleaning Data](#cleaning-data)
- [Producing Analysis](#producing-analysis)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/kunfupen/Stock-Price-Trend-Analysis.git
cd Stock-Price-Trend-Analysis
```

2. To install the required libraries for this project, run the following command in your terminal:
```bash
pip install -r requirements.txt
```

## Usage

### Data Collection
The data collection is handled in the `src/get_data.py` file. This script includes functions for collecting data from various sources, such as web scraping, API calls, or reading from files.
```bash
python src/get_data.py
```

### Data Cleaning
Data cleaning is performed in the `src/clean_data.py` file. This script contains functions for preprocessing the collected data, including handling missing values, removing duplicates, and transforming data types.
```bash
python src/clean_data.py
```

### Data Analysis
The data analysis is performed in the `src/run_analysis.py` file. This script includes functions for performing statistical analysis, identifying trends, and generating insights from the cleaned data.
```bash
python src/run_analysis.py
```

### Data Visualization
Visualization of the analysis results are created in the `src/visualize_results.py` file. This script contains functions for generating various types of plots and charts to represent the data visually.
```bash
python src/visualize_results.py
```

### Getting Data
Raw data files should be placed in the `data/raw/` directory. The data collection script will handle the retrieval and storage of these files.

### Cleaning Data
After collecting the raw data, run the cleaning script to preprocess the data and store the cleaned files in the `data/processed/` directory.

### Producing Analysis
To perform the analysis, run the analysis script which will read the cleaned data and generate the analysis results, saving them in the `results/` directory.