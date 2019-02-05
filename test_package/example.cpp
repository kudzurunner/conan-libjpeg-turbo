#include <iostream>
#include <string>
#include <jpeglib.h>
#include <jconfigint.h>

int error_code = 0;
void jpeg_error_exit(j_common_ptr jcp) {
    std::cout << "libjpeg: " << jcp->err->jpeg_message_table[jcp->err->last_jpeg_message] << std::endl;
    error_code = 1;
}

int main() {
    std::cout << "libjpeg-turbo version: " << VERSION << std::endl;

    struct jpeg_error_mgr jerr;
    jpeg_std_error(&jerr);
    jerr.error_exit = jpeg_error_exit;

    struct jpeg_compress_struct jcs;
    jcs.err = &jerr;
    jpeg_create_compress(&jcs);

    struct jpeg_decompress_struct jds;
    jds.err = &jerr;
    jpeg_create_decompress(&jds);
    return error_code;
}
