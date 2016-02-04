
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

unsigned int get_file_size(char* filename) {
    FILE *fp;
    fp = fopen(filename, "r");

    if (fp == NULL) {
        printf("Error: Cannot open %s\n", filename);
        fclose(fp);
        return -1;
    }

    struct stat buf;
    stat(filename, &buf);
    return buf.st_size;
}

void load_image(char * filename, unsigned int** buffer, int filesize) {
    FILE *fp;
    fp = fopen(filename, "r");

    if (fp == NULL) {
        printf("Error: MiasFormat, Cannot open %s\n", filename);
        fclose(fp);
        return;
    }



    int xn = 4320, yn;
    switch (filesize) {
        case (1600 * 4320): { yn = 1600; break; }
        case (2048 * 4320): { yn = 2048; break; }
        case (2600 * 4320): { yn = 2600; break; }
        case (5200 * 4000): { yn = 4000; xn = 5200; break; }

        default: {
            printf("Error: MiasFormat, incorrect file size %s\n", filename);
            fclose(fp);
            return;
        }
    }

    printf("%d, %d\n", xn, yn);

    // load file info a tempory image initially
    // as the images are not arranged for vertical
    // left/right breast display
    // this is faster than loading the file byte
    // by byte into the correct image positions
    *buffer = (unsigned int *) malloc(filesize*sizeof(unsigned int));
    fread(*buffer, sizeof(*buffer), filesize, fp);
    fclose(fp);
}

int main() {
    unsigned int *buffer;
    unsigned int size = get_file_size("./mdb001lm");
    load_image("./mdb001lm", &buffer, size);
    printf("File size is: %d\n", size);
    printf("Done.\n");
    free(buffer);
    return 0;
}
