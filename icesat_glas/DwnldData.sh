#echo "machine urs.earthdata.nasa.gov login petebunting password #########" >> ~/.netrc
#chmod 0600 ~/.netrc


wget --load-cookies urs_cookies --save-cookies urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off https://n5eil01u.ecs.nsidc.org/GLAS/GLAH14.034

#rm ~/.netrc
