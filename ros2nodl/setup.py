from setuptools import find_packages, setup

package_name = 'ros2nodl'

setup(
    name=package_name,
    version='0.3.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ubuntu Robotics',
    maintainer_email='ubuntu-robotics@lists.launchpad.net',
    url='https://github.com/ubuntu-robotics/nodl',
    download_url='https://github.com/ubuntu-robotics/nodl/releases',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='CLI tools for NoDL files.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
        'ros2cli.command': [
            'nodl = ros2nodl._command._nodl:_NoDLCommand',
        ],
        'ros2nodl.verb': [
            'show = ros2nodl._verb._show:_ShowVerb',
            'validate = ros2nodl._verb._validate:_ValidateVerb'
        ]
    },
)
