# Generated by binpac_quickstart

# ## TODO: Add your protocol structures in here.
# ## some examples:

# Types are your basic building blocks.
# There are some builtins, or you can define your own.
# Here's a definition for a regular expression:
# type BSAP_WHITESPACE = RE/[ \t]*/;

# A record is a collection of types.
# Here's one with the built-in types
# type example = record {
#
# };

enum node_status {
	NSB_ALARM = 0x01,
	NSB_INPUT_CHANGE = 0x02,
	NSB_PENDING = 0x04,
	NSB_POWER_FAIL = 0x08,
	NSB_DOWNLOADING = 0x10,
	NSB_VSAT = 0x20,
	NSB_XCHNG_NOT_FOUND = 0x40,
	NSB_COMM_FAIL = 0x80
};

enum function_codes {
	FUNC_DIAL_UP_ACK = 0x81,
	FUNC_POLL = 0x85,
	FUNC_DOWN_ACK = 0x86,
	FUNC_NOD = 0x87,
	FUNC_UP_ACK = 0x8B,
	FUNC_NACK = 0x95,
	FUNC_RDB = 0xA0,
	FUNC_RDB_EXTENSION = 0xA1
};

enum function_classes {
	CLASS_SLAVE_ACK,
	CLASS_MASTER_ACK,
	CLASS_DATA,
	CLASS_POLL
};

type BSAP_Payload = RE/[\x00-\xFF]*\x10\x03/;

type BSAP_FuncClass = uint8;
type BSAP_FunctionCode = uint8;


type BSAP_Expanded(DleStx: bytestring) = case DleStx[1]  of {
		1 -> GRN: uint8; # group number
		default -> none: empty;
};

type BSAP_DataHeader = record {
	SEQ: uint8; # applicaiton sequence number
	SFUN: BSAP_FunctionCode; # source function code
};

type BSAP_NodeStatus = record {
	raw: uint8; #raw, packed byte
} &let {
	Alarms: bool = (NSB_ALARM & raw);
	Input_Change: bool = (NSB_INPUT_CHANGE & raw);
	Data_Pending: bool = (NSB_PENDING & raw);
	Power_Failure: bool = (NSB_POWER_FAIL & raw);
	Downloading: bool = (NSB_DOWNLOADING & raw);
	VSAT_Message: bool = (NSB_VSAT & raw);
	Exchange_Not_Found: bool = (NSB_XCHNG_NOT_FOUND & raw);
	Comm_Failure: bool = (NSB_COMM_FAIL & raw);
};


function BSAP_ClassifyFunction(DFUN: BSAP_FunctionCode): BSAP_FuncClass
	%{
		switch(DFUN) {
			case FUNC_DOWN_ACK:
			case FUNC_DIAL_UP_ACK:
			case FUNC_NOD:
			case FUNC_NACK:
				return CLASS_SLAVE_ACK;
			case FUNC_UP_ACK:
				return CLASS_MASTER_ACK;
			case FUNC_POLL:
				return CLASS_POLL;
			default:
				return CLASS_DATA;
		}
	%}

type BSAP_FunctionHeader(head: BSAP_Header, is_orig: bool) = record {

	function_data: case func_class of {
		CLASS_SLAVE_ACK -> SLV: uint8; # responding slave address
		CLASS_MASTER_ACK -> SERS: uint8; # source message SER
		CLASS_DATA -> data: BSAP_DataHeader;
		default -> none: empty;
	};

	status_or_not: case (head.DFUN == FUNC_POLL) of {
		true -> PRI: uint8; # data request priority: poll only
		false -> NSB: BSAP_NodeStatus; # Node Status Byte
	};


} &let {
	func_class: BSAP_FuncClass = BSAP_ClassifyFunction(head.DFUN);
};

type BSAP_GlobalHeader = record {
	DADD: uint8; # Destination address (global)
	SADD: uint8; # Source Address (global)
	CTL: uint8; # Control Byte
};

type BSAP_Header(is_orig: bool, DleStx: bytestring) = record {
	exp: BSAP_Expanded(DleStx);
	DADD: uint8;
	SER: uint8;

	global_or_not: case (DADD & 0x80) of {
		0 -> none: empty;
		default -> glbl: BSAP_GlobalHeader; # global header (record)
	};
	DFUN: BSAP_FunctionCode; # destination function code
	func: BSAP_FunctionHeader(this,is_orig);
} &let {
	LADD: uint8 = DADD & 0x7F; # Local address is the lower 7 bits of the address field
};


type BSAP_PDU(is_orig: bool) = record {
	DleStx: bytestring &length = 2;
	head: BSAP_Header(is_orig, DleStx);
	rawData: BSAP_Payload;
	crc: uint16;
} &byteorder=bigendian;