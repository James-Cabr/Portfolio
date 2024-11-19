import os
import arcpy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Feature service paths
VMfs = r"https://services1.arcgis.com/REPLACE_WITH_FEATURE_SERVICE/FeatureServer/0"
VM_Photos = r"https://services1.arcgis.com/REPLACE_WITH_FEATURE_SERVICE/FeatureServer/1"

# Create a feature layer from the feature service
vm_layer = arcpy.management.MakeFeatureLayer(VMfs, "vm_layer")
vm_photo_layer = arcpy.management.MakeTableView(VM_Photos, "vm_photo_layer")

# Calculating max and min time of the previous day
dt = datetime.today()
print("The date the script is running for is: ", dt)

yesterday = dt - timedelta(days=1)
print("The submission query date is: ", yesterday)

yesterday_print = yesterday.strftime('%m/%d/%Y')  # Format for email
today_min = datetime.combine(dt, datetime.min.time())
yesterday_min = today_min - timedelta(days=1)
yesterday_df_min = yesterday_min.strftime('%m/%d/%Y %H:%M')
print("The beginning query time is: ", yesterday_df_min)

today_max = datetime.combine(dt, datetime.max.time())
yesterday_max = today_max - timedelta(days=1)
yesterday_df_max = yesterday_max.strftime('%m/%d/%Y %H:%M')
print("The ending query time is: ", yesterday_df_max)

YYYYMMDD = dt.strftime('%Y%m%d_')  # Format for CSV naming
print("The file date format is: ", YYYYMMDD)

# Mapping for columns in CSVs
column_mapping = {
    'EndDate': 'Date Form Submitted',
    'StartDate': 'Date Actually Surveyed or Monitored',
    'ERM_FirstName': 'First Name',
    'ERM_SurveyorName': 'Last Name',
    'ConsultantProjectIdentifier': 'Work Order ID',
    'LocationID': 'Location ID',
    'ERM_Form_Type': 'Form Type',
    'ERM_Begin_Survey': 'Accessed?'
}

# Path to the Master Tracker Excel file
userName = os.getlogin()
masterTrackerXlPath = os.path.join(r"C:\Users", userName, r"Documents\ERM\REPLACE_WITH_PROJECT\Master_Tracker.xlsx")

# Load the Master Tracker sheet
dfm = pd.read_excel(masterTrackerXlPath, sheet_name="MAT", dtype={
    "Work Order ID": str,
    "NBS": str,
    "Field Survey": str,
    "Plant Survey": str,
    "Bio Mon Phase": str,
    "Waters Mon Phase": str,
    "Arch Mon/Survey Phase": str
})
dfm['Date submitted (DO NOT EDIT CELLS)'] = pd.to_datetime(
    dfm['Date submitted (DO NOT EDIT CELLS)'], format='%Y%m%d'
).dt.strftime('%m/%d/%Y %H:%M')


def GetDfFromFC(vm_layer, company_name) -> pd.DataFrame:
    """Convert a feature class table to a pandas DataFrame."""
    columns = ["EndDate", "StartDate", "ERM_FirstName", "ERM_SurveyorName",
               "ConsultantProjectIdentifier", "LocationID", "BioFieldType",
               "ERM_Form_Type", "GlobalID", "ERM_Begin_Survey"]
    sql = f"ERM_Company_Name = '{company_name}'"

    with arcpy.da.SearchCursor(vm_layer, columns, sql) as cursor:
        data = [row for row in cursor]

    return pd.DataFrame(data=data, columns=columns)


def GetPhotoDfFromFC(vm_photo_layer, sql) -> pd.DataFrame:
    """Convert a feature class table to a pandas DataFrame for photos."""
    columns = ["GlobalID", "ResourceSupportReqPhoto", "Survey_Monitor_WorkType", "PhotoWorkStatus",
               "PhotoViewFrame", "PhotoMetadataDirection", "PhotoViewDirection", "PhotoLocationID",
               "PhotoComment", "parentglobalid", "CreationDate", "Creator", "EditDate", "Editor"]

    with arcpy.da.SearchCursor(vm_photo_layer, columns, sql) as cursor:
        data = [row for row in cursor]

    return pd.DataFrame(data=data, columns=columns)


def aggregate_unique_values(series):
    """Aggregate unique values in a column."""
    all_values = [item for sublist in series.str.split(',') for item in sublist]
    unique_values = list(dict.fromkeys(all_values))
    return ','.join(unique_values)


def ProcessSubConsultant(sub_consultant_name, output_folder):
    """Process data for a sub-consultant and export."""
    print(f"Processing data for {sub_consultant_name}...")
    sub_consultant_df = GetDfFromFC(vm_layer, sub_consultant_name)

    if not sub_consultant_df.empty:
        guid_list = sub_consultant_df['GlobalID'].tolist()
        if len(guid_list) > 1:
            where_sub_ph = f"parentglobalid IN {tuple(guid_list)}"
        else:
            where_sub_ph = f"parentglobalid = '{guid_list[0]}'"

        sub_ph_df = GetPhotoDfFromFC(vm_photo_layer, where_sub_ph)

        # Count the number of photos per GUID
        uni_guids = pd.unique(sub_ph_df['parentglobalid'])
        sub_guid_dict = {guid: sub_ph_df['parentglobalid'].value_counts()[guid] for guid in uni_guids}

        # Map the photo counts to the main DataFrame
        sub_consultant_df["Number of Photos"] = sub_consultant_df['GlobalID'].map(sub_guid_dict)

        # Reformat columns and process
        sub_consultant_df["ERM_Form_Type"] = np.where(
            sub_consultant_df["BioFieldType"] == "Pre-Activity Survey",
            "Bio Survey",
            sub_consultant_df['ERM_Form_Type']
        )
        sub_consultant_df["ERM_Form_Type"] = np.where(
            (sub_consultant_df["BioFieldType"] == "TBD") &
            (sub_consultant_df["ConsultantProjectIdentifier"].str.contains('Monitor')),
            "Arch Monitor",
            sub_consultant_df["ERM_Form_Type"]
        )
        sub_consultant_df["ERM_Form_Type"] = np.where(
            (sub_consultant_df["BioFieldType"] == "TBD") &
            (sub_consultant_df["ConsultantProjectIdentifier"].str.contains('Survey')),
            "Arch Survey",
            sub_consultant_df["ERM_Form_Type"]
        )
        sub_consultant_df["ERM_Begin_Survey"] = np.where(
            sub_consultant_df["ERM_Begin_Survey"].isnull(),
            "Yes",
            sub_consultant_df['ERM_Begin_Survey']
        )
        sub_consultant_df.drop(['BioFieldType', 'GlobalID'], axis=1, inplace=True)
        sub_consultant_df.rename(columns=column_mapping, inplace=True)

        # Format date columns
        sub_consultant_df['Date Form Submitted'] = pd.to_datetime(
            sub_consultant_df['Date Form Submitted'], format='%m/%d/%Y %H:%M:%S.%f'
        ).dt.strftime('%m/%d/%Y %H:%M')
        sub_consultant_df['Date Actually Surveyed or Monitored'] = pd.to_datetime(
            sub_consultant_df['Date Actually Surveyed or Monitored'], format='%m/%d/%Y %H:%M:%S.%f'
        ).dt.strftime('%m/%d/%Y %H:%M')

        # Filter data for yesterday's date range
        filtered_df = sub_consultant_df.loc[
            (sub_consultant_df['Date Form Submitted'] >= yesterday_df_min) &
            (sub_consultant_df['Date Form Submitted'] <= yesterday_df_max)
        ]

        if filtered_df.empty:
            print(f"No forms submitted yesterday by {sub_consultant_name}.")
            return

        # Process for invoicing summary
        woid_list = filtered_df['Work Order ID'].tolist()
        dfm_yest = dfm[dfm['Work Order ID'].isin(woid_list)]
        dfm_refined = dfm_yest[[
            "Work Order ID", "NBS", "Field Survey", "Plant Survey",
            "Bio Mon Phase", "Waters Mon Phase", "Arch Mon/Survey Phase"
        ]]
        dfm_merge = pd.merge(filtered_df, dfm_refined, on="Work Order ID")
        dfm_merge = dfm_merge.drop(columns=[
            'Date Form Submitted', 'Form Type', 'Number of Photos', 'Accessed?'
        ])

        # Format the date and group data by phase
        dfm_merge["Date"] = pd.to_datetime(
            dfm_merge["Date Actually Surveyed or Monitored"], format='%m/%d/%Y %H:%M'
        ).dt.strftime('%m/%d/%Y').astype(str)
        dfm_merge["Date"] = dfm_merge['Date'].astype(str)

        field_list = ["First Name", "Last Name", "Date"]
        for field in field_list:
            dfm_merge[field] = dfm_merge[field].apply(lambda x: x.strip())

        # Group by phase and aggregate unique Location IDs
        grouped_phases = []
        phase_columns = [
            "NBS", "Field Survey", "Plant Survey", "Bio Mon Phase",
            "Waters Mon Phase", "Arch Mon/Survey Phase"
        ]
        for phase in phase_columns:
            grouped = dfm_merge.groupby([phase, "First Name", "Last Name", "Date"], as_index=False).agg(
                {'Location ID': lambda x: list(x)}
            )
            grouped_phases.append(grouped)

        dfm_2merge = pd.concat(grouped_phases)
        dfm_2merge["Phase"] = dfm_2merge[phase_columns].bfill(axis=1).iloc[:, 0]
        dfm_2merge["Location ID"] = dfm_2merge["Location ID"].apply(
            lambda x: ','.join(map(str, x)).replace(" ", "")
        )
        dfm_2merge = dfm_2merge.drop(columns=phase_columns).reset_index(drop=True)

        dfm_2merge["Hours"] = ""  # Add Hours column
        desired_order = ['First Name', 'Last Name', 'Date', 'Location ID', 'Phase', 'Hours']
        dfm_2merge = dfm_2merge[desired_order]

        # Write to Excel
        sub_excel = os.path.join(output_folder, f"{sub_consultant_name}_{YYYYMMDD}.xlsx")
        with pd.ExcelWriter(sub_excel) as writer:
            filtered_df.to_excel(writer, sheet_name='Daily Submission Summary', index=False)
            dfm_2merge.to_excel(writer, sheet_name='Invoicing Summary', index=False)

        # Send email
        toVal = 'example1@domain.com; example2@domain.com'
        ccVal = 'examplecc@domain.com'
        subject = f"Daily Form Submissions - {sub_consultant_name} ({yesterday_print})"
        scriptPath = r"C:\REPLACE_WITH_PATH\send_email_script.vbs"
        html = f"<p>Here are the submissions for {yesterday_print}.</p>"
        os.system(f'{scriptPath} "{toVal}" "{ccVal}" "{subject}" "{html}" "{sub_excel}"')

        print(f"Data for {sub_consultant_name} processed and exported successfully.")
    else:
        print(f"No forms submitted by {sub_consultant_name}.")



def DeleteOutdatedCSVs():
    """Delete outdated files from folders."""
    folders = [
        r"C:\REPLACE_WITH_PATH\Folder1",
        r"C:\REPLACE_WITH_PATH\Folder2"
    ]
    sevendays = datetime.now() - timedelta(days=7)

    for folder in folders:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                file_time = os.path.getmtime(file_path)
                if datetime.fromtimestamp(file_time) < sevendays:
                    os.remove(file_path)


def main():
    try:
        print("Script starting...")
        sub_consultant_name = "SUB_CONSULTANT_NAME"
        output_folder = r"C:\REPLACE_WITH_PATH\SubConsultantReports"
        ProcessSubConsultant(sub_consultant_name, output_folder)
        DeleteOutdatedCSVs()
    except Exception as e:
        toVal = 'example1@domain.com'
        ccVal = 'examplecc@domain.com'
        scriptPath = r"C:\REPLACE_WITH_PATH\send_email_script.vbs"
        html = f"<p>Error: {e}</p>"
        subject = "SCRIPT ERROR"
        os.system(f'{scriptPath} "{toVal}" "{ccVal}" "{subject}" "{html}"')
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    main()
