forward_function envi_get_projection

PRO casi_nor_hsv
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

   outfile_path_name = STRSPLIT(layer[i],'.',/EXTRACT)

   outfile_name = STRARR(2)
   outfile_name[0] = STRTRIM(outfile_path_name[0])
   outfile_name[1] = STRTRIM("_hsv_stretched")

   out_name = (STRJOIN(outfile_name))

   PRINT, "FILE: ", out_name

   ;Create Stretched Image for CASI bands 1-14 and save in Memory
   pos_out = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]

   envi_doit, 'stretch_doit', fid=b_fid, $
               pos=pos_out, dims=dims, method=2,$
               /IN_MEMORY, i_min=0, i_max=100, $
               range_by=0, out_min=0, out_max=255,$
                out_dt=1, r_fid=stretch_fid


   ; Create HSV Image for bands 14, 9, 1 and Save in Memory
   fids = [stretch_fid, stretch_fid, stretch_fid]
   dims = [-1, 0, b_ns-1, 0, b_nl-1]
   pos_out = [13, 8, 0]

   envi_doit, 'rgb_trans_doit', fid=fids,$
               pos=pos_out, dims=dims, hsv=0,$
               /IN_MEMORY, r_fid=hsv_fid

PRINT, "Now going to stack the bands to create the new Image"

   fids = lonarr(b_nb+17)
   pos_out = lonarr(b_nb+17)
   dims_out = lonarr(5, b_nb+17)
   count = 0
      
   ; Input Image
   FOR j=0, b_nb-1 DO BEGIN
       pos_out[count] = j
       fids[count] = b_fid
       dims_out[0, count] = [-1,0,b_ns-1,0,b_nl-1]
       count = count + 1
   ENDFOR
   ; HSV Image
   FOR j=0, 2 DO BEGIN
       pos_out[count] = j
       fids[count] = hsv_fid
       dims_out[0, count] = [-1,0,b_ns-1,0,b_nl-1]
       count = count + 1
   ENDFOR
   ; Stretched Image
   FOR j=0, 13 DO BEGIN
       pos_out[count] = j
       fids[count] = stretch_fid
       dims_out[0, count] = [-1,0,b_ns-1,0,b_nl-1]
       count = count + 1
   ENDFOR
   
   out_proj = envi_get_projection(fid=b_fid, pixel_size = out_ps)
   out_dt = 4

   for j=0, b_nb+16 do begin
   PRINT, "j = ", j
   PRINT, "fid = ", fids[j]
   ;PRINT, "pos_out = ", pos_out[j]
   ;PRINT, "dims_out = [", dims_out[0, j], ",",  dims_out[1, j], ",", dims_out[2,j], ",", dims_out[3,j], ",", dims_out[4,j], "]"
   endfor

   envi_doit, 'envi_layer_stacking_doit', fid=fids, pos=pos_out,$
               dims=dims_out, out_dt=out_dt, out_name = out_name, $
               interp = 0, out_ps = out_ps, out_proj = out_proj, $
               r_fid = r_fid_out
endfor

PRINT, "Got to end! :-D"

END
