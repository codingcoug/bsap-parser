BSAP Network Protocol Dissector
==================================
# Purpose
Enhance the existing BSAP network protocol dissector to function and analyze network traffic over Ethernet and be portable by March 10, 2019 for under $1500 and 1,400 man hours.

# Structure
```
├── bsap
│   ├── bsapmodule.py         -- Main file for simulator
│   ├── constants.py          -- Contains constants used by multiple files
│   ├── interpreter.py        -- Contains functions for breaking down packets
│   ├── README.md             -- Detailed description of simulator
│   ├── requirements.txt      -- Requirements necessary to run simulator
│   └── udpcommunication.py   -- Contains functions used to communicate using UDP
├── CONTRIBUTING.md
└── README.md
```

# Analyzer for Bro
## Install
in your bro source directory, make the following symlinks:
- bro/scripts/base/protocols/bsap -> ./bro/base
- bro/src/analyzer/protocol/bsap -> ./bro/analyzer

# Everything below is deprecated

# Requirements
1. Build an apparatus to simulate flow between two tanks that is controllable and monitored by two PLC's.
2. Build a terminal server that manages two PLCs to control the movement of water from one tank to another.
    a. Allows the engineer to look at the processes, modify them, and download the BSAP traffic to use with secondary tools.
    b. Construct a workstation that allows this connection
    c. Also allow remote access to the server
3. Create a Engineering workstation that can change behavior of the terminal server.
4. Build a functional protocol dissector for BRO that can run on an engineering workstation:
    a. Interpret the different components that make up the BSAP communication protocol
    b. Allows analysts to understand the different actions being taken across the network
    c. Flag suspicious traffic

# Measures:
1. Are we able to control the transfer of liquid between two tanks?
2. Is an engineer able to talk to the PLC's that control the transfer locally and remotely?
3. Can the engineer see the network communications, modify them, and download them?
4. Summarize the protocol information in a format that is useful for the engineer.
5. Is the software integrated with BRO network tools?
6. Are the PLC's communicating using BSAP?

