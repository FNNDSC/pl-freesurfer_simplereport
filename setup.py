from setuptools import setup

setup(
    name='freesurfer_simplereport',
    version='1.1.0',
    description='A ChRIS DS plugin that generates a report table (in various formats) off a FreeSurfer annotation/segmentation volume',
    author='FNNDSC',
    author_email='rudolph.pienaar@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-freesurfer_simplere',
    py_modules=['freesurfer_simplereport'],
    install_requires=['chris_plugin'],
    license='MIT',
    python_requires='>=3.8.2',
    entry_points={
        'console_scripts': [
            'freesurfer_simplereport = freesurfer_simplereport:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
