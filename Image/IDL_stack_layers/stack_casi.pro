PRO stack_casi

envi, /restore_base_save_files
envi_batch_init, log_file='batch.log'

filepath = "/Users/pete/Documents/PHD/data/injune/"

cont_loop = 1

WHILE (cont_loop EQ 1) DO BEGIN


filepath =  DIALOG_PICKFILE(/DIRECTORY, PATH=filepath)

IF filepath EQ "" THEN BEGIN
   cont_loop = 0
   PRINT, "Cancel"
   return;
ENDIF

PRINT, "filepath: ", filepath

b1_arr = STRARR(2)
b2_arr = STRARR(2)
b3_arr = STRARR(2)
b4_arr = STRARR(2)
b5_arr = STRARR(2)
b6_arr = STRARR(2)
b7_arr = STRARR(2)
b8_arr = STRARR(2)
b9_arr = STRARR(2)
b10_arr = STRARR(2)
b11_arr = STRARR(2)
b12_arr = STRARR(2)
b13_arr = STRARR(2)
b14_arr = STRARR(2)

b1_arr[0] = filepath
b2_arr[0] = filepath
b3_arr[0] = filepath
b4_arr[0] = filepath
b5_arr[0] = filepath
b6_arr[0] = filepath
b7_arr[0] = filepath
b8_arr[0] = filepath
b9_arr[0] = filepath
b10_arr[0] = filepath
b11_arr[0] = filepath
b12_arr[0] = filepath
b13_arr[0] = filepath
b14_arr[0] = filepath

b1_arr[1] = STRTRIM("b1.tif")
b2_arr[1] = STRTRIM("b2.tif")
b3_arr[1] = STRTRIM("b3.tif")
b4_arr[1] = STRTRIM("b4.tif")
b5_arr[1] = STRTRIM("b5.tif")
b6_arr[1] = STRTRIM("b6.tif")
b7_arr[1] = STRTRIM("b7.tif")
b8_arr[1] = STRTRIM("b8.tif")
b9_arr[1] = STRTRIM("b9.tif")
b10_arr[1] = STRTRIM("b10.tif")
b11_arr[1] = STRTRIM("b11.tif")
b12_arr[1] = STRTRIM("b12.tif")
b13_arr[1] = STRTRIM("b13.tif")
b14_arr[1] = STRTRIM("b14.tif")

layer = STRARR(14)

layer[0] = (STRJOIN(b1_arr))
layer[1] = (STRJOIN(b2_arr))
layer[2] = (STRJOIN(b3_arr))
layer[3] = (STRJOIN(b4_arr))
layer[4] = (STRJOIN(b5_arr))
layer[5] = (STRJOIN(b6_arr))
layer[6] = (STRJOIN(b7_arr))
layer[7] = (STRJOIN(b8_arr))
layer[8] = (STRJOIN(b9_arr))
layer[9] = (STRJOIN(b10_arr))
layer[10] = (STRJOIN(b11_arr))
layer[11] = (STRJOIN(b12_arr))
layer[12] = (STRJOIN(b13_arr))
layer[13] = (STRJOIN(b14_arr))


out_name = DIALOG_PICKFILE(/WRITE, TITLE='OUPUT IMAGE', PATH=filepath)

IF out_name EQ "" THEN BEGIN
   cont_loop = 0
   PRINT, "Cancel"
   return;
ENDIF

PRINT, "out_name: ", out_name

layer_stack, layer, out_name

ENDWHILE

END


