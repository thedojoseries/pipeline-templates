import os
from setuptools import setup, find_packages

src_dir = os.path.dirname(__file__)

install_requires = [
    "python-dateutil<3.0.0",
    "stacker>=1.7.0",
    "troposphere>=2.3.2",
    "awacs>=0.8.2",
]

def read(filename):
    full_path = os.path.join(src_dir, filename)
    with open(full_path) as fd:
        return fd.read()

if __name__ == "__main__":
    setup(
        name="custom_blueprints",
        version="1.0.0",
        author="Renan Dias",
        author_email="author@gmail.com",
        license="New BSD license",
        description="Custom blueprints for the DevOps Dojo",
        packages=find_packages(),
        install_requires=install_requires
    )
