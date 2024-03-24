import os
from setuptools import setup, find_packages

folder_path = os.path.dirname(os.path.abspath(__file__))
requirements_path = os.path.join(folder_path, 'requirements.txt')
with open(requirements_path, 'r') as f:
    dependencies = list(map(lambda s: s.strip(), f.readlines()))

setup(
    name='basket',
    version='0.0.1',
    description='Projet pour les cours d\'optimisation',
    packages=find_packages(),
    install_requires=dependencies
)
