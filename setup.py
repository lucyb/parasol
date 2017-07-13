from setuptools import setup, find_packages

setup(
    name='parasol',
    version='0.1',
    description='Backup data from various on-line services',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'paramiko',
        'python-slugify'
    ],
    entry_points='''
        [console_scripts]
        parasol=parasol.cli:run
    ''',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Backup",
        ],
)
