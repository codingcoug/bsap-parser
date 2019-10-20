BSAP Python simulator
=====================

# Introduction to the Simulator
## Summary
Simulator we used to test our concept. The purpose of the code was to create BSAP messages and send them over the network, creating traffic to be monitored.

The files are separate so that they can be edited and tested individually.

## Description
### requirements.txt
A list of all pip3 packages necessary to run the code

### constants.py
All constants that the code uses. This includes the constant BSAP messages that will be sent back and forth.

### uspcommunication.py
This file is currently misnamed. It contains the function for sending something over UDP. Also contains code to recieve a packet over UDP.

### interpreter.py
The interpreter breaks down a given BSAP packet into its individual parts. It also checks the packet to ensure that it has the proper structure.  

### bsapmodule.py
This is the main file for the simulator. You run it as explained below, specifying if it is the Master or the Slave.

# Running the simulator

## Using Docker
* The root folder of this repository contains two Dockerfiles which run containers for an emulator master and slave.
* Running these requires installing the Docker daemon
* Once docker is installed, cd to the root folder and run `./dstart`. This creates and runs 2 docker containers called emum (master) and emus (slave).
* Open 2 terminal windows and paste `docker exec -it emum python bsap/bsapmodule.py --address 0 -v` in one and `docker exec -it emus python bsap/bsapmodule.py --address 1 -v` in the other. To change the command being run, just change everything after `emu[s/m]` to the new command, in this form: `docker exec -it emu[s/m] [COMMAND]`.
* If all is working, there should be a ton of output coming out of both terminal windows.


## Running natively

### Requirements
* Running the simulator requires two devices, a master and a slave computer.
* The bsapmodule.py file needs to be changed to update to the correct IP addresses of the master and slave
    * UDP_IP_MASTER is the master's IP
    * UDP_IP_SLAVE is the slave's IP
* Install all requirements in the requirements.txt

### Running the simulator
The bsapmodule.py script requires a single argument, the address of the device. Essentially this is meant to identify if this is the Master or the slave. ***The master is always address 0***. The slave address doesn't really matter as long as its not 0.

***The slave must be started before the master, or communication will not occur.***

```
# Starting the SLAVE
python3 bsapmodule.py --address 1
```

After the slave is started, the master can start.

```
# Starting the MASTER
python3 bsapmodule.py --address 0
```

The simulator has other arguments that you can learn about by typing:
```
python3 bsapmodule.py -h
```
