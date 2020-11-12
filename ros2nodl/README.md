# ros2nodl

![License](https://img.shields.io/badge/License-Apache%202-green) ![Test NoDL](https://github.com/ubuntu-robotics/nodl/workflows/test%20nodl/badge.svg?event=push)

The source code for the NoDL command line tools for ROS 2.

## Usage

available verbs for `ros2 nodl`:

- show
- validate

Run `ros2 nodl --help` to see all available commands

Run `ros2 nodl <verb> --help` to see individual verb usage

### show
Pretty-print NoDL information for given executable(s)

```bash
usage: ros2 nodl show [-h] package_name [executable [executable ...]]

Show NoDL data

positional arguments:
  package_name  Name of the package to show.
  executable    Specific Executable to display.

optional arguments:
  -h, --help    show this help message and exit
```

#### Example

Show the NoDL data for `publisher_lambda` in `examples_rclcpp_minimal_publisher`:

```bash
$ ros2 nodl show examples_rclcpp_minimal_publisher publisher_lambda
{'actions': [],
 'executable': 'publisher_lambda',
 'name': 'minimal_publisher',
 'parameters': [],
 'services': [],
 'topics': [{'name': 'topic',
             'publisher': True,
             'subscription': False,
             'type': 'std_msgs/msg/String'}]}
```

### validate

Validate a .nodl.xml file against the schema and attempt to parse it

```bash
usage: ros2 nodl validate [-h] [-p] [file [file ...]]

Validate NoDL XML documents

positional arguments:
  file         Specific .nodl.xml file(s) to validate.

optional arguments:
  -h, --help   show this help message and exit
  -p, --print  Print parsed output.
```

#### Example

Validate a file `publisher.nodl.xml`

```bash
$ ros2 nodl validate publisher.nodl.xml
Validating publisher.nodl.xml...
  Success
All files validated
```
