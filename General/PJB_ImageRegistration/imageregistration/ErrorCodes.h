/*
 *  ErrorCodes.h
 *  ImageRegistration
 *
 *  Created by Peter Bunting on 30/11/2005.
 *  Copyright 2005 Peter Bunting, University of Wales, Aberystwyth. All rights reserved.
 *
 */

#ifndef error_codes_H
#define error_codes_H

namespace error_codes
{
	enum
	{
		reference_image = 100,
		floating_image = 101,
		other_image = 102,
	
		insufficent_num_bands = 200,
		no_projection = 201,
		different_pixel_resolution = 202,
		difference_rotation = 203,
		no_image_overlap = 204,
		interpolation_grid_error = 205,
		xy_resolutions_different = 206,
	
		no_driver = 300,
		unsupported_format = 301,
	
		root_already_set = 400,
		root_not_set = 401,
		outside_of_area = 402,
		insufficient_levels = 403,
	
		empty_queue = 500,
		
		passed_null_pointer = 600,
		
		cannot_create_output_file = 700,
		
		cannot_find_place4node = 800,
		
		node_distances_not_found = 900,
		too_many_nodes_x_axis = 901,
		too_many_nodes_y_axis = 902,
		no_nodes_for_level = 903
	};
}

#endif
