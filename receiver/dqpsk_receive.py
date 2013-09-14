#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Sep  9 18:50:04 2013
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from grc_gnuradio import blks2 as grc_blks2
#from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
#import wx

class mytop(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self)
#		grc_wxgui.top_block_gui.__init__(self, title="Top Block")
#		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
#		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000
		self.samp_per_sym = samp_per_sym = 8

		##################################################
		# Blocks
		##################################################

		# Docs for osmosdr parms are in: http://cgit.osmocom.org/gr-osmosdr/tree/grc/gen_osmosdr_blocks.py

		self.rtlsdr_source_c_0 = osmosdr.source( args="nchan=1")
		self.rtlsdr_source_c_0.set_sample_rate(samp_rate)
		self.rtlsdr_source_c_0.set_center_freq(500e6, 0)
		self.rtlsdr_source_c_0.set_freq_corr(0, 0)
		self.rtlsdr_source_c_0.set_iq_balance_mode(0, 0) # 0 is off, 1 manual, 2 automatic
		self.rtlsdr_source_c_0.set_gain_mode(1, 0) # automatic gain. 0 means manual, 1 means automatic
#		self.rtlsdr_source_c_0.set_gain(10, 0)
#		self.rtlsdr_source_c_0.set_if_gain(20, 0)
#		self.rtlsdr_source_c_0.set_bb_gain(20, 0)
#		self.rtlsdr_source_c_0.set_antenna("", 0)
		self.rtlsdr_source_c_0.set_bandwidth(0, 0)
		  
		self.digital_dxpsk_demod_0 = digital.dqpsk_demod(
			mod_code='gray',
			samples_per_symbol=8,
			excess_bw=0.35,
			freq_bw=6.28/1000.0,
			phase_bw=6.28/1000.0,
			timing_bw=6.28/1000.0,
#			gray_coded=True,
			verbose=True,
			log=True
		)
		self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/tmp/sdr_output.txt")
		self.blocks_file_sink_0.set_unbuffered(False)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="0001000100010001",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.digital_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_file_sink_0, 0))
		self.connect((self.rtlsdr_source_c_0, 0), (self.digital_dxpsk_demod_0, 0))


	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.rtlsdr_source_c_0.set_sample_rate(self.samp_rate)

	def get_samp_per_sym(self):
		return self.samp_per_sym

	def set_samp_per_sym(self, samp_per_sym):
		self.samp_per_sym = samp_per_sym

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = mytop()
	tb.run()

