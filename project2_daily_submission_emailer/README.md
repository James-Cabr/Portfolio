Sub-Consultant Daily Submission Processing Script
Overview
This script automates the processing of daily submissions from sub-consultants for a project managed in ArcGIS. It extracts and processes data from an ArcGIS Feature Service and outputs reports in Excel format for daily submission summaries and invoicing summaries. Additionally, it handles sending automated emails to notify stakeholders of the results.

Features
Data Extraction: Fetches sub-consultant submission data from an ArcGIS Online Feature Service.
Photo Analysis: Counts the number of photos associated with each submission.
Invoicing Preparation: Groups submissions by phase and aggregates unique location IDs for invoicing summaries.
Email Notifications: Automatically sends emails with the generated reports attached.
Automated Cleanup: Deletes outdated CSV and Excel files from specified folders.
Prerequisites
Before running the script, ensure the following:

Python (version 3.6 or higher) installed.
Required Python libraries:
arcpy (requires ArcGIS Pro installation)
pandas
numpy
Access to:
ArcGIS Online Feature Service with the required permissions.
The Master Tracker Excel file (MAT sheet).
A valid .vbs script for sending emails (modify the path as needed).
Properly configured folder paths for saving reports and cleaning old files.

Update the script with the following details:

Feature Service URLs: Replace REPLACE_WITH_FEATURE_SERVICE with the URLs for your ArcGIS Feature Service and photo table.
File Paths: Replace REPLACE_WITH_PATH with the appropriate file paths for:
Master Tracker Excel file.
Folders for saving reports and cleaning outdated files.
The .vbs email script.
Email Addresses: Replace example1@domain.com, example2@domain.com, etc., with the actual recipient email addresses.

Outputs
The script generates:

Daily Submission Summary: A report showing all forms submitted by the sub-consultant during the specified date range.
Invoicing Summary: A report summarizing data by phase, including aggregated location IDs.
The reports are saved in Excel format in the specified output folder.
