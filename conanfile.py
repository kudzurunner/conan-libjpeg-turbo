from conans import ConanFile, CMake, tools
import os


class LibjpegturboConan(ConanFile):
    name = "libjpeg-turbo"
    version = "2.0.3"
    license = "https://raw.githubusercontent.com/libjpeg-turbo/libjpeg-turbo/master/LICENSE.md"
    author = "KudzuRunner"
    url = "https://github.com/kudzurunner/conan-libjpeg-turbo"
    description = "libjpeg-turbo is a JPEG image codec that uses SIMD instructions to accelerate baseline JPEG " \
                  "compression and decompression "
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "require_simd": [True, False],
        "with_12bit": [True, False],
        "with_arith_dec": [True, False],
        "with_arith_enc": [True, False],
        "with_java": [True, False],
        "with_jpeg7": [True, False],
        "with_jpeg8": [True, False],
        "with_mem_srcdst": [True, False],
        "with_simd": [True, False],
        "with_turbojpeg": [True, False]
    }
    default_options = {
        "shared": True,
        "require_simd": False,
        "with_12bit": False,
        "with_arith_dec": True,
        "with_arith_enc": True,
        "with_java": False,
        "with_jpeg7": False,
        "with_jpeg8": True,
        "with_mem_srcdst": True,
        "with_simd": True,
        "with_turbojpeg": True
    }
    generators = "cmake"
    source_name = "{}-{}".format(name, version)

    exports = (
        "patches/*.patch")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows":
            self.requires("nasm/2.14")

    def source(self):
        archive_name = "{}.tar.gz".format(self.version)
        url = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/{}".format(archive_name)

        tools.download(url, filename=archive_name)
        tools.untargz(filename=archive_name)
        os.remove(archive_name)

        tools.patch(base_path=self.source_name, patch_file="patches/install.patch", strip=1)

        tools.replace_in_file(
            "{}/CMakeLists.txt".format(self.source_name), "project(libjpeg-turbo C)",
            '''project(libjpeg-turbo C)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()'''
        )

    def build(self):
        cmake = CMake(self)
        cmake.definitions['ENABLE_SHARED'] = self.options.shared
        cmake.definitions['ENABLE_STATIC'] = not self.options.shared
        cmake.definitions['REQUIRE_SIMD'] = self.options.require_simd
        cmake.definitions['WITH_12BIT'] = self.options.with_12bit
        cmake.definitions['WITH_ARITH_DEC'] = self.options.with_arith_dec
        cmake.definitions['WITH_ARITH_ENC'] = self.options.with_arith_enc
        cmake.definitions['WITH_JAVA'] = self.options.with_java
        cmake.definitions['WITH_JPEG7'] = self.options.with_jpeg7
        cmake.definitions['WITH_JPEG8'] = self.options.with_jpeg8
        cmake.definitions['WITH_MEM_SRCDST'] = self.options.with_mem_srcdst
        cmake.definitions['WITH_SIMD'] = self.options.with_simd
        cmake.definitions['WITH_TURBOJPEG'] = self.options.with_turbojpeg
        cmake.configure(source_folder=self.source_name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="include", keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy("jconfig.h", dst="include", src=".")
            self.copy("jconfigint.h", dst="include", src=".")

        self.copy("license*", src=self.source_name, dst="licenses", ignore_case=True, keep_path=False)

        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['jpeg', 'turbojpeg'] if self.settings.os == "Windows" and self.options.shared else [
            'jpeg-static', 'turbojpeg-static']
