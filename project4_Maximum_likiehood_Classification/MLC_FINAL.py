# Author: James Cabrera
# Maximum Likelihood Classification with Region Growing

import numpy as np 
import sys
import math
import random

# Check for GDAL installation
try:
    import gdal
    print("module 'gdal' is installed")
    import gdalconst
except ModuleNotFoundError:
    print("module 'gdal' is not installed")
    exit()

# Check for NumPy installation
try:
    import numpy
    print("module 'numpy' is installed")
except ModuleNotFoundError:
    print("module 'numpy' is not installed")
    exit()

# Input and Output File Paths
# Replace 'your_path' with the actual path to the raster image
imgFName = r"your_path/tm_860516.img"  # Input raster file
outFName = imgFName.split(".")[0] + "_FINALPROJ_Grow_5.img"  # Output raster file with a modified name

# Register GDAL drivers
gdal.AllRegister()

# Open the input raster file
rasterIn = gdal.Open(imgFName, gdalconst.GA_ReadOnly)
if rasterIn is None:
    print("Cannot access the input file!\n")
    sys.exit(0)

# Extract raster metadata
projectionfrom = rasterIn.GetProjection()  # Get the spatial reference system
geotransform = rasterIn.GetGeoTransform()  # Get georeferencing information
numCols = rasterIn.RasterXSize             # Number of columns (pixels wide)
numRows = rasterIn.RasterYSize             # Number of rows (pixels tall)
bands = rasterIn.RasterCount               # Number of spectral bands in the image

# Load the raster data into a 3D NumPy array
# Shape: [numRows, numCols, bands]
imgData = np.zeros((numRows, numCols, bands), dtype=np.float32)
for iband in range(bands):
    band = rasterIn.GetRasterBand(iband + 1)  # GDAL uses 1-based indexing for bands
    imgData[:, :, iband] = band.ReadAsArray(0, 0, numCols, numRows)

# Function to calculate spectral distance between two pixels
def specDist(p1, p2, num):
    """
    Compute the Euclidean distance between two pixels in spectral space.
    p1, p2: Pixel values (arrays) from different bands
    num: Number of bands
    """
    return math.sqrt(sum((p1[iband] - p2[iband]) ** 2 for iband in range(num)))

# Function to calculate log probability based on the multivariate Gaussian distribution
def Log_P(cp, mu, cov):
    """
    Compute the log-probability of a pixel belonging to a class.
    cp: Current pixel (array of band values)
    mu: Mean vector of the class
    cov: Covariance matrix of the class
    """
    det = np.linalg.det(cov)  # Determinant of the covariance matrix
    inv = np.linalg.inv(cov)  # Inverse of the covariance matrix
    # Probability computation based on Gaussian distribution
    P = (-0.5 * np.log(det) - (np.matmul(np.matmul(inv, (cp - mu)), (cp - mu).transpose())) / 2)
    return P

# List of user-defined seed points (row, column) for different land cover classes
Spixels = [[500, 800], [23, 609], [100, 200], [128, 373], [233, 342]]  # Example: water, urban, forest, vegetation

# Neighborhood offsets for region growing (8 neighbors: diagonal and cardinal directions)
NBs = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

# Function for region growing
def SeedGrow(imgData, SeedRow, SeedCol, threshold):
    """
    Perform region growing starting from a seed point.
    imgData: Input raster data
    SeedRow, SeedCol: Row and column of the seed point
    threshold: Spectral distance threshold for including neighboring pixels
    """
    checkd = np.zeros((numRows, numCols), dtype=np.uint8)  # Keep track of visited pixels
    N2chck = [[SeedRow, SeedCol]]  # Initialize the list of pixels to check
    Pixels = []  # List to store all pixels in the grown region

    while len(N2chck) > 0:
        cp = N2chck.pop()  # Get the current pixel to process
        crow, ccol = cp
        for iNB in NBs:
            NBrow = crow + iNB[0]
            NBcol = ccol + iNB[1]
            # Skip if neighbor is out of bounds or already checked
            if NBrow < 0 or NBrow >= numRows or NBcol < 0 or NBcol >= numCols:
                continue
            if checkd[NBrow, NBcol] == 1:
                continue
            # Calculate spectral distance between seed and neighbor
            SD = specDist(imgData[SeedRow, SeedCol, :], imgData[NBrow, NBcol, :], bands)
            checkd[NBrow, NBcol] = 1  # Mark as checked
            # If within the threshold, add the neighbor to the region
            if SD < threshold:
                Pixels.append(imgData[NBrow, NBcol, :])  # Add to region pixels
                N2chck.append([NBrow, NBcol])  # Add to the list of pixels to check

    # Compute mean and covariance matrix for the grown region
    Mat = np.array(Pixels)  # Convert region pixels to NumPy array
    local_mu = Mat.mean(0)  # Mean vector
    dif = Mat - local_mu    # Subtract mean from each pixel
    trans = np.transpose(dif)
    local_Cov = np.matmul(trans, dif) / (len(Pixels) - 1)  # Covariance matrix
    return local_Cov, local_mu

# Initialize arrays to store covariance matrices and mean vectors for each seed
numseeds = len(Spixels)
all_Covs = np.zeros((bands, bands, numseeds), dtype=np.float64)  # Covariance matrices
all_mu = np.zeros((numseeds, bands), dtype=np.float64)  # Mean vectors

# Perform region growing for each seed point
for idx, s in enumerate(Spixels):
    Cov, Mu = SeedGrow(imgData, s[0], s[1], 20)  # Threshold is 20
    all_Covs[:, :, idx] = Cov  # Store covariance matrix
    all_mu[idx, :] = Mu        # Store mean vector

# Initialize output image for classification
outImg = np.zeros((numRows, numCols), dtype=np.uint8)

# Classify each pixel using Maximum Likelihood Classification
for irow in range(numRows):
    for icol in range(numCols):
        cp = imgData[irow, icol, :]  # Current pixel
        max_P = Log_P(cp, all_mu[0, :], all_Covs[:, :, 0])  # Compute log-probability for the first class
        tmpCls = 0  # Initialize class label
        for iseed in range(1, numseeds):
            tmp_P = Log_P(cp, all_mu[iseed, :], all_Covs[:, :, iseed])  # Log-probability for other classes
            if max_P < tmp_P:  # If a higher probability is found
                max_P = tmp_P
                tmpCls = iseed  # Update class label
        outImg[irow, icol] = tmpCls  # Assign class label to the output image

# Save the classified image to a new raster file
rasterOut = gdal.GetDriverByName("HFA").Create(outFName, numCols, numRows, 1, gdal.GDT_Byte)
rasterOut.SetProjection(projectionfrom)  # Set spatial reference
rasterOut.SetGeoTransform(geotransform)  # Set georeferencing information
rasterOut.GetRasterBand(1).WriteArray(outImg)  # Write classification result
rasterIn = None
rasterOut = None

print("Classification Done!")
