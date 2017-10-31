import os

from conans import ConanFile, CMake, AutoToolsBuildEnvironment
from conans.client import tools
from conans.util import files

class libjpegConan(ConanFile):
    name = "libjpeg"
    version = "8.3"
    LIBJPEG_FOLDER_NAME = "jpeg-8c"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    license = "Open source: http://www.libpng.org/pub/png/src/libpng-LICENSE.txt"
    exports = "CMakeLists.txt", "libjpeg/*"
    url="http://github.com/bzzzil/conan-libjpeg"

    def requirements(self):
        self.requires.add("zlib/1.2.8@lasote/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx

    def remove_crlf(self, filename):
        with tools.chdir(self.LIBJPEG_FOLDER_NAME):
            self.run("mv ./%s ./%s_win" % (filename, filename))
            self.run("tr -d '\015' <./%s_win >./%s" % (filename, filename))
            os.unlink("./%s_win" % filename)

    def source(self):
        src_name = "jpegsr8c.zip"
        tools.download("http://ijg.org/files/%s" % src_name, src_name)
        tools.unzip(src_name)
        os.unlink(src_name)
        if self.settings.os != "Windows":
            for filename in ["configure", "aclocal.m4", "configure.ac", "Makefile.am", "config.sub", "ltmain.sh", "Makefile.in", "depcomp", "config.guess", "missing"]:
                self.remove_crlf(filename)
            self.run("chmod +x ./%s/configure" % self.LIBJPEG_FOLDER_NAME)

    def build(self):
        with tools.chdir(self.LIBJPEG_FOLDER_NAME):
            if not tools.OSInfo().is_windows:
                env_build = AutoToolsBuildEnvironment(self)
                env_build.fpic = True
                if self.settings.os == "Macos":
                    old_str = '-install_name $libdir/$SHAREDLIBM'
                    new_str = '-install_name $SHAREDLIBM'
                    tools.replace_in_file("./configure", old_str, new_str)

                env_build.configure("./", build=False, host=False, target=False)
                env_build.make()
            else:
                files.mkdir("_build")
                with tools.chdir("_build"):
                    cmake = CMake(self)
                    cmake.configure(build_dir=".")
                    cmake.build(build_dir=".")

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copying libjpeg.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.LIBJPEG_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            self.copy(pattern="libjpegd.lib", dst="lib", src="build/lib", keep_path=False)
            self.copy(pattern="libjpeg.lib", dst="lib", src="build/lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s/.libs" % self.LIBJPEG_FOLDER_NAME, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ['libjpegd']
            else:
                self.cpp_info.libs = ['libjpeg']
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ['jpegd']
            else:
                self.cpp_info.libs = ['jpeg']
