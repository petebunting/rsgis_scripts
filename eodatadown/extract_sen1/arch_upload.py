import glob
import os
from ftplib import FTP

scn_list = [
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191230T063117_20191230T063142_030574_038084_3524-GRD_HD_4277",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191218T063117_20191218T063142_030399_037A83_95C5-GRD_HD_4230",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191206T063118_20191206T063143_030224_037476_8CC7-GRD_HD_4179",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191124T063118_20191124T063143_030049_036E66_30F8-GRD_HD_4161",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191031T063119_20191031T063144_029699_036235_1EA1-GRD_HD_4034",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191019T063119_20191019T063144_029524_035C20_FBCD-GRD_HD_4071",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20191007T063119_20191007T063144_029349_03561B_2D50-GRD_HD_4108",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190925T063118_20190925T063143_029174_035008_007F-GRD_HD_4145",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190913T063118_20190913T063143_028999_034A13_C257-GRD_HD_2810",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190901T063117_20190901T063142_028824_034401_BA52-GRD_HD_38",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190820T063117_20190820T063142_028649_033DE6_C76B-GRD_HD_2891",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190808T063116_20190808T063141_028474_0337D6_5C2B-GRD_HD_90",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190727T063115_20190727T063140_028299_03327A_574F-GRD_HD_2970",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190715T063114_20190715T063139_028124_032D23_491D-GRD_HD_139",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190703T063114_20190703T063139_027949_0327D7_7718-GRD_HD_162",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190621T063113_20190621T063138_027774_032290_3B28-GRD_HD_187",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190609T063112_20190609T063137_027599_031D5A_5205-GRD_HD_213",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190528T063112_20190528T063137_027424_0317F6_9445-GRD_HD_3156",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190516T063111_20190516T063136_027249_031280_751B-GRD_HD_3182",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190504T063111_20190504T063136_027074_030CD8_D6C2-GRD_HD_3212",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190422T063110_20190422T063135_026899_030676_4B23-GRD_HD_309",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190410T063109_20190410T063134_026724_03002A_58C4-GRD_HD_336",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190329T063109_20190329T063134_026549_02F9B7_375F-GRD_HD_361",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190317T063109_20190317T063134_026374_02F34C_C990-GRD_HD_385",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190305T063109_20190305T063134_026199_02ECD9_F086-GRD_HD_408",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190221T063109_20190221T063134_026024_02E692_D621-GRD_HD_3361",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190209T063109_20190209T063134_025849_02E060_6528-GRD_HD_454",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190128T063110_20190128T063135_025674_02DA10_4F3D-GRD_HD_477",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20190116T063110_20190116T063135_025499_02D3AC_E6CD-GRD_HD_504",
"/bigdata/eodd_wales_ard/data/sen1asf/ard/S1A_IW_GRDH_1SDV_20181223T063111_20181223T063136_025149_02C70A_F4C3-GRD_HD_550"]

ftp_ses = FTP('144.124.80.198', user='eogroup', passwd='aberdata')
ftp_ses.cwd('/PeteBunting/StevanHowe')
for scn in scn_list:
    img_file = glob.glob(os.path.join(scn, "*_dB_osgb.tif"))
    if len(img_file) == 1:
        img_file = img_file[0]
    else:
        raise Exception("Could not find a single file within directory: {}".format(scn))
    print(img_file)
    img_basename = os.path.basename(img_file)
    with open(img_file, 'rb') as fp:
        ftp_ses.storbinary('STOR {}'.format(img_basename), fp)     # send the file
ftp_ses.quit()
    
    