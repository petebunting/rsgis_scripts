forward_function envi_get_projection

PRO convert2tiff
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
   outfile_name[1] = STRTRIM("_tif.tif")

   out_name = (STRJOIN(outfile_name))

   PRINT, out_name

   ENVI_OUTPUT_TO_EXTERNAL_FORMAT, dims=dims, fid=b_fid, out_name=out_name, pos=pos_out, /TIFF

endfor

PRINT, "Got to end! :-D"

END
