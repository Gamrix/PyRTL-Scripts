from setuptools import setup

setup(
    name='PyRTL-Scripts',
    version='0.0.1',
    packages=['JohnLib'],
    description='RTL-level Hardware Design and Simulation Toolkit scripts',
    author='John Clow',
    author_email='',
    install_requires=['six', 'pyrtl'],
    tests_require=['tox', 'nose'],
    extras_require={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: System :: Hardware'
    ]
)
