import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
    name='ddgimagetoascii',
    version='1.0.0',
    url='https://github.com/mikhailfedechkin/kts',
    author = 'Mikhail',
    description='This is console utility for getting random image from duckduckgo by keyword and convert it into ascii-art file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='kts metaclass hw lesson03',
    packages=setuptools.find_packages(),
    classifiers = [
    	"Programming Language :: Python :: 3",
    	"Operating System :: OS Independent",
	],
)