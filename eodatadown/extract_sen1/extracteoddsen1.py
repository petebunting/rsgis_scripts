import eodatadown.eodatadownsystemmain
import eodatadown.eodatadownutils
import rsgislib
import rsgislib.imageutils
import rsgislib.vectorutils
import rsgislib
import datetime
import pprint
import glob
import os
import json

def subset_mask_img(input_img, roi_vec_file, roi_vec_lyr, scn_tmp_dir, out_img):
    basename = os.path.splitext(os.path.basename(input_img))[0]
    rsgis_utils = rsgislib.RSGISPyUtils()
    bbox = rsgis_utils.getVecLayerExtent(roi_vec_file, roi_vec_lyr)
    rsgis_dtype = rsgis_utils.getRSGISLibDataTypeFromImg(input_img)
    sub_img = os.path.join(scn_tmp_dir, "{}_sub.kea".format(basename))
    rsgislib.imageutils.subsetbbox(input_img, sub_img, 'KEA', rsgis_dtype, bbox[0], bbox[1], bbox[2], bbox[3])
    msk_img = os.path.join(scn_tmp_dir, "{}_msk.kea".format(basename))
    rsgislib.vectorutils.rasteriseVecLyr(roi_vec_file, roi_vec_lyr, sub_img, msk_img, gdalformat="KEA")
    rsgislib.imageutils.maskImage(sub_img, msk_img, out_img, "GTIFF", rsgis_dtype, 32767, 0)
    rsgislib.imageutils.popImageStats(out_img, usenodataval=True, nodataval=32767, calcpyramids=True)

def export_metadata(scn, md_file):
    eodd_utils = eodatadown.eodatadownutils.EODataDownUtils()
    metadata = dict()
    metadata['Scene_ID'] = scn.Scene_ID
    metadata['Product_Name'] = scn.Product_Name
    metadata['Product_File_ID'] = scn.Product_File_ID
    metadata['ABS_Orbit'] = scn.ABS_Orbit
    metadata['Rel_Orbit'] = scn.Rel_Orbit
    metadata['Doppler'] = scn.Doppler
    metadata['Flight_Direction'] = scn.Flight_Direction
    metadata['Granule_Name'] = scn.Granule_Name
    metadata['Granule_Type'] = scn.Granule_Type
    metadata['Incidence_Angle'] = scn.Incidence_Angle
    metadata['Look_Direction'] = scn.Look_Direction
    metadata['Platform'] = scn.Platform
    metadata['Polarization'] = scn.Polarization
    metadata['Process_Date'] = eodd_utils.getDateTimeAsString(scn.Process_Date)
    metadata['Process_Description'] = scn.Process_Description
    metadata['Process_Level'] = scn.Process_Level
    metadata['Process_Type'] = scn.Process_Type
    metadata['Process_Type_Disp'] = scn.Process_Type_Disp
    metadata['Acquisition_Date'] = eodd_utils.getDateTimeAsString(scn.Acquisition_Date)
    metadata['Scene_ID'] = scn.Scene_ID
    metadata['Sensor'] = eodd_utils.getDateTimeAsString(scn.BeginPosition)
    metadata['Scene_ID'] = eodd_utils.getDateTimeAsString(scn.EndPosition)
    
    with open(md_file, 'w') as outfile:
        json.dump(metadata, outfile, indent=4, separators=(',', ': '), ensure_ascii=False)



def extract_sen1_img_data(eodd_config_file, roi_vec_file, roi_vec_lyr, start_date, end_date, out_dir, tmp_dir):
    rsgis_utils = rsgislib.RSGISPyUtils()
    bbox = rsgis_utils.getVecLayerExtent(roi_vec_file, roi_vec_lyr)
    bbox_wgs84 = rsgis_utils.reprojBBOX_epsg(bbox, 27700, 4326)
    
    sys_main_obj = eodatadown.eodatadownsystemmain.EODataDownSystemMain()
    sys_main_obj.parse_config(eodd_config_file)

    sen_obj = sys_main_obj.get_sensor_obj("Sentinel1ASF")    
    scns = sen_obj.query_scn_records_date_bbox(start_date, end_date, bbox_wgs84, start_rec=0, n_recs=0, valid=True, cloud_thres=None)
    print("N scns = {}".format(len(scns)))
    
    for scn in scns:
        print(scn.ARDProduct_Path)
        scn_dB_file = glob.glob(os.path.join(scn.ARDProduct_Path, "*dB_osgb.tif"))
        if len(scn_dB_file) == 1:
            scn_dB_file = scn_dB_file[0]
        else:
            raise Exception("There should only be 1 dB image for the scene.")
        basename = os.path.splitext(os.path.basename(scn_dB_file))[0]
        scn_dir = os.path.join(out_dir, "{}_{}".format(scn.Product_File_ID, scn.PID))
        if not os.path.exists(scn_dir):
            os.mkdir(scn_dir)
            
        scn_tmp_dir = os.path.join(tmp_dir, "{}_{}".format(scn.Product_File_ID, scn.PID))
        if not os.path.exists(scn_tmp_dir):
            os.mkdir(scn_tmp_dir)
        
        metadata_file = os.path.join(scn_dir, "{}.json".format(basename))
        export_metadata(scn, metadata_file)
        
        out_img = os.path.join(scn_dir, "{}_sub.tif".format(basename))
        subset_mask_img(scn_dB_file, roi_vec_file, roi_vec_lyr, scn_tmp_dir, out_img)
        print("")
        
os.environ["RSGISLIB_IMG_CRT_OPTS_GTIFF"] = "TILED=YES:COMPRESS=LZW:BIGTIFF=YES"
config_file = '/bigdata/eodd_wales_ard/scripts/eodd/config/EODataDownBaseConfig_psql.json'
roi_vec_file = '/data/extract_sen1_data/wye_roi_osgb.geojson'
roi_vec_lyr = 'wye_roi_osgb'
start_date = datetime.datetime.now()
end_date = datetime.datetime(year=2019, month=1, day=1)
out_dir = '/data/extract_sen1_data/out_data'
tmp_dir = '/data/extract_sen1_data/tmp'

extract_sen1_img_data(config_file, roi_vec_file, roi_vec_lyr, start_date, end_date, out_dir, tmp_dir)
