rsgislibxml.py -i FindImageFootPrintsTemplate.xml -o FindImageFootPrint -p /home/pete.bunting/SarahImageFootprints/footprints -d /home/pete.bunting/SarahImageFootprints/tifs/ -e .tif -t multiple

python Submit2bsub.py -i FindImageFootPrint_exe_all.sh -o HPCSubmitFindImageFootPrint -m 1000 -t 0:30 -n HPCSubmitFindImageFootPrint

