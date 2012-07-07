g++ -I/Users/richard/Downloads/xerces-c-src_2_8_0/include -c main.cpp DefiniensRuleset.cpp DefiniensException.cpp
g++ -L/Users/richard/Downloads/xerces-c-src_2_8_0/lib/ -lxerces-c -o definienscolours main.o DefiniensRuleset.o DefiniensException.o

rm *.o

