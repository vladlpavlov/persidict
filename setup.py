import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="persidict"
    ,version="0.0.1"
    ,author="Vlad (Volodymyr) Pavlov"
    ,author_email="vlpavlov@ieee.org"
    ,description= "Simple persistent key-value store for Python. " 
        "Values are stored as files on a disk or as S3 objects."
    ,long_description=long_description
    ,long_description_content_type="text/markdown"
    ,url="https://github.com/vladlpavlov/persidict"
    ,packages=["persidict"]
    ,classifiers=[
        "Development Status :: 3 - Alpha"
        , "Intended Audience :: Developers"
        , "Intended Audience :: Science/Research"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 3"
        , "License :: OSI Approved :: MIT License"
        , "Operating System :: OS Independent"
        , "Topic :: Software Development :: Libraries"
        , "Topic :: Software Development :: Libraries :: Python Modules"
    ]
    ,keywords='persistence, dicts, distributed, parallel'
    ,python_requires='>=3.7'
    ,install_requires=[
        'numpy'
        , 'scipy'
        , 'pandas'
        , 'jsonpickle'
        , 'psutil'
        , 'boto3'
        , 'moto'
        , 'pytest'
    ]

)