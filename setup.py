from pathlib import Path

from setuptools import setup, find_packages

from ligo.environment.Constants import Constants

setup(
    name="ligo",
    version=Constants.VERSION,
    description="LIgO is a tool for simulation of adaptive immune receptors and repertoires.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Milena Pavlovic",
    author_email="milenpa@student.matnat.uio.no",
    url="https://github.com/uio-bmi/ligo",
    install_requires=["pandas", "bionumpy==0.2.26", "numpy", "olga", "pyyaml", "airr<1.4", "plotly", "pystache", "scipy", 'npstructures', 'stitchr',
                      'IMGTgeneDL', 'dill'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3"
    ],
    python_requires='>=3.11',
    packages=find_packages(exclude=["test", "test.*"]),
    package_data={
        'ligo': [str(Path('IO/dataset_import/conversion/*.csv')),
                 str(Path("presentation/html/templates/*.html")),
                 str(Path("presentation/html/templates/css/*.css"))] +
                [str(Path("config/default_params/") / dir.name / "*.yaml") for dir in Path("ligo/config/default_params/").glob("*")],
    },
    entry_points={
        'console_scripts': [
            'ligo = ligo.app.LigoApp:main'
        ]
    },
)
