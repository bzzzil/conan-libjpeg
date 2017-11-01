[![Build Status](https://travis-ci.org/bzzzil/conan-libjpeg.svg)](https://travis-ci.org/bzzzil/conan-libjpeg)

conan-libjpeg
=============

[Conan.io](https://conan.io) package for JPEG library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/libjpeg/8.3/bzzzil/stable).

Build packages
--------------

Download conan client from [Conan.io](https://conan.io) and run:

```
$ pip install conan_package_tools
$ python build.py
```

Upload packages to server
-------------------------

```
$ conan upload libjpeg/8.3@bzzzil/stable --all
```

Reuse the packages
------------------

### Basic setup

```
$ conan install libjpeg/8.3@bzzzil/stable
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

```
[requires]
libjpeg/8.3@bzzzil/stable

[options]
libjpeg:shared=true # false

[generators]
txt
cmake
```

Complete the installation of requirements for your project running:</small></span>

```
conan install .
```

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
