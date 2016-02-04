
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

typedef struct ImgShape {
    unsigned int width, height, size;
} ImgShape;

/*
    Get the size of the image to load as struct with members height and width.
*/
ImgShape get_file_size(char* filename) {
    ImgShape shape;
    shape.width = 0;
    shape.height = 0;

    //get file pointer and check it's valid
    FILE *fp;
    fp = fopen(filename, "r");

    if (fp == NULL) {
        printf("Error: Cannot open %s\n", filename);
        fclose(fp);
        return shape;
    }

    // get info from file
    struct stat buf;
    stat(filename, &buf);
    long long filesize=buf.st_size;

    // find the size of the image
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

    shape.size = shape.width * shape.height;
    return shape;
}

/*
    Load the image into an array of unsigned ints
*/
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
