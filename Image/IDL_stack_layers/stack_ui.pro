PRO stack_ui

envi, /restore_base_save_files
envi_batch_init, log_file='batch.log'

layers = DIALOG_PICKFILE(/MULTIPLE_FILES, /MUST_EXIST)

out_name = DIALOG_PICKFILE()

layer_stack, layers, out_name

envi_batch_exit

END


