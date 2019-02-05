from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="kudzurunner")
    builder.add(settings={"arch": "x86_64", "build_type": "Release", "compiler": "Visual Studio", "compiler.version": 15, "compiler.runtime": "MD"},
                options={}, env_vars={}, build_requires={})
    builder.run()