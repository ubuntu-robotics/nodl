# NoDL - Node Definition Language

![Test NoDL](https://github.com/ubuntu-robotics/nodl/workflows/test%20nodl/badge.svg?event=push)

NoDL is the Node Definition Language - a common declarative representation of a Node's interfaces including Parameters, Topics, Services, and Actions. See the [design document (review in progress)](https://github.com/ubuntu-robotics/design/blob/node_idl/articles/ros2_nodl.md) for more context on the project.

This repository contains the CLI and parsing utilities for NoDL.

## Installation

Run `python3 setup.py install`

Install the 'ament_nodl' extension for exporting NoDL .xml files:

`sudo apt-get install ros-<ros2_distro>-ament-nodl`

## Configuration

Add to `package.xml`:

`<depend>ament_nodl</depend>`

Add to `CMakeLists.txt`:

`find_package(ament_nodl REQUIRED)`

`nodl_export_node_description_file(<package_name>.nodl.xml)`

## Usage

Create a file called "<package_name>.nodl.xml" in the same folder as your project's CMakeLists.txt. 
Include in this file the interface description for each node in the package.
Node attributes can be `parameter`, `topic`, `service` or `action`.

Valid values for the topic `role` tag are: `publisher`, `subscription`, or `both`.
Valid values for the service `role` tag are: `server`, `client`, or `both`.
Valid values for the action `role` tag are: `server`, `client`, or `both`.
Types can have custom names.

### Example

```xml
<interface version="1">
	<node name="<node1_name>" executable="<executable_name>">
		<parameter name="rate" type="int" />
		<topic name="/foo/bar" type="std_msgs/msg/String" role="subscription" />
		<service name="/example_service" type="std_srvs/srv/Empty" role="client" />
		<action name="/example_action" type="example_interfaces/action/Fibonacci" role="both" />
	</node>
	<node name="<node2_name>" executable="<executable_name>">
		...
	</node>
</interface>
```

## CLI

See available verbs on the [ROS 2 command line tools for NoDL repo](https://github.com/ubuntu-robotics/nodl/tree/master/ros2nodl).
