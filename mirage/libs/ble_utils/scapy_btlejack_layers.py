from scapy.all import *
'''
This module contains some scapy definitions for communicating with a BTLEJack device.
'''

BTLEJACK_PACKETS_TYPES = {
				0x1 : "command", 
				0x2 : "response",
				0x4 : "notification"
			}

BTLEJACK_PACKETS_OPCODES = {
				0x1 : "version",
				0x2 : "reset",
				0x3 : "scan_access_address",
				0x4 : "recover", 
				0x5 : "recover_channel_map",
				0x6 : "recover_hop_interval",
				0x7 : "sniff_connection_requests",
				0x8 : "enable_jamming", 
				0x9 : "enable_hijacking",
				0xa : "send_packet",
				0xb : "collaborative_channel_map",
				0xe : "debug",
				0xf : "verbose"
			}
BTLEJACK_NOTIFICATION_TYPES = {
				0x0 : "access_address",
				0x1 : "crc",
				0x2 : "channel_map", 
				0x3 : "hop_interval", 
				0x4 : "hop_increment", 
				0x5 : "packet", 
				0x6 : "connection_request", 
				0x7 : "packet_nordic", 
				0x8 : "hijack_status", 
				0x9 : "connection_lost", 
				0xa : "advertisement"
			}
class BTLEJack_Hdr(Packet):
	name = "BTLEJack Packet"
	fields_desc = [
		XByteField("magic",0xBC), 
		BitEnumField("packet_type",None, 4, BTLEJACK_PACKETS_TYPES), 
		ConditionalField(BitEnumField("opcode",None, 4, BTLEJACK_PACKETS_OPCODES), lambda pkt:pkt.packet_type <= 0x3),
		ConditionalField(BitEnumField("notification_type",None, 4, BTLEJACK_NOTIFICATION_TYPES), lambda pkt:pkt.packet_type == 0x4),
		LEShortField("length",None), 
		XByteField("crc",None)
	]
	def pre_dissect(self,data):
		return data[0:4] + data[-1:] + data[4:-1] 

	def post_build(self,p,pay):
		if self.crc is None:
			self.crc = 0xFF
			for byte in p+pay:
				self.crc ^= byte

		if self.length is None:
			self.length = len(pay)
			self.crc ^= self.length
		return p[0:2]+struct.pack('<H',self.length)+pay+struct.pack('B',self.crc)

# BTLEJack Commands
class BTLEJack_Version_Command(Packet):
	name = "BTLEJack Version Command"

class BTLEJack_Reset_Command(Packet):
	name = "BTLEJack Reset Command"

class BTLEJack_Reset_Command(Packet):
	name = "BTLEJack Reset Command"

class BTLEJack_Scan_Connections_Command(Packet):
	name = "BTLEJack Scan Connections Command"

class BTLEJack_Collaborative_Channel_Map_Command(Packet):
	name = "BTLEJack Collaborative Channel Map Command"
	fields_desc = [
			XLEIntField("access_address",None),
			LEX3BytesField("crc_init",None),
			ByteField("start_channel",0),
			ByteField("end_channel",37)
		      ]

class BTLEJack_Recover_Command(Packet):
	name = "BTLEJack Recover Command"
	fields_desc = [
			ByteEnumField("operation_type",None, {
								0x00 : "recover_crc_init",
								0x01 : "recover_channel_map",
								0x02 : "recover_hop"
							})
			]


class BTLEJack_Recover_Crcinit_Command(Packet):
	name = "BTLEJack Recover CRCInit Command"
	fields_desc = [
			XLEIntField("access_address",None)			
		      ]

class BTLEJack_Recover_Channel_Map_Command(Packet):
	name = "BTLEJack Recover Channel Map Command"
	fields_desc = [
			XLEIntField("access_address",None),
			LEX3BytesField("crc_init",None),
			ByteField("start_channel",0),
			ByteField("end_channel",37),
			LEIntField("timeout",None)		
		      ]

class BTLEJack_Recover_Hopping_Parameters_Command(Packet):
	name = "BTLEJack Recover Hopping Parameters Command"
	fields_desc = [
			XLEIntField("access_address",None),
			LEX3BytesField("crc_init",None),
			BTLEChanMapField("channel_map",None)
		      ]


class BTLEJack_Recover_Connection_AA_Command(Packet):
	name = "BTLEJack Recover Connection AA Command"
	fields_desc = [
			XLEIntField("access_address",None)			
		      ]

class BTLEJack_Recover_Connection_AA_Chm_Command(Packet):
	name = "BTLEJack Recover Connection AA Chm Command"
	fields_desc = [
			XLEIntField("access_address",None),
			BTLEChanMapField("channel_map",None)		
		      ]


class BTLEJack_Recover_Connection_AA_Chm_HopInterval_Command(Packet):
	name = "BTLEJack Recover Connection AA Chm Command"
	fields_desc = [
			XLEIntField("access_address",None),
			BTLEChanMapField("channel_map",None),
			XLEShortField("hop_interval",None)		
		      ]

class BTLEJack_Sniff_Connection_Request_Command(Packet):
	name = "BTLEJack Sniff Connection Request Command"
	fields_desc = [
			BDAddrField("address",None),
			ByteField("channel",37)
			]

class BTLEJack_Sniff_Advertisements_Command(Packet):
	name = "BTLEJack Sniff Advertisements Command"
	fields_desc = [
			BDAddrField("address",None),
			ByteField("channel",37)
			]

class BTLEJack_Jam_Advertisements_Command(Packet):
	name = "BTLEJack Jam Advertisements Command"
	fields_desc = [
			ByteField("channel",37),
			ByteField("offset",None),
			FieldLenField("pattern_length", None,fmt="B", length_of="pattern"), 
			StrField("pattern",None)
			]

class BTLEJack_Enable_Jamming_Command(Packet):
	name = "BTLEJack Enable Jamming Command"
	fields_desc = [
			ByteEnumField("enabled",None,{0x00 : "no",0x01 : "yes"})
			]

class BTLEJack_Enable_Hijacking_Command(Packet):
	name = "BTLEJack Enable Hijacking Command"
	fields_desc = [
			ByteEnumField("enabled",None,{0x00 : "no",0x01 : "yes"})
			]

class BTLEJack_Send_Packet_Command(Packet):
	name = "BTLEJack Send Packet Command"
	fields_desc = [
			PacketField("ble_payload",None,BTLE_DATA)
			]

# BTLEJack Responses	
class BTLEJack_Send_Packet_Response(Packet):
	name = "BTLEJack Send Packet Response"

class BTLEJack_Enable_Jamming_Response(Packet):
	name = "BTLEJack Enable Jamming Response"

class BTLEJack_Enable_Hijacking_Response(Packet):
	name = "BTLEJack Enable Hijacking Response"

class BTLEJack_Recover_Response(Packet):
	name = "BTLEJack Recover Response"

class BTLEJack_Scan_Connections_Response(Packet):
	name = "BTLEJack Scan Connections Response"

class BTLEJack_Collaborative_Channel_Map_Response(Packet):
	name = "BTLEJack Collaborative Channel Map Response"

class BTLEJack_Version_Response(Packet):
	name = "BTLEJack Version Response"
	fields_desc = [
			ByteField("major",None),
			ByteField("minor",None)
	]
class BTLEJack_Reset_Response(Packet):
	name = "BTLEJack Reset Response"

class BTLEJack_Sniff_Connection_Request_Response(Packet):
	name = "BTLEJack Sniff Connection Request Response"

class BTLEJack_Sniff_Advertisements_Response(Packet):
	name = "BTLEJack Sniff Advertisements Response"

class BTLEJack_Jam_Advertisements_Response(Packet):
	name = "BTLEJack Jam Advertisements Response"

class BTLEJack_Verbose_Response(Packet):
	name = "BTLEJack Verbose Response"
	fields_desc = [StrField("message",None)]

class BTLEJack_Debug_Response(Packet):
	name = "BTLEJack Debug Response"
	fields_desc = [StrField("message",None)]

class BTLEJack_Recover_Connection_AA_Response(Packet):
	name = "BTLEJack Recover Connection AA Response"
	fields_desc = [
		XLEIntField("access_address",None)
	]

class BTLEJack_Recover_Connection_AA_Chm_Response(Packet):
	name = "BTLEJack Recover Connection AA Chm Response"
	fields_desc = [
		XLEIntField("access_address",None)
	]


# BTLEJack Notifications
class BTLEJack_Access_Address_Notification(Packet):
	name = "BTLEJack Access Address Notification"
	fields_desc = [
		ByteField("channel",None), 
		ByteField("rssi", None), 
		XLEIntField("access_address",None)
	]

class BTLEJack_CRCInit_Notification(Packet):
	name = "BTLEJack CRCInit Notification"
	fields_desc = [
		XLEIntField("access_address",None),
		LEX3BytesField("crc_init",None),
		ByteField("unused",0)
	]

class BTLEJack_Channel_Map_Notification(Packet):
	name = "BTLEJack Channel Map Notification"
	fields_desc = [
		XLEIntField("access_address",None),
		BTLEChanMapField("channel_map",None)
	]

class BTLEJack_Hop_Interval_Notification(Packet):
	name = "BTLEJack Hop Interval Notification"
	fields_desc = [
		XLEIntField("access_address",None),
		XLEShortField("hop_interval",None)
	]

class BTLEJack_Hop_Increment_Notification(Packet):
	name = "BTLEJack Hop Increment Notification"
	fields_desc = [
		XLEIntField("access_address",None),
		ByteField("hop_increment",None)
	]

class BTLEJack_Nordic_Tap_Packet_Notification(Packet):
	name = "BTLEJack Nordic Tap Packet Notification"
	fields_desc = [
		ByteField("header_length",None),
		ByteField("flags",None),
		ByteField("channel",None),
		ByteField("rssi",None),
		LEShortField("event_counter",None), 
		LEIntField("delta", None),
		PacketField("ble_payload",None, BTLE_DATA)
	]

class BTLEJack_Hijack_Status_Notification(Packet):
	name = "BTLEJack Hijack Status Notification"
	fields_desc = [
		ByteEnumField("status",None, {0 : "success", 1 : "failure"})
	]
class BTLEJack_Connection_Lost_Notification(Packet):
	name = "BTLEJack Connection Lost Notification"

class BTLEJack_Advertisement_Notification(Packet):
	name = "BTLEJack Advertisement Notification"
	fields_desc = [
		PacketField("ble_payload",None,BTLE_ADV)
	]

class BTLEJack_Connection_Request_Notification(Packet):
	name = "BTLEJack Connection Request Notification"
	fields_desc = [
		BitEnumField("RxAdd", 0, 1, {0: "public", 1: "random"}),
		BitEnumField("TxAdd", 0, 1, {0: "public", 1: "random"}),
		BitField("RFU", 0, 2),  # Unused
		BitEnumField("PDU_type", 0, 4, {0: "ADV_IND", 1: "ADV_DIRECT_IND", 2: "ADV_NONCONN_IND", 3: "SCAN_REQ",
		4: "SCAN_RSP", 5: "CONNECT_REQ", 6: "ADV_SCAN_IND"}),
		ByteField("payload_length", 0x22),
		PacketField("ble_payload",None,BTLE_CONNECT_REQ)

	]

# Binding BTLEJack Commands
bind_layers(BTLEJack_Hdr, BTLEJack_Version_Command,packet_type=0x1, opcode=0x1)
bind_layers(BTLEJack_Hdr, BTLEJack_Reset_Command,packet_type=0x1, opcode=0x2)
bind_layers(BTLEJack_Hdr, BTLEJack_Scan_Connections_Command, packet_type=0x1,opcode=0x3)
bind_layers(BTLEJack_Hdr, BTLEJack_Collaborative_Channel_Map_Command,packet_type=0x1,opcode=0xb)

bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Command,packet_type=0x1, opcode=0x4)

bind_layers(BTLEJack_Recover_Command,BTLEJack_Recover_Crcinit_Command,operation_type=0x00)
bind_layers(BTLEJack_Recover_Command,BTLEJack_Recover_Channel_Map_Command,operation_type=0x01)
bind_layers(BTLEJack_Recover_Command,BTLEJack_Recover_Hopping_Parameters_Command,operation_type=0x02)

#bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Connection_AA_Command,packet_type=0x1,opcode=0x4)
#bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Connection_AA_Chm_Command,packet_type=0x1,opcode=0x5)
#bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Connection_AA_Chm_HopInterval_Command,packet_type=0x1,opcode=0x6)
bind_layers(BTLEJack_Hdr, BTLEJack_Jam_Advertisements_Command,packet_type=0x1, opcode=0x5)
bind_layers(BTLEJack_Hdr, BTLEJack_Sniff_Connection_Request_Command,packet_type=0x1,opcode=0x7)
bind_layers(BTLEJack_Hdr, BTLEJack_Sniff_Advertisements_Command,packet_type=0x1,opcode=0xc)
bind_layers(BTLEJack_Hdr, BTLEJack_Enable_Jamming_Command,packet_type=0x1,opcode=0x8)
bind_layers(BTLEJack_Hdr, BTLEJack_Enable_Hijacking_Command,packet_type=0x1,opcode=0x9)
bind_layers(BTLEJack_Hdr, BTLEJack_Send_Packet_Command,packet_type=0x1,opcode=0xa)
# Binding BTLEJack Responses
bind_layers(BTLEJack_Hdr, BTLEJack_Send_Packet_Response,packet_type=0x2,opcode=0xa)
bind_layers(BTLEJack_Hdr, BTLEJack_Enable_Jamming_Response,packet_type=0x2,opcode=0x8)
bind_layers(BTLEJack_Hdr, BTLEJack_Enable_Hijacking_Response,packet_type=0x2,opcode=0x9)
bind_layers(BTLEJack_Hdr, BTLEJack_Sniff_Connection_Request_Response,packet_type=0x2, opcode=0x7)
bind_layers(BTLEJack_Hdr, BTLEJack_Sniff_Advertisements_Response,packet_type=0x1,opcode=0xc)
'''
bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Connection_AA_Response,packet_type=0x2, opcode=0x4)
bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Connection_AA_Chm_Response,packet_type=0x2, opcode=0x5)
'''
bind_layers(BTLEJack_Hdr, BTLEJack_Jam_Advertisements_Command,packet_type=0x1,opcode=0x5)
bind_layers(BTLEJack_Hdr, BTLEJack_Recover_Response,packet_type=0x2, opcode=0x4)
bind_layers(BTLEJack_Hdr, BTLEJack_Version_Response,packet_type=0x2, opcode=0x1)
bind_layers(BTLEJack_Hdr, BTLEJack_Reset_Response,packet_type=0x2, opcode=0x2)
bind_layers(BTLEJack_Hdr, BTLEJack_Scan_Connections_Response,packet_type=0x2, opcode=0x3)
bind_layers(BTLEJack_Hdr, BTLEJack_Collaborative_Channel_Map_Response,packet_type=0x2, opcode=0xb)
bind_layers(BTLEJack_Hdr, BTLEJack_Debug_Response,packet_type=0x2, opcode=0xe)
bind_layers(BTLEJack_Hdr, BTLEJack_Verbose_Response,packet_type=0x2, opcode=0xf)

# Binding BTLEJack Notifications
bind_layers(BTLEJack_Hdr, BTLEJack_Access_Address_Notification, packet_type=0x4, notification_type=0x0)
bind_layers(BTLEJack_Hdr, BTLEJack_CRCInit_Notification, packet_type=0x4, notification_type=0x1)
bind_layers(BTLEJack_Hdr, BTLEJack_Channel_Map_Notification, packet_type=0x4, notification_type=0x2)
bind_layers(BTLEJack_Hdr, BTLEJack_Hop_Interval_Notification, packet_type=0x4, notification_type=0x3)
bind_layers(BTLEJack_Hdr, BTLEJack_Hop_Increment_Notification, packet_type=0x4, notification_type=0x4)
bind_layers(BTLEJack_Hdr, BTLEJack_Nordic_Tap_Packet_Notification, packet_type=0x4, notification_type=0x7)
bind_layers(BTLEJack_Hdr, BTLEJack_Hijack_Status_Notification, packet_type=0x4, notification_type=0x8)
bind_layers(BTLEJack_Hdr, BTLEJack_Connection_Lost_Notification, packet_type=0x4, notification_type=0x9)
bind_layers(BTLEJack_Hdr, BTLEJack_Connection_Request_Notification, packet_type=0x4, notification_type=0x6)
bind_layers(BTLEJack_Hdr, BTLEJack_Advertisement_Notification, packet_type=0x4, notification_type=0xa)

