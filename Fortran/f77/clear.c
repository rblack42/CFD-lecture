#include <stdlib.h>
#include <stdio.h>
int system(const char *command);

void clear_() {
	fflush(stdout);
	system("clear");
}
