g++ -I/usr/local/include -c main.cpp ImageUtils.cpp 
g++ -L/usr/local/lib -lgdal -o rasterize main.o ImageUtils.o

rm *.o

