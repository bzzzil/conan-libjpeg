import platform
from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name="libjpeg:shared", pure_c=True)
#    new_builds = []
#    for settings, options, env_vars, build_requires in builder.builds:
#        if settings["arch"] == "x86" or settings["compiler.version"] != "5.4":
#            continue
#        new_builds.append((settings, options, env_vars, build_requires))
#    builder.builds = new_builds
    builder.run()
