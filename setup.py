from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='placeholders',
    version='2.0',
    description='Create placeholder images by embedding keywords into regular jpg images.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Austin Brown',
    author_email='austinbrown34@gmail.com',
    url='https://github.com/austinbrown34/placeholders',
    keywords=['image', 'exif', 'jpg'],
    packages=find_packages(),
    scripts=['scripts/placeholders'],
    install_requires=[
        'Pillow',
        'piexif',
    ],
    include_package_data=True,
)
