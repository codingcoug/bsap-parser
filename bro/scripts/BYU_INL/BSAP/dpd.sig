# Generated by binpac_quickstart
# Payload Signature by Jesse Codling
# Last Modified: 02 Apr 2019
signature dpd_bsap {
	
	ip-proto = udp
	

		# TODO: add support for DLE-SOH (for eBSAP messages)
	payload /\x10(\x02|\x01)[\x00-\xFF]{3,}\x10\x03[\x00-\xFF]{2}/
		# matches:
			# DLE
			# STX
			# any two bytes
			# 1-250 bytes that are not DLE followed by ETX
			# DLE
			# ETX
			# any two bytes

	enable "bsap"
}
