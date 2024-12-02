# Portfolio
Overview
This repository contains scripts designed to streamline GIS workflows for feature service management, reporting, data integration, and remote sensing classification. These scripts use ArcPy, Python, and integrations like Smartsheet to automate data handling and communication. While each script is independent, they can work together to create a cohesive data management workflow.

Scripts Overview
1. Daily Submission Emailer
Purpose:
Automates tracking and reporting of subcontractor form submissions from a feature service.
Sends email notifications summarizing daily submissions to stakeholders and subcontractors.
Key Features:
Queries submissions from the last 24 hours.
Generates lists of subcontractors who did and did not submit forms.
Sends automated email summaries to recipients.
Usage:
Run daily to monitor submission activity.
Outputs:
Email Summary: Sent to subcontractors and stakeholders.
Dependencies:
Requires access to the feature service containing submission data.
Configurable email automation for sending summaries.
2. Master Feature Service Updater
Purpose:
Consolidates data from multiple source layers into a master feature service while applying custom field mappings and logic.
Handles large-scale GIS workflows where multiple datasets need to be unified into one feature class.
Key Features:
Pulls features from layers like:
Structure Brushing
Hazard Tree
Supplemental Patrols
AGOL Desktop Review
Arbora Workpoints
Applies logic to populate fields such as:
Program
Work Class
Billing Category
Access Route
Removes outdated features from the master service while creating backups.
Usage:
Typically run at the start of the workflow to ensure the master service is up to date.
Outputs:
Updated master feature service.
Backups of removed features.
Dependencies:
Requires source layers to be accessible via AGOL or as feature services.
Ideal for workflows requiring regular updates to the master service.
3. Spatial Join Script
Purpose:
Enriches the master feature service with spatial data through automated joins with external layers.
Works as a companion to the Master Feature Service Updater, applying spatial updates post-ingestion.
Key Features:
Performs spatial joins with layers such as:
Whitebark Pine Areas
Wilderness Areas
Government Lands
FERC Boundaries
Riparian Conservation Areas (FEIS and INF)
Updates fields like:
Wilderness Area
Whitebark Pine Survey Required
Geographic Area
Waters/Wetlands Work Class
Usage:
Run after the Master Feature Service Updater for spatial enrichment.
Outputs:
Enhanced master feature service with additional attributes from spatial joins.
Dependencies:
Requires access to external spatial layers and a populated master feature service.
4. Smartsheet Data Integrator
Purpose:
Synchronizes data between a Smartsheet and a GIS feature service.
Ensures data consistency and automates updates from a tabular format to a geospatial service.
Key Features:
Pulls data from Smartsheet and processes it into a DataFrame.
Appends or updates records in a GIS feature service.
Supports handling of attachments and mapping tabular fields to feature service attributes.
Usage:
Ideal for workflows involving external collaboration or project tracking via Smartsheet.
Outputs:
Updated feature service based on Smartsheet data.
Dependencies:
Requires access to Smartsheet API and AGOL feature service.
Recommended Workflow
Daily Submission Emailer:
Monitor subcontractor form submissions and notify stakeholders.
Master Feature Service Updater:
Ingest and consolidate data into the master feature service.
Spatial Join Script:
Apply spatial enrichments to the master feature service.
Smartsheet Data Integrator:
Synchronize external Smartsheet data with GIS feature services.
5. Maximum Likelihood Classification
Purpose: This script implements a Maximum Likelihood Classification (MLC) algorithm combined with region growing for multispectral raster images. It is designed for remote sensing workflows to classify land cover based on spectral properties. Using user-defined seed points, the script grows regions based on spectral similarity and computes statistical parameters (mean vectors and covariance matrices) for each class. Each pixel is then classified into the most likely class using a multivariate Gaussian distribution. The output is a classified raster image that can be used for land cover analysis or feature extraction in remote sensing projects.
