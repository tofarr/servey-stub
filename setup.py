import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_require = {
    "dev": [
        "black~=23.3",
        "boto3~=1.26",
        "requests~=2.31",
        "pytest~=7.2",
        "pytest-cov~=4.0",
        "pytest-xdist~=3.2",
        "pylint~=2.17",
    ],
}
extras_require["all"] = list(
    {
        dependency
        for dependencies in extras_require.values()
        for dependency in dependencies
    }
)


setuptools.setup(
    name="servey-stub",
    author="Tim O'Farrell",
    author_email="tofarr@gmail.com",
    description="A service stub generator for servey",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofarr/servey-stub",
    packages=setuptools.find_packages(exclude=("tests*", "examples")),
    package_data={"": ["*.txt"]},
    include_package_data=True,
    install_requires=[
        "servey~=2.8",
    ],
    extras_require=extras_require,
    setup_requires=["setuptools-git-versioning"],
    setuptools_git_versioning={"enabled": True, "dirty_template": "{tag}"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
