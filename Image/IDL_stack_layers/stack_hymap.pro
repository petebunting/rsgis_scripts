PRO stack_hymap

envi, /restore_base_save_files
envi_batch_init, log_file='batch.log'

layers = [$
"b1.tif",$
"b2.tif",$
"b3.tif",$ 
"b4.tif",$ 
"b5.tif",$ 
"b6.tif",$ 
"b7.tif",$ 
"b8.tif",$ 
"b9.tif",$ 
"b10.tif",$ 
"b11.tif",$ 
"b12.tif",$ 
"b13.tif",$ 
"b14.tif",$
"b15.tif",$ 
"b16.tif",$ 
"b17.tif",$ 
"b18.tif",$ 
"b19.tif",$ 
"b20.tif"]
 
out_name = 'hymap_stack1'
layer_stack, layers, out_name

layers = [$
"b21.tif",$ 
"b22.tif",$ 
"b23.tif",$
"b24.tif",$ 
"b25.tif",$ 
"b26.tif",$ 
"b27.tif",$ 
"b28.tif",$ 
"b29.tif",$ 
"b30.tif",$ 
"b31.tif",$
"b32.tif",$ 
"b33.tif",$ 
"b34.tif",$ 
"b35.tif",$ 
"b36.tif",$ 
"b37.tif",$ 
"b38.tif",$ 
"b39.tif",$ 
"b40.tif"]

out_name = 'hymap_stack2'
layer_stack, layers, out_name

layers = [$
"b41.tif",$ 
"b42.tif",$ 
"b43.tif",$ 
"b44.tif",$ 
"b45.tif",$ 
"b46.tif",$ 
"b47.tif",$
"b48.tif",$ 
"b49.tif",$ 
"b50.tif",$ 
"b51.tif",$ 
"b52.tif",$ 
"b53.tif",$ 
"b54.tif",$ 
"b55.tif",$ 
"b56.tif",$ 
"b57.tif",$
"b58.tif",$ 
"b59.tif",$ 
"b60.tif"]
 
out_name = 'hymap_stack3'
layer_stack, layers, out_name

layers = [$
"b61.tif",$ 
"b62.tif",$ 
"b63.tif",$ 
"b64.tif",$
"b65.tif",$ 
"b66.tif",$ 
"b67.tif",$ 
"b68.tif",$ 
"b69.tif",$ 
"b70.tif",$ 
"b71.tif",$ 
"b72.tif",$ 
"b73.tif",$
"b74.tif",$ 
"b75.tif",$ 
"b76.tif",$ 
"b77.tif",$ 
"b78.tif",$ 
"b79.tif",$ 
"b80.tif"]

out_name = 'hymap_stack4'
layer_stack, layers, out_name

layers = [$
"b81.tif",$ 
"b82.tif",$ 
"b83.tif",$ 
"b84.tif",$ 
"b85.tif",$ 
"b86.tif",$ 
"b87.tif",$ 
"b88.tif",$ 
"b89.tif",$
"b90.tif",$ 
"b91.tif",$ 
"b92.tif",$ 
"b93.tif",$ 
"b94.tif",$ 
"b95.tif",$ 
"b96.tif",$
"b97.tif",$ 
"b98.tif",$ 
"b99.tif",$ 
"b100.tif"]
 
out_name = 'hymap_stack5'
layer_stack, layers, out_name

layers = [$
"b101.tif",$ 
"b102.tif",$ 
"b103.tif",$ 
"b104.tif",$ 
"b105.tif",$
"b106.tif",$ 
"b107.tif",$ 
"b108.tif",$ 
"b109.tif",$ 
"b110.tif",$ 
"b111.tif",$ 
"b112.tif",$ 
"b113.tif"]
 
out_name = 'hymap_stack6'
layer_stack, layers, out_name
layers = [$
"b114.tif",$
"b115.tif",$ 
"b116.tif",$ 
"b117.tif",$ 
"b118.tif",$ 
"b119.tif",$ 
"b120.tif",$
"b121.tif",$ 
"b122.tif",$ 
"b123.tif",$ 
"b124.tif",$ 
"b125.tif",$ 
"b126.tif"] 

out_name = 'hymap_stack7'
layer_stack, layers, out_name

layers = [$
"hymap_stack1",$
"hymap_stack2",$
"hymap_stack3",$
"hymap_stack4",$
"hymap_stack5",$
"hymap_stack6",$
"hymap_stack7"]

out_name = 'hymap_126bands'
layer_stack, layers, out_name

envi_batch_exit
END


