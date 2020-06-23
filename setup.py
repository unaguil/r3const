from setuptools import setup, find_packages

setup(
    name='r3const',
    version='1.0.0',
    url='https://github.com/unaguil/r3const.git',
    author='Unai Aguilera',
    author_email='unai.aguilera@deusto.es',
    description='Minimal 3d scene manager',
    packages=find_packages(),    
    install_requires=['panda3d==1.10.6'],
)