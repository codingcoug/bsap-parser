module BSAP;

export {

	## An array of named bools marking the presence of each type of node
	## alert
	type NodeStatus: record {
		Alarms: bool;
		Input_Change: bool;
		Data_Pending: bool;
		Power_Failure: bool;
		Downloading: bool;
		VSAT_Message: bool;
		Exchange_Not_Found: bool;
		Comm_Failure: bool;
	};

	## Headers sepecific to all data messages
	type DataHeader: record {
		## SEQ: Application Sequence Number
		SEQ: count;

		## SFUN: Source Function Code
		SFUN: count;
	};

	## Header Components dependent on the packet type
	type FunctionHeader: record {
		## PRI: Priority of Requested Data (for Poll messages)
		PRI: count &optional;

		## NSB: Node Status Byte (converted to boolean values)
		NSB: NodeStatus &optional;

		## Responding Slave Address (for ACKs)
		SLV: count &optional;

		## Source Message Serial Number (for Master ACKs)
		SERS: count &optional;

		## Data Message Headers
		data: DataHeader &optional;
	};

	## Extra fields for Globally-Addressed messages
	type GlobalHeader: record {
		## DADD: Destination (Global) Address
		DADD: count;

		## SADD: Source (Global) Address
		SADD: count;

		## CTL: Control Byte
		CTL: count;

	};

	## Complete BSAP Header, adaptable to all content types
	type Header: record {
		## GRN: group number (for expanded BSAP messages)
		GRN: count &optional;

		## DADD: Destination Local Address (7-bit BSAP address)
		DADD: count;

		## SER: Message Serial Number
		SER: count;

		## Header for Global Messages
		glbl: GlobalHeader &optional;

		## DFUN: (Destination) Function Code
		## Some message types have an additional function code in their
		## function header;
		DFUN: string &optional;

		## Function Header: Components that vary dynamically with DFUN
		func: FunctionHeader &optional;
	};

}
