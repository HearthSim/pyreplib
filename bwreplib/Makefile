CPP = g++
AR = ar
HEADERS = /usr/include/bwrep
CP = cp
RM = rm

all: libbwrep.a

bwrepactions.o: 
	$(CPP) bwrepactions.cpp -O2 -o bwrepactions.o -c 

bwrepapi.o: 
	$(CPP) bwrepapi.cpp -O2 -o bwrepapi.o -c 

bwrepgamedata.o: 
	$(CPP) bwrepgamedata.cpp -O2 -o bwrepgamedata.o -c

bwrepmap.o: 
	$(CPP) bwrepmap.cpp -O2 -o bwrepmap.o -c
    
stdafx.o:
	$(CPP) stdafx.cpp -O2 -o stdafx.o -c
    
unpack.o:
	$(CPP) unpack.cpp -O2 -o unpack.o -c

libbwrep.a: unpack.o stdafx.o bwrepmap.o bwrepgamedata.o bwrepapi.o bwrepactions.o
	$(AR) cr libbwrep.a bwrepmap.o bwrepgamedata.o stdafx.o unpack.o bwrepapi.o bwrepactions.o

install:
	@md $(HEADERS)
	$(CP) *.h $(HEADERS)
	
clean:
	$(RM) *.o *.a