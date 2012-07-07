forward_function envi_get_projection

PRO casi2refl
;This file reads an input file and then outputs it again
;restore all base save files
envi,/restore_base_save_files
envi_batch_init,log_file='batch.log'

layer = DIALOG_PICKFILE(/MULTIPLE_FILES, /MUST_EXIST)

sizeinfo = size(layer)
print, "Number of sizeofinfo:", sizeinfo
numlayers = sizeinfo[1]
print, "Number of layers:", numlayers

for i=0, numlayers-1 do begin

   ENVI_OPEN_FILE, layer[i], r_fid=b_fid
   if(b_fid eq -1) then begin
      PRINT, "Could not open file"
      envi_batch_exit
      return
   endif

   ENVI_FILE_QUERY, b_fid, nb=b_nb, ns=b_ns, nl=b_nl

   PRINT, "b_ns=", b_ns
   PRINT, "b_nl=", b_nl
   PRINT, "b_nb=", b_nb

   print, "Got even further! :-)"

   dims = [-1,0,b_ns-1,0,b_nl-1]
   pos_out = lindgen(b_nb)

   outfile_path_name = STRSPLIT(layer[i],'.',/EXTRACT)

   PRINT, "start of file name: ", outfile_path_name[0]

   outfile_name = STRARR(2)
   outfile_name[0] = STRTRIM(outfile_path_name[0])
   outfile_name[1] = STRTRIM("_refl")

   out_name = (STRJOIN(outfile_name))

   solar_irr = [38902.511719, 42664.128906, 43025.082031, $
                41966.589844, 41960.304688, 40473.386719, $
                40065.277344, 37281.753906, 36510.746094, $
                34287.183594, 35954.015625, 35994.796875, $
 		32673.142578, 29632.125000]

   path_rad = [677.495972, 260.343628, 264.453949, 311.931030, $ 
               251.052765, 161.276718, 36.059589, 75.571289, $
               54.764339, 98.207367, 95.909966, 96.011337, $
               118.738258, 313.033386]

   envi_doit, 'eline_cal_doit', fid=b_fid, pos=pos_out, $
               dims=dims, path_rad=path_rad, solar_irr=solar_irr, $
               out_name=out_name, r_fid=r_fid

endfor

PRINT, "Got to end! :-D"

envi_batch_end

END
