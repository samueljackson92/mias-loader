
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

typedef struct ImgShape {
    unsigned int width, height;
} ImgShape;

ImgShape get_file_size(char* filename) {
    ImgShape shape;
    shape.width = 0;
    shape.height = 0;

    FILE *fp;
    fp = fopen(filename, "r");

    if (fp == NULL) {
        printf("Error: Cannot open %s\n", filename);
        fclose(fp);
        return shape;
    }

    struct stat buf;
    stat(filename, &buf);
    int filesize=buf.st_size;

    shape.height = 4320;
    switch (filesize) {
        case (1600 * 4320): { shape.width = 1600; break; }
        case (2048 * 4320): { shape.width = 2048; break; }
        case (2600 * 4320): { shape.width = 2600; break; }
        case (5200 * 4000): { shape.width = 4000; shape.height = 5200; break; }

        default: {
            printf("Error: incorrect file size %s\n", filename);
            fclose(fp);
            shape.height = 0;
            shape.width = 0;
            return shape;
        }
    }

    return shape;
}

void load_image(char * filename, unsigned int** buffer, int filesize) {
    FILE *fp;
    fp = fopen(filename, "r");

    if (fp == NULL) {
        printf("Error: MiasFormat, Cannot open %s\n", filename);
        fclose(fp);
        return;
    }
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
    ImgShape size = get_file_size("./mdb001lm");
    load_image("./mdb001lm", &buffer, size.height*size.width);
    printf("File size is: %d, %d\n", size.height, size.width);
    printf("Done.\n");
    free(buffer);
    return 0;
}
