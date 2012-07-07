forward_function envi_get_projection

PRO casi_multi1000
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
   outfile_name[1] = STRTRIM("_1000")

   out_name = (STRJOIN(outfile_name))

   PRINT, "FILE: ", out_name

   math_expression = "float(b1*1000)"

   r_fids = lonarr(b_nb)
   pos_out = lonarr(b_nb)
   dims_out = lonarr(5, b_nb)
   pos_out_math = lonarr(1)

   for j=0, b_nb-1 do begin
      pos_out_math[0] = j;
      PRINT, "Performing Calc on each band: ", j
      envi_doit, 'math_doit', fid=b_fid, pos=pos_out_math, $
                  dims=dims, exp=math_expression, $
                  /IN_MEMORY, r_fid=r_fid
      PRINT, "r_fid: ", r_fid
      r_fids[j] = r_fid
      pos_out[j] = 0
      dims_out[0, j] = [-1,0,b_ns-1,0,b_nl-1]
   endfor
   PRINT, "Now going to stack the bands to create the new Image"
   out_proj = envi_get_projection(fid=b_fid, pixel_size = out_ps)
   out_dt = 4

   for j=0, b_nb-1 do begin
   PRINT, "j = ", j
   PRINT, "fid = ", r_fids[j]
   ;PRINT, "pos_out = ", pos_out[j]
   ;PRINT, "dims_out = [", dims_out[0, j], ",",  dims_out[1, j], ",", dims_out[2,j], ",", dims_out[3,j], ",", dims_out[4,j], "]"
   endfor

   envi_doit, 'envi_layer_stacking_doit', fid=r_fids, pos=pos_out,$
               dims=dims_out, out_dt=out_dt, out_name = out_name, $
               interp = 0, out_ps = out_ps, out_proj = out_proj, $
               r_fid = r_fid_out
endfor

PRINT, "Got to end! :-D"

END
