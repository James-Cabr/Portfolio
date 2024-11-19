"""Runs in conjunction with Master_MSUP_WOrkpoints_FS script but can be run separately to do spatial joins only if features already exist in FS
Created June 2024 by James C.  Work in progress.
8/1/2024 Added "Waters_Wetlands_Work_Class", "Waters_Wetlands_Review", "Waters_Wetlands_RPMs" spatial join
"""

import arcpy

def main():
    # URLs for the feature layers
    master_feature_class_url = r"https://example.com/arcgis/rest/services/MSUP_Feature_Class/FeatureServer/7"
    whitebark_pine_layer_url = r"https://example.com/arcgis/rest/services/GeneralBioReview/FeatureServer/25"
    wilderness_area_layer_url = r"https://example.com/arcgis/rest/services/GovtLands_Additional/FeatureServer/13"
    government_lands_layer_url = r"https://example.com/arcgis/rest/services/GeneralBioReview/FeatureServer/13"
    ranger_district_layer_url = r"https://example.com/arcgis/rest/services/GeneralBioReview/FeatureServer/28"
    sce_district_layer_url = r"https://example.com/arcgis/rest/services/SCELayers/FeatureServer/5"
    township_layer_url = r"https://example.com/arcgis/rest/services/Cadastral/MapServer/1"
    section_layer_url = r"https://example.com/arcgis/rest/services/Cadastral/MapServer/2"
    ferc_boundaries_layer_url = r"https://example.com/arcgis/rest/services/GeneralBioReview/FeatureServer/9"
    feis_rca_layer_url = r"\\SharedDrive\Data\MSUP_Script_Layers.gdb\FEIS_Riparian_Conservation_Areas"
    rca_inf_layer_url = r"https://example.com/arcgis/rest/services/Riparian_Conservation_Areas_INF_LMP/FeatureServer/0"

    master_feature_class_url_layer = arcpy.management.MakeFeatureLayer(master_feature_class_url, "master_feature_class_url_layer")
    whitebark_pine_layer = arcpy.management.MakeFeatureLayer(whitebark_pine_layer_url, "whitebark_pine_layer")
    wilderness_area_layer = arcpy.management.MakeFeatureLayer(wilderness_area_layer_url, "wilderness_area_layer")
    government_lands_layer = arcpy.management.MakeFeatureLayer(government_lands_layer_url, "government_lands_layer")
    ranger_district_layer = arcpy.management.MakeFeatureLayer(ranger_district_layer_url, "ranger_district_layer")
    sce_district_layer = arcpy.management.MakeFeatureLayer(sce_district_layer_url, "sce_district_layer")
    township_layer = arcpy.management.MakeFeatureLayer(township_layer_url, "township_layer")
    section_layer = arcpy.management.MakeFeatureLayer(section_layer_url, "section_layer")
    ferc_boundaries_layer = arcpy.management.MakeFeatureLayer(ferc_boundaries_layer_url, "ferc_boundaries_layer")
    feis_rca_layer = arcpy.management.MakeFeatureLayer(feis_rca_layer_url, "feis_rca_layer")
    rca_inf_layer = arcpy.management.MakeFeatureLayer(rca_inf_layer_url, "rca_inf_layer")

    # Local workspace for temporary data
    arcpy.env.workspace = "in_memory"

    temp_join_fc_whitebark = "temp_join_whitebark"
    temp_join_fc_wilderness = "temp_join_wilderness"
    temp_join_fc_government = "temp_join_government"
    temp_join_fc_ranger = "temp_join_ranger"
    temp_join_fc_sce_district = "temp_join_sce_district"
    temp_join_fc_township = "temp_join_township"
    temp_join_fc_section = "temp_join_section"
    temp_join_fc_ferc = "temp_join_ferc"
    temp_join_fc_feis_rca = "temp_join_fc_feis_rca"
    temp_join_fc_rca_inf = "temp_join_fc_rca_inf"

    for temp_fc in [temp_join_fc_whitebark, temp_join_fc_wilderness, temp_join_fc_government, temp_join_fc_ranger,
                    temp_join_fc_sce_district, temp_join_fc_township, temp_join_fc_section, temp_join_fc_ferc,
                    temp_join_fc_feis_rca, temp_join_fc_rca_inf]:
        if arcpy.Exists(temp_fc):
            arcpy.Delete_management(temp_fc)

    # WBP JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, whitebark_pine_layer, temp_join_fc_whitebark, "KEEP_ALL", "WITHIN")
    survey_required_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_whitebark, ["TARGET_FID", "Join_Count"]) as cursor:
        for row in cursor:
            survey_required_dict[row[0]] = 'Yes' if row[1] > 0 else 'No'

    # Wilderness JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, wilderness_area_layer, temp_join_fc_wilderness, "KEEP_ALL", "WITHIN")
    wilderness_required_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_wilderness, ["TARGET_FID", "Join_Count"]) as cursor:
        for row in cursor:
            wilderness_required_dict[row[0]] = 'Yes' if row[1] > 0 else 'No'

    # Government JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, government_lands_layer, temp_join_fc_government, "KEEP_ALL", "INTERSECT")
    forest_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_government, ["TARGET_FID", "AGENCY_ARE"]) as cursor:
        for row in cursor:
            forest_dict[row[0]] = row[1]

    # Ranger JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, ranger_district_layer, temp_join_fc_ranger, "KEEP_ALL", "INTERSECT")
    ranger_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_ranger, ["TARGET_FID", "DISTRICTNAME"]) as cursor:
        for row in cursor:
            ranger_dict[row[0]] = row[1]

    # SCE District JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, sce_district_layer, temp_join_fc_sce_district, "KEEP_ALL", "INTERSECT")
    sce_district_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_sce_district, ["TARGET_FID", "DistrictNumber", "NAME"]) as cursor:
        for row in cursor:
            sce_district_dict[row[0]] = (row[1], row[2])

    # Township JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, township_layer, temp_join_fc_township, "KEEP_ALL", "INTERSECT")
    township_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_township, ["TARGET_FID", "TWNSHPLAB"]) as cursor:
        for row in cursor:
            township_dict[row[0]] = (row[1],)

    # Section JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, section_layer, temp_join_fc_section, "KEEP_ALL", "INTERSECT")
    with arcpy.da.SearchCursor(temp_join_fc_section, ["TARGET_FID", "FRSTDIVNO"]) as cursor:
        for row in cursor:
            township_dict[row[0]] += (row[1],)

    # FERC JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, ferc_boundaries_layer, temp_join_fc_ferc, "KEEP_ALL", "INTERSECT")
    ferc_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_ferc, ["TARGET_FID", "Join_Count"]) as cursor:
        for row in cursor:
            ferc_dict[row[0]] = 'Yes' if row[1] > 0 else 'No'

    # FEIS JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, feis_rca_layer, temp_join_fc_feis_rca, "KEEP_ALL", "INTERSECT")
    waters_feis_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_feis_rca, ["TARGET_FID", "Join_Count"]) as cursor:
        for row in cursor:
            waters_feis_dict[row[0]] = 'Yes' if row[1] > 0 else 'No'

    # INF JOIN
    arcpy.analysis.SpatialJoin(master_feature_class_url_layer, rca_inf_layer, temp_join_fc_rca_inf, "KEEP_ALL", "INTERSECT")
    waters_INF_dict = {}
    with arcpy.da.SearchCursor(temp_join_fc_rca_inf, ["TARGET_FID", "Join_Count"]) as cursor:
        for row in cursor:
            waters_INF_dict[row[0]] = 'Yes' if row[1] > 0 else 'No'

    # Update fields
    excluded_internal_ids = ['XX056']
    where_clause = ("Wilderness_Area IS NULL OR Whitebark_Pine_Survey_Required IS NULL OR Forest IS NULL OR Ranger_District IS NULL "
                    "OR SCE_District IS NULL OR Geographic_Area IS NULL OR FERC_Notification_Required IS NULL "
                    "OR Waters_Wetlands_Work_Class IS NULL OR Waters_Wetlands_Review1 IS NULL OR Waters_Wetlands_RPMs IS NULL")

    with arcpy.da.UpdateCursor(master_feature_class_url_layer, ["OBJECTID", "Wilderness_Area", "Whitebark_Pine_Survey_Required",
                                                                "Forest", "Ranger_District", "SCE_District", "Geographic_Area",
                                                                "FERC_Notification_Required", "Waters_Wetlands_Work_Class",
                                                                "Waters_Wetlands_Review1", "Waters_Wetlands_RPMs", "Internal_ID"],
                               where_clause) as cursor:
        for row in cursor:
            # Update logic here...
            cursor.updateRow(row)

    # Clean up
    for temp_fc in [temp_join_fc_whitebark, temp_join_fc_wilderness, temp_join_fc_government, temp_join_fc_ranger,
                    temp_join_fc_sce_district, temp_join_fc_township, temp_join_fc_section, temp_join_fc_ferc,
                    temp_join_fc_feis_rca, temp_join_fc_rca_inf]:
        arcpy.Delete_management(temp_fc)

    print("Update completed successfully.")

if __name__ == "__main__":
    main()
