##! Implements base functionality for BSAP analysis.
##! Generates the Bsap.log file.

# Generated by binpac_quickstart

module BSAP;

export {
	redef enum Log::ID += { LOG_BSAP_DATA };

	type Info: record {
		## Timestamp for when the event happened.
		ts:     time    &log;
		## Unique ID for the connection.
		uid:    string  &log;
		## The connection's 4-tuple of endpoint addresses/ports.
		id:     conn_id &log;
		##destination address of message
		dadd:  count &log;
		## Serial num of message
		ser:	count &log;
		## The Destination function code
		dfun: string &log;
		
		pri: count &log &optional;
				
		NSB_ALARM: bool &log &optional;
	        NSB_INPUT_CHANGE: bool &log &optional;
		NSB_PENDING: bool &log &optional;
		NSB_POWER_FAIL: bool &log &optional;
		NSB_DOWNLOADING: bool &log &optional;
		NSB_VSAT: bool &log &optional;
		NSB_XCHNG_NOT_FOUND: bool &log &optional;
		NSB_COMM_FAIL: bool &log &optional;
	
		slv: count &log &optional;

		sers: count &log &optional;

		buffers: count &log &optional;

		dataOut: string &log &optional;

		# ## TODO: Add other fields here that you'd like to log.
	};

	## Event that can be handled to access the BSAP record as it is sent on
	## to the loggin framework.
	global log_bsapData: event(rec: Info);
}

# Settings for Port-Based DPD (which we aren't using right now)
# const ports = { 1234/udp, 5678/udp };
# redef likely_server_ports += { ports };

event bro_init() &priority=5
	{
	
	Log::create_stream(BSAP::LOG_BSAP_DATA, [$columns=Info, $ev=log_bsapData, $path="bsap_dataOnly"]);
		# Settings for Port-Based DPD (which we aren't using right now)
	# Analyzer::register_for_ports(Analyzer::ANALYZER_BSAP, ports);
	local info: Info;
        info$ts  = network_time();
        info$uid = "test";
        #info$id 
	info$dadd = 18;
	info$ser = 19;
        info$dfun = "func test";

        Log::write(BSAP::LOG_BSAP_DATA, info);


	}

event bsap_event(c: connection, head1: BSAP::Header, data1: string)
	{
	local info: Info;
	info$ts  = network_time();
	info$uid = c$uid;
	info$id  = c$id;
	info$dadd = head1$DADD;
	info$ser = head1$SER;
	info$dfun = head1$DFUN;
	
	if (head1$DFUN != "Poll" ){
	info$NSB_ALARM = head1$func$NSB$Alarms;
        info$NSB_INPUT_CHANGE = head1$func$NSB$Input_Change;
        info$NSB_PENDING = head1$func$NSB$Data_Pending;
        info$NSB_POWER_FAIL = head1$func$NSB$Power_Failure;
        info$NSB_DOWNLOADING = head1$func$NSB$Downloading;
        info$NSB_VSAT = head1$func$NSB$VSAT_Message;
        info$NSB_XCHNG_NOT_FOUND = head1$func$NSB$Exchange_Not_Found;
        info$NSB_COMM_FAIL = head1$func$NSB$Comm_Failure;
	}
	else
	{
	info$pri = head1$func$PRI;
	}
	
	if (head1$DFUN == "Up Ack"){
		info$sers = head1$func$SERS;
	}else if ((head1$DFUN == "NAK") || (head1$DFUN == "DU-Ack") || (head1$DFUN == "Ack-NOD")){
		info$slv = head1$func$SLV;
	}else{
	
	}

	info$dataOut = data1;
	

	Log::write(BSAP::LOG_BSAP_DATA, info);
	}


event dataMessage_event(c: connection, head1: BSAP::Header, data1: string)
        {
        local info: Info;
        info$ts  = network_time();
        info$uid = c$uid;
        info$id  = c$id;
        info$dadd = head1$DADD;
        info$ser = head1$SER;
        info$dfun = "DATA"; #head1$DFUN;

        info$NSB_ALARM = head1$func$NSB$Alarms;
        info$NSB_INPUT_CHANGE = head1$func$NSB$Input_Change;
        info$NSB_PENDING = head1$func$NSB$Data_Pending;
        info$NSB_POWER_FAIL = head1$func$NSB$Power_Failure;
        info$NSB_DOWNLOADING = head1$func$NSB$Downloading;
        info$NSB_VSAT = head1$func$NSB$VSAT_Message;
        info$NSB_XCHNG_NOT_FOUND = head1$func$NSB$Exchange_Not_Found;
        info$NSB_COMM_FAIL = head1$func$NSB$Comm_Failure;
       
	info$dataOut = data1;

        Log::write(BSAP::LOG_BSAP_DATA, info);
}
