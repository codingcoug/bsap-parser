module BSAPdumb;

export {
	#set all UDP packets to be dumped
	redef udp_content_deliver_all_orig = T;
	redef udp_content_deliver_all_resp = T;

	redef enum Log::ID += {LOG}; #add a log store for BSAP packets
	type Info: record {
		ts: time &log; #recieved timestamp
		id: conn_id &log; #connection ID tuple (containing to/from addresses and ports)
		service: set[string] &optional &log; #service identifier tuples
		payload: string &optional &log; #packet data dump
	};

}

event bro_init() {
	Log::create_stream(BSAPdumb::LOG,[$columns=Info, $path="bsap_dump"]);
	#initialize the new log store
}

event udp_contents(u: connection, is_orig: bool , contents: string) {
	if (contents[:2] == "\x10\x02") {
		local out: BSAPdumb::Info = [$ts=network_time(),$id=u$id,$service=u$service,$payload=contents];
#	assemble the output object:
#	ts: get the current time
#	id: get the ID tuple from the connection
#	service: get the service data from the connection
#	payload: get the contents string
		Log::write(BSAPdumb::LOG,out);
	}
}
