This script processes data from multiple source layers and adds qualified features to the MSUP master feature class. It is designed to identify features based on specific criteria, such as hold reasons, district validity, and other attributes, to ensure only the appropriate data is included. Additionally, it performs updates to calculated fields like billing categories, vegetation clearing, and equipment used.

Features
Integration with Multiple Source Layers: Processes data from the following feature services:

AGOL
Arbora
Structure Brushing
Hazard Tree
Supplemental Patrols
Filtering Logic: Filters features based on:

On-Hold Reason fields.
Valid districts assigned to ERM.
Other attribute-based criteria.
Feature Insertion: Adds filtered features to the master feature class, ensuring no duplicates by comparing control numbers.

Automated Field Updates:

Billing Categories
Vegetation Clearing
Equipment Used
Access Routes
Backup Creation: Creates a backup of features removed from the master feature class in a geodatabase.

Prerequisites
ArcGIS Environment:

This script requires an environment where ArcPy is installed (e.g., ArcGIS Pro or ArcGIS Enterprise).
Python Packages:

arcpy
datetime
Access to Feature Services:

The script uses REST URLs for feature services. Ensure you have the appropriate permissions to access these services.
Usage
Clone or download the script.

Update the following placeholders in the script with actual values:

REPLACE_WITH_STRUCTURE_BRUSHING_FEATURE_SERVICE_URL
REPLACE_WITH_HAZ_TREE_FEATURE_SERVICE_URL
REPLACE_WITH_SUPPLEMENTAL_PATROLS_FEATURE_SERVICE_URL
REPLACE_WITH_AGOL_FEATURE_SERVICE_URL
REPLACE_WITH_ARBORA_FEATURE_SERVICE_URL
REPLACE_WITH_MASTER_FEATURE_SERVICE_URL
REPLACE_WITH_BACKUP_GDB_PATH
REPLACE_WITH_WORKSPACE_PATH
Run the script in an ArcGIS-compatible Python environment.

Script Workflow
Feature Filtering:

Loops through the source feature services.
Applies filtering logic based on On-Hold Reason, district validity, and other custom conditions.
Feature Insertion:

Inserts qualified features into the master feature class.
Avoids duplication by checking existing control numbers.
Backup Creation:

Identifies features to be removed from the master layer.
Saves them into a backup geodatabase for safekeeping.
Field Updates:

Updates specific fields (Billing_Category, Vegetation_Clearing, etc.) using logic tailored to each source layer.
Customization
The script is modular and allows for easy customization:

Add or remove source feature services in the feature_classes list.
Modify filtering criteria in the add_filtered_features function.
Adjust field mapping as required for your project.
