from setuptools import setup, find_packages

setup(
    name="O2QAPlot",
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/hzanoli/O2QA',
    license='MIT License',
    author='Henrique J. C. Zanoli',
    author_email='hzanoli@gmail.com',
    description="Plotting tools for the ALICE O2 quality assurance",
    entry_points={'console_scripts': ['plot-all=plot:plot', 'compare-plots=compare:compare']},
    install_requires=["numpy", "matplotlib", "seaborn", "pandas", "uproot"]
)
