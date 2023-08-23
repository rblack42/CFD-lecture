SRCS = $(wildcard f90/*.f90)
OBJS = $(SRCS:.f=.o)
OBJS += f77/clear.o
FOPTS = --std=f2018 -ffpe-trap=invalid,zero
FC = gfortran


all: $(OBJS)
	$(FC) $(FOPTS) -o rrbaxi $^

%.o:	%.f
	$(FC) $(FOPTS) -c -o $@ $<

clean:
	rm -f f90/.o rrbaxi
