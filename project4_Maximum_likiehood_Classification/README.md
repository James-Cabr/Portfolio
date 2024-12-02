Maximum Likelihood Classification with Region Growing
This Python script implements a Maximum Likelihood Classification (MLC) algorithm combined with region growing for multispectral raster imagery. It is designed for remote sensing applications to classify different land cover types based on user-defined seed points.

Features
Region Growing:
Expands regions based on spectral similarity using a specified threshold.
Maximum Likelihood Classification:
Classifies each pixel based on the probability of belonging to a predefined class (seed regions).
Statistical Analysis:
Computes mean vectors and covariance matrices for each class during region growing.
How it Works
Input:
A multispectral raster file is read into memory.
Seed Points:
User-defined points (Spixels) representing different classes (e.g., water, urban, forest) are used for region growing.
Region Growing:
Expands regions around the seed points using a spectral distance threshold.
Maximum Likelihood Classification:
Each pixel is classified into the class with the highest likelihood based on covariance and mean statistics.
Output:
A classified raster file is generated.
Requirements
Python 3.x
Libraries:
gdal
numpy
math
Input Parameters
Spixels: List of seed points for classification (coordinates in row, column format).
threshold: Spectral distance threshold for region growing.
bands: Number of spectral bands in the input raster.
Output
A classified raster image with each pixel labeled as a specific class based on the maximum likelihood probability.
Disclaimer
Ensure the input raster file is properly preprocessed (e.g., georeferenced, no missing values) before using this script.
Replace confidential or sensitive paths (e.g., C:\Users\...) with generic placeholders if sharing the script.
