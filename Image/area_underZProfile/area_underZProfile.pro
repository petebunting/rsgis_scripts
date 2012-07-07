forward_function ENVI_GET_PROJECTION		

PRO  area_underZProfile

	ENVI, /RESTORE_BASE_SAVE_FILES
	ENVI_BATCH_INIT, log_file = 'batch.log'

	filepath = "/Users/pete/Documents/PHD/data/injune/"

	bands = DIALOG_PICKFILE(/READ, /MUST_EXIST, PATH=filepath, GET_PATH=filepath)
	ENVI_OPEN_FILE, bands[0], r_fid = b_fid
	IF(b_fid EQ -1) THEN BEGIN
		ENVI_BATCH_EXIT
		RETURN
	ENDIF

	PRINT, "Current PATH: ", filepath
	
	ENVI_FILE_QUERY, b_fid, ns = b_ns, nl = b_nl, $
                         nb = b_nb, bname = b_name, $
                         wl = b_wl, interleave=interleave

	b_dims = [-1, 0, b_ns-1, 0, b_nl-1]
	b_pos = lonarr(b_nb)
	
	result = FLTARR(b_ns, b_nl)

	size_result = size(result)

	PRINT, "size_result: ", size_result
	PRINT, "b_wl: ", b_wl
	
	FOR i=0, b_nb-1 DO BEGIN
		b_pos[i] = i	
	ENDFOR

	tile_id = ENVI_INIT_TILE(b_fid, b_pos, $
				NUM_TILES=num_tiles, interleave=(interleave >1), $
				XS=b_dims[1], XE=b_dims[2], YS=b_dims[3], YE=b_dims[4]) 

	PRINT, "NUM_TILES: ", num_tiles

	FOR i=0L, num_tiles-1 DO BEGIN
		data = ENVI_GET_TILE(tile_id, i)
		data_size = size(data)
		
		IF(data_size[0] EQ 1) THEN BEGIN
			data_samples = data_size[1]
			data_bands = 1
			data_pixels = data_size[3]
		ENDIF ELSE BEGIN
			data_samples = data_size[1]
			data_bands = data_size[2]
			data_pixels = data_size[4]
		ENDELSE

		area = FLTARR(data_bands-1)	
		FOR j=0L, data_samples-1 DO BEGIN
			FOR k=0L, data_bands-2 DO BEGIN
				wl_diff = float(b_wl[k+1]) - float(b_wl[k])
				IF(data[j, k] EQ data[j, k+1]) THEN BEGIN
					area[k] = float(data[j, k]) * float(wl_diff)
				ENDIF ELSE BEGIN
					IF(data[j, k] GT data[j, k+1]) THEN BEGIN
						maxHeight = float(data[j, k])
						minHeight = float(data[j, k+1])
					ENDIF ELSE BEGIN
						maxHeight = float(data[j, k+1])
						minHeight = float(data[j, k])
					ENDElSE
					triHeight = float(maxHeight) - float(minHeight)
					mainArea = float(minHeight) * float(b_wl[k])
					triArea = float(triHeight) * float(b_wl[k])
					
					area[k] =  float(mainArea) + float(triArea)
				ENDELSE
			ENDFOR
			overallArea = float(0)
			FOR m=0L, data_bands-2 DO BEGIN
				overallArea = float(overallArea) +float(area[m])
			ENDFOR
			result[j,i] = overallArea	
		ENDFOR
	ENDFOR
	ENVI_TILE_DONE, tile_id

	out = BYTSCL(result)

	data_type = 4
	out_proj = ENVI_GET_PROJECTION(fid=b_fid, pixel_size = out_ps)
	out_name = DIALOG_PICKFILE(/WRITE, TITLE='FLOAT OUTPUT', PATH=filepath, GET_PATH=filepath)
	map_info = ENVI_GET_MAP_INFO(fid=b_fid)
	
	PRINT, "MAP_INFO: ", map_info
	
	ENVI_WRITE_ENVI_FILE, result, out_dt=data_type, out_name=out_name, map_info=map_info,  pixel_size=out_ps

	data_type = 1
	out_name = DIALOG_PICKFILE(/WRITE, TITLE='BYTE OUTPUT', PATH=filepath)

	ENVI_WRITE_ENVI_FILE, out, out_dt=data_type, out_name=out_name, map_info=map_info, pixel_size=out_ps

END
