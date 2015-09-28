# Smartlab-Repository

With this repository comes the ability to set up a homeautomation-system, based on openHAB and Z-Wave. It also provides a ROS-bridge and several addons 

Table of content:
| core    | addons         |
|---------|----------------|
| openHAB | ROS-bridge     |
| HABmin  | gcal-parser    |
|         | e-mail client  |
|         | emoncms client |

It is specially adapted for the "Institut für Künstliche Intelligenz" at Hochschule Ravensburg-Weingarten with a user "iki" and the usual password (without numbers)


The following Z-Wave-devices are included

|Quantity|Type|Description|
|---------|---------|-----------|
|1|USB-Controllerstick|Aeon Labs Z-Stick S2|
|2|Wall-Plug|Fibaro Wall-Plug FGWPE 101|
|3|Thermostat|Danfoss living connect Z|
|1|4in1 multisensor|Aeon Labs MultiSensor V1.17|
|1|3in1 ultisensor| Fibaro Motion sensor V2.4|
|2|Door/window sensor| Fibaro door/window sensor FGK 101|

Find the controlling webpage at http://{Server-IP}:8080/ and the HABmin configpage at http://{Server-IP}:8080/habmin/index.html



There is also a subsystem for external purposes, i.e. exhibition-Fair demonstrations

Quantity|Type|Description|
|---------|---------|-----------|
|1|USB-Controllerstick|Aeon Labs Z-Stick S2|
|1|Wall-Plug|Fibaro Wall-Plug FGWPE 101|

A spicific webpage is available at http://{Server-IP}:8080/openhab.app?sitemap=extern


# Implementation

OpenHAB is based on Java and runs on port 8080

- Clone the GIT-repository as normal user
- Make start-script executable
- Add user to the dialout-group
- Add openHAB to autostart
    
    git clone {GIT-URL}
    cd smartlab
    sudo chmod a+x start.sh
    sudo usermod -a -G dialout {user}
    sudo vim /etc/init.d/rc.local
    {smartlab-directory}/start.sh
    
Make sure zwave:port in file smartlab/configurations/openhab.cfg is matching the Z-Wave-controller USB-port.

The security-level can also be modified in openhab.cfg. To add a security-account, edit smartlab/configurations/users.cfg

========= GoogleCalendar parser ==========
- To enable the GoogleCalendar-parser, you have to install the 
  Google-API python-client

    sudo pip install --upgrade google-api-python-client
    
- Afterwards execute {smartlab}/configurations/GCal-Parser/gcal_parser.py
- If the Server does not provide a GUI, add the parameter --noauth_local_webserver

- An webbrowser will open where you have to verify the login with iki.wgt@gmail.com.


If needed, get client_id and client_secret at https://console.developers.google.com/project/openhab-parser/apiui/credential.
Sign in as iki.wgt@gmail.com and see openHAB-Client.


=============== ROS-bridge ===============

For this addon a ROS environment is required
Find a tutorial to set up ROS at http://wiki.ros.org/ROS/Installation

- Copy the ROS-bridge folder into your ROS-environment and build it

   cp -r {smartlab}/configurations/ROS-bridge/iot_bridge {ROS-workspace}/src/
   catkin_make

Make sure, the openHAB-address and user is set correctly in iot_bridge/scripts/iot_bridge

Add the package permanently to your ROS-System
vim /home/{user}/bash.rc
export ROS_PACKAGE_PATH={ROS-workspace}/src/iot_bridge/:$ROS_PACKAGE_PATH




PROBLEME
PORT 8080 belegt
in start.sh und iot_bridge/scripts/iot_bridge ändern


This is a repository for homeautomation, 
It is based on openHAB combined with Z-Wave.