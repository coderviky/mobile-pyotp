import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mobile-pyotp",
    version="0.0.1",
    author="Vivek Suryawanshi",
    author_email="coderviky@gmail.com",
    description="Python OTP with Mobile Number Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coderviky/mobile-pyotp",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
