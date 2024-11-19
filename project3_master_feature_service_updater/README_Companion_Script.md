Overview
This script performs spatial joins on an existing MSUP Feature Service to enrich it with additional spatial data from various related feature layers. It is designed as a companion to the Master_Feature_Service_Updater script, which focuses on filtering, inserting, and updating features within the master feature class.

While the Master_Feature_Service_Updater script primarily handles importing and maintaining the core feature dataset, this script focuses on spatially enriching the existing features in the MSUP feature service by joining them with external layers, such as wilderness areas, government lands, and SCE districts.

Key Features
Spatial Joins:

Performs spatial joins between the MSUP master feature class and several supporting spatial layers, such as:
Whitebark Pine Survey Areas
Wilderness Areas
Government Lands
Ranger Districts
SCE Districts
Township and Range
FERC Boundaries
FEIS Riparian Conservation Areas
INF Riparian Conservation Areas
Enriches the MSUP master feature class with attributes like:
Survey requirements
Wilderness area designations
Forest name and ranger district
SCE district and geographic area
FERC notifications
Waters/Wetlands classifications and reviews.
Field Updates:

Populates fields in the MSUP feature class if they are missing or incomplete.
Updates attributes based on spatial join results or default logic where spatial data is unavailable.
Efficiency:

Uses in-memory processing for faster execution.
Dynamically skips processing for records with already populated fields.
Handles exclusions for specific internal IDs (e.g., XX056).
Integration:

Complements the Master_Feature_Service_Updater script by ensuring that spatial information is properly updated after new features are added to the feature service.
Script Workflow
Input
The MSUP master feature class is accessed via a URL. This feature service contains the core dataset to be enriched.
External feature layers (e.g., Whitebark Pine Survey, Wilderness Areas) are accessed via URLs or local paths.
Processing Steps
Set Up Temporary Layers:

Creates in-memory layers for each spatial join operation.
Deletes any pre-existing temporary layers.
Spatial Joins:

Performs SpatialJoin operations between the MSUP master feature class and the external layers.
Generates dictionaries that map feature IDs to attribute values for updates.
Attribute Updates:

Iterates through the MSUP feature class to update fields with spatial join results.
Uses default logic where necessary (e.g., if no spatial join match is found).
Clean-Up:

Deletes all temporary layers to free up memory and storage.
Companion to Master_Feature_Service_Updater Script
The Master_Feature_Service_Updater script focuses on:

Adding new features to the MSUP master feature class from multiple source layers.
Assigning default attributes and ensuring proper field mappings for newly added records.
Filtering records to only include those relevant to the MSUP program.
This script complements it by:

Enriching the dataset with spatially relevant data after features are added.
Ensuring all geographic and regulatory attributes are up-to-date, even for pre-existing records.
Together, these scripts maintain a dynamic and complete MSUP master feature class that integrates both tabular and spatial data.

Configuration
Before running the script:

Dependencies:

Ensure arcpy is available (requires ArcGIS Pro or ArcGIS Server).
Required Python version: 3.x.
Access to the feature service URLs and local paths specified in the script.
Customizations:

Update URLs for the MSUP master feature class and external layers as needed.
Adjust the excluded_internal_ids list to exclude specific records from updates.
Running the Script
Run this script after running the Master_Feature_Service_Updater script, or independently if spatial updates are the sole requirement.
Ensure that the master feature class contains the required fields for updates:
Wilderness_Area, Whitebark_Pine_Survey_Required, Forest, Ranger_District, SCE_District, etc.
