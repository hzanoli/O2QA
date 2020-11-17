from setuptools import setup, find_packages

setup(
    name="alice3data",
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/hzanoli/O2QA',
    license='MIT License',
    author='Henrique J. C. Zanoli',
    author_email='hzanoli@gmail.com',
    description="Tools to download the ALICE3 data",
    entry_points={'console_scripts': ['alice3_download=download:download']},
    install_requires=['beautifulsoup4', 'requests'])
