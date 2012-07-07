forward_function envi_get_projection

PRO layer_stack, layers, out_name
;This file reads an input file and then outputs it again
;restore all base save files
envi,/restore_base_save_files
envi_batch_init,log_file='batch.log'

;layers  = DIALOG_PICKFILE(/MULTIPLE_FILES, /MUST_EXIST)

print, layers
nb = 0;
sizeinfo = size(layers)
numlayers = sizeinfo[1]

print, "Number of layers:", numlayers

for i=0, numlayers-1  do begin

   ENVI_OPEN_FILE, layers[i], r_fid=b_fid
   if(b_fid eq -1) then begin
      PRINT, "Could not open file"
      envi_batch_exit
      return
   endif

   ENVI_FILE_QUERY, b_fid, nb=b_nb
   nb = nb + b_nb
endfor

print, "nb:", nb

fid = lonarr(nb)
pos = lonarr(nb)
dims = lonarr(5,nb)
count = 0
for i=0,numlayers-1 do begin

   ENVI_OPEN_FILE, layers[i], r_fid=b_fid
   if(b_fid eq -1) then begin
      envi_batch_exit
      return
   endif

   ENVI_FILE_QUERY, b_fid, ns=b_ns, nl=b_nl, nb=b_nb
  print, "bands=", b_nb
   if (b_nb eq 1) then begin
      pos[count] = 0;
      fid[count] = b_fid
      dims[0,count] = [-1,0,b_ns-1,0,b_nl-1]
      count = count +1
   ENDIF ELSE BEGIN
      FOR j=0, b_nb-1 DO BEGIN
         pos[count] = j;
         fid[count] = b_fid
         dims[0,count] = [-1,0,b_ns-1,0,b_nl-1]
         count = count+1
      ENDFOR
   ENDELSE
ENDFOR

print, "fid", fid
print, "Pos", pos
print, "dims", dims

out_proj = envi_get_projection(fid=b_fid, $
   pixel_size = out_ps)

;filename = DIALOG_PICKFILE()

;out_name = filename[0];

out_dt = 4

envi_doit, 'envi_layer_stacking_doit', $
  fid=fid, pos=pos, dims=dims, $
 out_dt=out_dt, out_name=out_name, $
  interp = 0, out_ps=out_ps, $
  out_proj=out_proj, r_fid=out_fid

END
