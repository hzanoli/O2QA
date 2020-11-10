from setuptools import setup, find_packages

setup(
    name="O2SingleTrackQA",
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/hzanoli/O2QA',
    license='MIT License',
    author='Henrique J. C. Zanoli',
    author_email='hzanoli@gmail.com',
    description="Tools to plot the Single Track QA for the ALICE O2",
    entry_points={'console_scripts': ['qa-single-track = plot:plot', 'compare-qa-single-track=compare:compare']},
    install_requires=["numpy",
                      "matplotlib",
                      "seaborn",
                      "pandas",
                      "uproot"]
)
