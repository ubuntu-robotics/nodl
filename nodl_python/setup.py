from pathlib import Path

from setuptools import find_packages, setup

package_name = 'nodl_python'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Ted Kern',
    author_email='ted.kern@canonical.com',
    maintainer='Ubuntu Robotics',
    maintainer_email='ubuntu-robotics@lists.launchpad.net',
    url='https://github.com/ubuntu-robotics/nodl',
    download_url='https://github.com/ubuntu-robotics/nodl/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Limited General Public License v3',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Implementation of the NoDL API in Python.',
    license='GNU Limited General Public License v3',
    tests_require=['pytest'],
    package_data={
        'nodl': [str(child) for child in Path('nodl/schemas').iterdir() if child.is_file()]
    }
)
