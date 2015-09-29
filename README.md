# Smartlab with OpenHAB and Z-Wave

With this repository comes the ability to set up a homeautomation-system, based on openHAB and Z-Wave.  
It also provides a ROS-bridge and several extensions located at **smartlab/configurations** and **smartlab/configurations/rules/**

**Table of content:**

| Core         |Extensions |
|------------|------------|------------|
| OpenHAB      | ROS-bridge    |
| HABmin      | GCal-parser  |
|| E-Mail client     |
|| Emoncms client    |

**Z-Wave** is a wireless communications specification designed to allow devices in the home (lighting, access controls, entertainment systems and household appliances, for example) to communicate with one another for the purposes of home automation.  
**OpenHAB** is a software for integrating different home automation systems and technologies into one single solution that allows over-arching automation rules and that offers uniform user interfaces.  
**Robot Operating System (ROS)** is a collection of software frameworks for robot software development, providing operating system-like functionality on a heterogeneous computer cluster. ROS provides standard operating system services such as hardware abstraction, low-level device control, implementation of commonly used functionality, message-passing between processes, and package management.  
**GCal-parser** is used to provide action-/ and timebased controll of the Z-Wave network. It respoonds to the start and end of an calendar entry, depending on a specified location.  
**E-Mail Client** is used to send E-Mails, based on an Google E-Mail Server.  
**Emoncms** is a open-source web-app for processing, logging and visualising energy, temperature and other environmental data.

This project is specially adapted to the "Institut für Künstliche Intelligenz" at Hochschule Ravensburg-Weingarten with a user "iki" and the usual password

The following Z-Wave-devices are included

|Quantity   |Type               |Description                        |
|-----------|-----------|-----------|
|1          |USB-Controllerstick|Aeon Labs Z-Stick S2               |
|2          |Wall-Plug          |Fibaro Wall-Plug FGWPE 101         |
|3          |Thermostat         |Danfoss living connect Z           |
|1          |4in1 multisensor   |Aeon Labs MultiSensor V1.17        |
|1          |3in1 ultisensor    |Fibaro Motion sensor V2.4          |
|2          |Door/window sensor |Fibaro door/window sensor FGK 101  |

Find the controlling webpage at **http://{Server-IP}:8080/** and the HABmin configpage at **http://{Server-IP}:8080/habmin/index.html**

There is also a subsystem for external purposes, i.e. exhibition-Fair demonstrations

|Quantity   |Type               |Description                |
|-----------|-----------|-----------|
|1          |USB-Controllerstick|Aeon Labs Z-Stick S2       |
|1          |Wall-Plug          |Fibaro Wall-Plug FGWPE 101 |

A spicific webpage is available at **http://{Server-IP}:8080/openhab.app?sitemap=extern**
***
The following is a brief guide, how to set up the System.  
A detailed documentation in german can be found within the repository
***
# Implementation
### Z-Wave
If not done yet, include the Z-Wave devices into the Z-Wave network.
To do so, press the include-button first on the controller, then on the corresponding device
***
Note that some USB-controller can not enter the include-mode while pluged in an USB-port
***

### OpenHAB

OpenHAB is based on Java and is running on port 8080

* Clone the GIT-repository as normal user
* Make the start-script executable
* Add user to the dialout-group
* Add openHAB to autostart

``` sh
git clone {GIT-URL}
cd smartlab
sudo chmod a+x start.sh
sudo usermod -a -G dialout {user}
sudo vim /etc/init.d/rc.local
```
```sh
#rc.local
...
{smartlab-directory}/start.sh
```
Make sure **zwave:port** in file **smartlab/configurations/openhab.cfg** is matching the used Z-Wave-controller USB-port.

The security-level can also be modified in openhab.cfg. 
```sh
#openhab.cfg
...
# ON = security is switched on generally
# OFF = security is switched off generally
# EXTERNAL = security is switched on for external requests 
security:option=EXTERNAL
```
To add a security-account, edit **smartlab/configurations/users.cfg**
```sh
#users.cfg
user=password
```

### ROS-bridge

For this extension a ROS environment is required  
Copy the folder iot_bridge and build the package
``` sh
cp -r smartlab/configurations/ROS-bridge/iot_bridge {ROS-workspace}/src/
catkin_make
```
Make sure, the openHAB-address and /-user is set correctly in **iot_bridge/scripts/iot_bridge**
```python
#iot_bridge
...
  def __init__(self):
    self.iot_host=rospy.get_param(BASENAME+'/host',"openHAB-IP")
    self.iot_port=rospy.get_param(BASENAME+'/port',8080)
    self.username=rospy.get_param(BASENAME+'/username',"openhab")
    self.password=rospy.get_param(BASENAME+'/password',"")
```

Add the package-path
```sh
# ~/.bashrc
...
export ROS_PACKAGE_PATH={ROS-workspace}/src/iot_bridge/:$ROS_PACKAGE_PATH
```

### GoogleCalendar parser
To enable the GCal-parser, you have to install the **Google-API python-client**
``` sh
sudo pip install --upgrade google-api-python-client
```
Afterwards execute **smartlab/configurations/GCal-Parser/gcal_parser.py**.  
A webbrowser will open where you have to verify the access with **iki.wgt@gmail.com**.  

If the Server does not provide a GUI, add the parameter **--noauth_local_webserver**.  
# Make changes

### Add devices
* Connect the device with the controller
* Add to smartlab/configurations/items/zwave.items
* Add to smartlab/configurations/sitemaps/default.sitemap
* Add to smartlab/configurations/rules/emoncms.rules (if wanted to log values)

### Update openHAB and HABmin
* Save smartlab/configurations/
* Download and unzip openHAB **runtime** and **addons** at **http://www.openHAB.org/getting-started/downloads.html**  
or the latest snapshot at **https://openhab.ci.cloudbees.com/job/openhab/**
* Insert the saved folder and the addons **binding.zwave** and **action.mail**
* Download HABmin at **https://github.com/cdjackson/HABmin**, unzip it to **smartlab/webapps/** and rename the folder to habmin
* Move **/smartlap/webapps/habmin/addons/io.habmin** to **/smartlab/addons/**

### Change E-Mail Server

To set a new E-Mail server, open **smartlab/configurtaions/openhab.cfg** and make changes at

```sh
#openhab.cfg
#### Mail Action configuration ####
mail:hostname=smtp.gmail.com
mail:port=587
mail:username=ikiwgt@gmail.com
mail:password=password
mail:from=noreply@openHAB.info
mail:tls=true
```

### Change Server-IP

If the server-IP has changed, only the file **{ROS-workspace}/src/iot_bridge/scripts/iot_bridge** has to be modified
```python
#iot_bridge
...
  def __init__(self):
    self.iot_host=rospy.get_param(BASENAME+'/host',"openHAB-IP")
    self.iot_port=rospy.get_param(BASENAME+'/port',8080)
```
