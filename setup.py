from setuptools import setup, find_packages


setup(
    name='logie', 
    version='0.1.0', 
    packages=find_packages(),
    description='simple small logger for python',
    install_requires = [],
    scripts=[],
    python_requires = '>=3',
    include_package_data=True,
    author='Liu Shengli',
    url='https://github.com/gseismic/logie',
    zip_safe=False,
    author_email='liushengli203@163.com'
)
