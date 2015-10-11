#!/usr/bin/env python
"""
A script to download Landsat scenes from
Google using gutil, which can be downloaded from:

https://cloud.google.com/storage/docs/gsutil

Takes CSV file with scene names as input.

These can be exported from EarthExplorer

Author: Dan Clewley
Creation Date: 10/10/2015

"""
from __future__ import print_function
import argparse
import os
import subprocess

#: Download link for list of scenes
GOOGLE_SCENELIST_LINK = 'gs://earthengine-public/landsat/scene_list.zip'

#: Path to gsutil script
try:
    GSUTIL_PATH = os.environ['GSUTIL_PATH']
except KeyError:
    GSUTIL_PATH = 'gsutil'

def download_google_scenelist(out_scene_list_dir):
	"""
	Download list of landsat files from Google server
	and unzips.
	"""
	subprocess.check_call([GSUTIL_PATH,'cp',GOOGLE_SCENELIST_LINK,out_scene_list_dir])
	current_dir = os.path.abspath(os.curdir)
	os.chdir(out_scene_list_dir)
	subprocess.check_call(['unzip','scene_list.zip'])
	os.chdir(current_dir)

	return os.path.join(out_scene_list_dir, 'scene_list')

def grep_for_scene(scenename, scenelist):
	"""
	Search for a scene within the list of all available
	scenes on Google server using grep.

	As searching a large text file grep is probably faster
	"""
	try:
		out_path = subprocess.check_output(['grep',scenename,scenelist])
	except subprocess.CalledProcessError:
		return None

	out_path = out_path.decode().strip()
	return out_path

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''A script to download
	Landsat scenes from Google's server using gsutil. To search for scenes
	use http://earthexplorer.usgs.gov and export the search as a CSV file''')
	parser.add_argument('csv', nargs=1, 
					help='''CSV file containing scenenames 
							in first column. 
							Assumed to have header row''')
	parser.add_argument('--scenelist',
						required=False,
						default=None,
						help='''List of scenes and location on Google servers.
								Provide a directory to download''')
	parser.add_argument('-o','--outdir',
						required=False,
						default=None,
						help='''Output directory to download scenes to.
								If not provided will just print path''')
	args = parser.parse_args()
	
	if not os.path.isfile(args.scenelist):
		if os.path.isdir(args.scenelist):
			google_scenelist = download_google_scenelist(args.scenelist)
		else:
			print('Must provide scenelist or directory to download to',file=sys.stderr)
			sys.exit(1)
	else:
		google_scenelist = args.scenelist
		
	# Open CSV file.
	# USGS uses degrees symbol (non-unicode) in their CSV files
	# which causes problems.
	# setting the encoding to latin-1 fixes this.
	csv_data = open(args.csv[0],'rU',encoding="latin-1")
	
	# skip header
	next(csv_data)
	
	for line in csv_data:
		# Take scene name from first column.
		elements = line.split(',')
		scene = elements[0]
		# Check if scene is in list of Google links.
		scene_path = grep_for_scene(scene, google_scenelist)

		if scene_path is None:
			print('Could not find "{}"'.format(scene))
		# If an output directory is provided download
		# the scene.
		elif args.outdir is not None:
			subprocess.check_call([GSUTIL_PATH, 'cp', scene_path, 
								   os.path.abspath(args.outdir)])
		else:
			print(scene_path)

