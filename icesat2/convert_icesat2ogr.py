import h5py
import argparse
import os.path

from osgeo import gdal
from osgeo import ogr
from osgeo import osr


def exportATL08(input_icesat_h5file, out_vec_file, out_vec_lyr, vec_frmt='GPKG'):
    """
A function to import a ATL08 ICESAT2 hdf5.

* input_icesat_file
* out_vec_file
* out_vec_lyr
* vec_frmt

    """

    if os.path.exists(out_vec_file):
        vecDS = gdal.OpenEx(out_vec_file, gdal.GA_Update)
    else:            
        outdriver = ogr.GetDriverByName(vec_frmt)
        vecDS = outdriver.CreateDataSource(out_vec_file)
    
    if vecDS is None:
        raise Exception("Could not open or create '{}'".format(out_vec_file))   
    
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    
    laser_beams = ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']
    flds_dict = dict()
    # General
    flds_dict['segment_id'] = ogr.OFTInteger
    flds_dict['segment_id_beg'] = ogr.OFTInteger
    flds_dict['segment_id_end'] = ogr.OFTInteger
    flds_dict['latitude'] = ogr.OFTReal
    flds_dict['longitude'] = ogr.OFTReal
    flds_dict['solar_azimuth'] = ogr.OFTReal
    flds_dict['solar_elevation'] = ogr.OFTReal
    flds_dict['delta_time'] = ogr.OFTReal
    flds_dict['delta_time_beg'] = ogr.OFTReal
    flds_dict['delta_time_end'] = ogr.OFTReal
    flds_dict['night_flag'] = ogr.OFTInteger
    flds_dict['dem_h'] = ogr.OFTReal
    flds_dict['dem_flag'] = ogr.OFTInteger
    flds_dict['dem_removal_flag'] = ogr.OFTInteger
    flds_dict['h_dif_ref'] = ogr.OFTReal
    flds_dict['terrain_flg'] = ogr.OFTInteger
    flds_dict['segment_landcover'] = ogr.OFTInteger
    flds_dict['segment_watermask'] = ogr.OFTInteger
    flds_dict['segment_snowcover'] = ogr.OFTInteger
    flds_dict['urban_flag'] = ogr.OFTInteger
    flds_dict['cloud_flag_asr'] = ogr.OFTInteger
    flds_dict['surf_type'] = ogr.OFTInteger
    flds_dict['snr'] = ogr.OFTReal
    # Terrain
    flds_dict['h_te_mean'] = ogr.OFTReal
    flds_dict['h_te_median'] = ogr.OFTReal
    flds_dict['h_te_min'] = ogr.OFTReal
    flds_dict['h_te_max'] = ogr.OFTReal
    flds_dict['h_te_mode'] = ogr.OFTReal
    flds_dict['h_te_skew'] = ogr.OFTReal
    flds_dict['n_te_photons'] = ogr.OFTInteger
    flds_dict['h_te_interp'] = ogr.OFTReal
    flds_dict['h_te_std'] = ogr.OFTReal
    flds_dict['h_te_uncertainty'] = ogr.OFTReal
    flds_dict['terrain_slope'] = ogr.OFTReal
    flds_dict['h_te_best_fit'] = ogr.OFTReal
    # Canopy
    flds_dict['canopy_h_metrics_abs_p25'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p50'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p60'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p70'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p75'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p80'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p85'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p90'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_abs_p95'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p25'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p50'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p60'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p70'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p75'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p80'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p85'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p90'] = ogr.OFTReal
    flds_dict['canopy_h_metrics_p95'] = ogr.OFTReal
    flds_dict['h_canopy_abs'] = ogr.OFTReal
    flds_dict['h_canopy'] = ogr.OFTReal
    flds_dict['h_mean_canopy_abs'] = ogr.OFTReal
    flds_dict['h_mean_canopy'] = ogr.OFTReal
    flds_dict['h_dif_canopy'] = ogr.OFTReal
    flds_dict['h_min_canopy_abs'] = ogr.OFTReal
    flds_dict['h_min_canopy'] = ogr.OFTReal
    flds_dict['h_max_canopy_abs'] = ogr.OFTReal
    flds_dict['h_max_canopy'] = ogr.OFTReal
    flds_dict['h_canopy_uncertainty'] = ogr.OFTReal
    flds_dict['canopy_openness'] = ogr.OFTReal
    flds_dict['toc_roughness'] = ogr.OFTReal
    flds_dict['h_canopy_quad'] = ogr.OFTReal
    flds_dict['n_ca_photons'] = ogr.OFTInteger
    flds_dict['n_toc_photons'] = ogr.OFTInteger
    flds_dict['centroid_height'] = ogr.OFTReal
    flds_dict['canopy_rh_conf'] = ogr.OFTInteger
    flds_dict['canopy_flag'] = ogr.OFTInteger
    flds_dict['landsat_flag'] = ogr.OFTInteger
    flds_dict['landsat_perc'] = ogr.OFTReal
    
    print("Processing Input File: {}".format(input_icesat_h5file))
    fH5 = h5py.File(input_icesat_h5file)
    for beam_name in laser_beams:
        print("\tProcessing Beam: {}".format(beam_name))
        lyr_name = '{}_{}'.format(out_vec_lyr, beam_name)
        out_lyr_obj = vecDS.CreateLayer(lyr_name, srs, geom_type=ogr.wkbPoint, options=['OVERWRITE=YES'])
        if out_lyr_obj is None:
            raise Exception("Could not create layer: '{}'".format(lyr_name))
        feat_defn = out_lyr_obj.GetLayerDefn()
        
        col_exists = False
        for fld_name in flds_dict:
            #print(fld_name)
            for i in range( feat_defn.GetFieldCount() ):
                if feat_defn.GetFieldDefn(i).GetName().lower() == fld_name.lower():
                    col_exists = True
                    break
    
            if not col_exists:
                field_defn = ogr.FieldDefn( fld_name, flds_dict[fld_name] )
                if out_lyr_obj.CreateField ( field_defn ) != 0:
                    raise Exception("Creating '{}' field failed; becareful with case.".format(fld_name))
        
        lsr_beam_pth = '{}/land_segments'.format(beam_name)
        cnpy_info_pth = '{}/land_segments/canopy'.format(beam_name)
        trn_info_pth = '{}/land_segments/terrain'.format(beam_name)
        land_segs_dir = fH5[lsr_beam_pth]
        cnpy_info_dir = fH5[cnpy_info_pth]
        trn_info_dir = fH5[trn_info_pth]
        
        # General
        segment_id = land_segs_dir['segment_id']
        segment_id_beg = land_segs_dir['segment_id_beg']
        segment_id_end = land_segs_dir['segment_id_end']
        latitude = land_segs_dir['latitude']
        longitude = land_segs_dir['longitude']
        solar_azimuth = land_segs_dir['solar_azimuth']
        solar_elevation = land_segs_dir['solar_elevation']
        delta_time = land_segs_dir['delta_time']
        delta_time_beg = land_segs_dir['delta_time_beg']
        delta_time_end = land_segs_dir['delta_time_end']
        night_flag = land_segs_dir['night_flag']
        dem_h = land_segs_dir['dem_h']
        dem_flag = land_segs_dir['dem_flag']
        dem_removal_flag = land_segs_dir['dem_removal_flag']
        h_dif_ref = land_segs_dir['h_dif_ref']
        terrain_flg = land_segs_dir['terrain_flg']
        segment_landcover = land_segs_dir['segment_landcover']
        segment_watermask = land_segs_dir['segment_watermask']
        segment_snowcover = land_segs_dir['segment_snowcover']
        urban_flag = land_segs_dir['urban_flag']
        last_seg_extend = land_segs_dir['last_seg_extend']
        cloud_flag_asr = land_segs_dir['cloud_flag_asr']
        snr = land_segs_dir['snr']
        # Terrain
        h_te_mean = trn_info_dir['h_te_mean']
        h_te_median = trn_info_dir['h_te_median']
        h_te_min = trn_info_dir['h_te_min']
        h_te_max = trn_info_dir['h_te_max']
        h_te_mode = trn_info_dir['h_te_mode']
        h_te_skew = trn_info_dir['h_te_skew']
        n_te_photons = trn_info_dir['n_te_photons']
        h_te_interp = trn_info_dir['h_te_interp']
        h_te_std = trn_info_dir['h_te_std']
        h_te_uncertainty = trn_info_dir['h_te_uncertainty']
        terrain_slope = trn_info_dir['terrain_slope']
        h_te_best_fit = trn_info_dir['h_te_best_fit']
        # Canopy
        canopy_h_metrics_abs = cnpy_info_dir['canopy_h_metrics_abs']
        canopy_h_metrics = cnpy_info_dir['canopy_h_metrics']
        h_canopy_abs = cnpy_info_dir['h_canopy_abs']
        h_canopy = cnpy_info_dir['h_canopy']
        h_mean_canopy_abs = cnpy_info_dir['h_mean_canopy_abs']
        h_mean_canopy = cnpy_info_dir['h_mean_canopy']
        h_dif_canopy = cnpy_info_dir['h_dif_canopy']
        h_min_canopy_abs = cnpy_info_dir['h_min_canopy_abs']
        h_min_canopy = cnpy_info_dir['h_min_canopy']
        h_max_canopy_abs = cnpy_info_dir['h_max_canopy_abs']
        h_max_canopy = cnpy_info_dir['h_max_canopy']
        h_canopy_uncertainty = cnpy_info_dir['h_canopy_uncertainty']
        canopy_openness = cnpy_info_dir['canopy_openness']
        toc_roughness = cnpy_info_dir['toc_roughness']
        h_canopy_quad = cnpy_info_dir['h_canopy_quad']
        n_ca_photons = cnpy_info_dir['n_ca_photons']
        n_toc_photons = cnpy_info_dir['n_toc_photons']
        centroid_height = cnpy_info_dir['centroid_height']
        canopy_rh_conf = cnpy_info_dir['canopy_rh_conf']
        canopy_flag = cnpy_info_dir['canopy_flag']
        landsat_flag = cnpy_info_dir['landsat_flag']
        landsat_perc = cnpy_info_dir['landsat_perc']
        
        open_transaction = False
        n_feats = latitude.shape[0]
        for i in range(n_feats):
            if not open_transaction:
                out_lyr_obj.StartTransaction()
                open_transaction = True
            
            out_feat = ogr.Feature(feat_defn)
            pt = ogr.Geometry(ogr.wkbPoint)
            pt.AddPoint(float(longitude[i]), float(latitude[i]))
            out_feat.SetGeometry(pt)
            
            # General
            out_feat.SetField('segment_id', int(segment_id[i]))
            out_feat.SetField('segment_id_beg', int(segment_id_beg[i]))
            out_feat.SetField('segment_id_end', int(segment_id_end[i]))
            out_feat.SetField('latitude', float(latitude[i]))
            out_feat.SetField('longitude', float(longitude[i]))
            out_feat.SetField('solar_azimuth', float(solar_azimuth[i]))
            out_feat.SetField('solar_elevation', float(solar_elevation[i]))
            out_feat.SetField('delta_time', float(delta_time[i]))
            out_feat.SetField('delta_time_beg', float(delta_time_beg[i]))
            out_feat.SetField('delta_time_end', float(delta_time_end[i]))
            out_feat.SetField('night_flag', int(night_flag[i]))
            out_feat.SetField('dem_h', float(dem_h[i]))
            out_feat.SetField('dem_flag', int(dem_flag[i]))
            out_feat.SetField('dem_removal_flag', int(dem_removal_flag[i]))
            out_feat.SetField('h_dif_ref', float(h_dif_ref[i]))
            out_feat.SetField('terrain_flg', int(terrain_flg[i]))
            out_feat.SetField('segment_landcover', int(segment_landcover[i]))
            out_feat.SetField('segment_watermask', int(segment_watermask[i]))
            out_feat.SetField('segment_snowcover', int(segment_snowcover[i]))
            out_feat.SetField('urban_flag', int(urban_flag[i]))
            out_feat.SetField('cloud_flag_asr', int(cloud_flag_asr[i]))
            out_feat.SetField('snr', float(snr[i]))
            # Terrain
            out_feat.SetField('h_te_mean', float(h_te_mean[i]))
            out_feat.SetField('h_te_median', float(h_te_median[i]))
            out_feat.SetField('h_te_min', float(h_te_min[i]))
            out_feat.SetField('h_te_max', float(h_te_max[i]))
            out_feat.SetField('h_te_mode', float(h_te_mode[i]))
            out_feat.SetField('h_te_skew', float(h_te_skew[i]))
            out_feat.SetField('n_te_photons', int(n_te_photons[i]))
            out_feat.SetField('h_te_interp', float(h_te_interp[i]))
            out_feat.SetField('h_te_std', float(h_te_std[i]))
            out_feat.SetField('h_te_uncertainty', float(h_te_uncertainty[i]))
            out_feat.SetField('terrain_slope', float(terrain_slope[i]))
            out_feat.SetField('h_te_best_fit', float(h_te_best_fit[i]))
            # Canopy
            out_feat.SetField('canopy_h_metrics_abs_p25', float(canopy_h_metrics_abs[i][0]))
            out_feat.SetField('canopy_h_metrics_abs_p50', float(canopy_h_metrics_abs[i][1]))
            out_feat.SetField('canopy_h_metrics_abs_p60', float(canopy_h_metrics_abs[i][2]))
            out_feat.SetField('canopy_h_metrics_abs_p70', float(canopy_h_metrics_abs[i][3]))
            out_feat.SetField('canopy_h_metrics_abs_p75', float(canopy_h_metrics_abs[i][4]))
            out_feat.SetField('canopy_h_metrics_abs_p80', float(canopy_h_metrics_abs[i][5]))
            out_feat.SetField('canopy_h_metrics_abs_p85', float(canopy_h_metrics_abs[i][6]))
            out_feat.SetField('canopy_h_metrics_abs_p90', float(canopy_h_metrics_abs[i][7]))
            out_feat.SetField('canopy_h_metrics_abs_p95', float(canopy_h_metrics_abs[i][8]))
            out_feat.SetField('canopy_h_metrics_p25', float(canopy_h_metrics[i][0]))
            out_feat.SetField('canopy_h_metrics_p50', float(canopy_h_metrics[i][1]))
            out_feat.SetField('canopy_h_metrics_p60', float(canopy_h_metrics[i][2]))
            out_feat.SetField('canopy_h_metrics_p70', float(canopy_h_metrics[i][3]))
            out_feat.SetField('canopy_h_metrics_p75', float(canopy_h_metrics[i][4]))
            out_feat.SetField('canopy_h_metrics_p80', float(canopy_h_metrics[i][5]))
            out_feat.SetField('canopy_h_metrics_p85', float(canopy_h_metrics[i][6]))
            out_feat.SetField('canopy_h_metrics_p90', float(canopy_h_metrics[i][7]))
            out_feat.SetField('canopy_h_metrics_p95', float(canopy_h_metrics[i][8]))
            out_feat.SetField('h_canopy_abs', float(h_canopy_abs[i]))
            out_feat.SetField('h_canopy', float(h_canopy[i]))
            out_feat.SetField('h_mean_canopy_abs', float(h_mean_canopy_abs[i]))
            out_feat.SetField('h_mean_canopy', float(h_mean_canopy[i]))
            out_feat.SetField('h_dif_canopy', float(h_dif_canopy[i]))
            out_feat.SetField('h_min_canopy_abs', float(h_min_canopy_abs[i]))
            out_feat.SetField('h_min_canopy', float(h_min_canopy[i]))
            out_feat.SetField('h_max_canopy_abs', float(h_max_canopy_abs[i]))
            out_feat.SetField('h_max_canopy', float(h_max_canopy[i]))
            out_feat.SetField('h_canopy_uncertainty', float(h_canopy_uncertainty[i]))
            out_feat.SetField('canopy_openness', float(canopy_openness[i]))
            out_feat.SetField('toc_roughness', float(toc_roughness[i]))
            out_feat.SetField('h_canopy_quad', float(h_canopy_quad[i]))
            out_feat.SetField('n_ca_photons', int(n_ca_photons[i]))
            out_feat.SetField('n_toc_photons', int(n_toc_photons[i]))
            out_feat.SetField('centroid_height', float(centroid_height[i]))
            out_feat.SetField('canopy_rh_conf', int(canopy_rh_conf[i]))
            out_feat.SetField('canopy_flag', int(canopy_flag[i]))
            out_feat.SetField('landsat_flag', int(landsat_flag[i]))
            out_feat.SetField('landsat_perc', float(landsat_perc[i]))
            
                        
            out_lyr_obj.CreateFeature(out_feat)
            out_feat = None
            
            if ((i % 20000) == 0) and open_transaction:
                out_lyr_obj.CommitTransaction()
                open_transaction = False
        
        if open_transaction:
            out_lyr_obj.CommitTransaction()
            open_transaction = False
        out_lyr_obj.SyncToDisk()
    
    fH5 = None    
    vecDS = None
    




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--icesat", type=str, required=True, help="Input icesat2 ATL08 hdf5 file.")
    parser.add_argument("--vecfile", type=str, required=True, help="Specify an output vector file.")
    parser.add_argument("--veclyr", type=str, required=True, help="Specify the output vector layer.")
    parser.add_argument("--vecformat", type=str, required=False, default='GPKG', help="Specify an OGR file format (Default: GPKG).")
   
    args = parser.parse_args()
    
    exportATL08(args.icesat, args.vecfile, args.veclyr, args.vecformat)
    

