#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: add tests for real event data, loading it from files (examples by Werner)

"""
TODO: description of module
"""

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import sys
import unittest

sys.path = [ '.', '..' ] + sys.path
from utils import _init_log
from events import *
from datetime import datetime

log = _init_log("events_test")

class TestEventsX(unittest.TestCase):

	def setUp(self):
		# Events to test
		self.e = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 20))
		self.f = PyEvent(datetime(2015, 1, 7, 11, 48, 15))

		# Events for 'during' tests
		self.g = PyEvent(datetime(2015, 1, 7, 10, 48, 16), datetime(2015, 1, 7, 10, 48, 19)) # normal case
		self.h = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 18)) # edge case: minimum
		self.i = PyEvent(datetime(2015, 1, 7, 10, 48, 17), datetime(2015, 1, 7, 10, 48, 20)) # edge case: maximum
		self.j = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 20)) # edge case: same event

		# Events for before tests
		self.r = PyEvent(datetime(2015, 1, 4, 10, 40, 15), datetime(2015, 1, 6, 10, 43, 11)) # normal case
		self.s = PyEvent(datetime(2015, 1, 4, 10, 40, 15), datetime(2015, 1, 7, 10, 48, 14)) # edge case

		# Events for after tests
		self.t = PyEvent(datetime(2015, 1, 7, 10, 48, 40), datetime(2015, 1, 7, 10, 48, 50)) # normal case
		self.u = PyEvent(datetime(2015, 1, 7, 10, 48, 21), datetime(2015, 1, 7, 10, 48, 25)) # edge case

		# Events for overlapping tests
		self.k = PyEvent(datetime(2015, 1, 7, 10, 48, 10), datetime(2015, 1, 7, 10, 48, 17)) # normal case: beginning before e, ending within e
		self.l = PyEvent(datetime(2015, 1, 7, 10, 48, 17), datetime(2015, 1, 7, 10, 48, 27)) # normal case: beginning within e, ending after e
		self.m = PyEvent(datetime(2015, 1, 7, 10, 48, 12), datetime(2015, 1, 7, 10, 48, 15)) # edge case: beginning before e, ending right at the beginning of e
		self.n = PyEvent(datetime(2015, 1, 7, 10, 48, 20), datetime(2015, 1, 7, 10, 48, 30)) # edge case: beginning right at the end of e, ending after e
		self.o = PyEvent(datetime(2015, 1, 7, 10, 48, 15), datetime(2015, 1, 7, 10, 48, 23)) # error case: beginning right at the beginning of e, ending after e
		self.p = PyEvent(datetime(2015, 1, 7, 10, 48, 10), datetime(2015, 1, 7, 10, 48, 20)) # error case: beginning before e, ending right at the ending of e
		self.q = PyEvent(datetime(2015, 1, 7, 10, 48, 10), datetime(2015, 1, 7, 10, 48, 30)) # error case: beginning before e, ending after e

	def test_constructor_with_two_arguments(self):
		''' Test constructor for an interval event '''
		self.assertEqual(self.e.startTime, datetime(2015, 1, 7, 10, 48, 15))
		self.assertEqual(self.e.endTime, datetime(2015, 1, 7, 10, 48, 20))

	def test_constructor_with_one_argument(self):
		''' Test constructor for a date event '''
		self.assertEqual(self.f.startTime, datetime(2015, 1, 7, 11, 48, 15))
		self.assertEqual(self.f.endTime, None)

	def test_constructor_error_wrong_startTime_type(self):
		self.assertRaises(TypeError, PyEvent, 1134, datetime(2015, 1, 7, 10, 48, 16))

	def test_constructor_error_wrong_endTime_type(self):
		self.assertRaises(TypeError, PyEvent, datetime(2015, 1, 7, 10, 48, 16), 'sdkfjdsf')

	def test_constructor_error_endTime_earlier_than_startTime(self):
		self.assertRaises(ValueError, PyEvent, datetime(2015, 1, 7, 10, 48, 16), datetime(2015, 1, 7, 10, 48, 4))

	def test_within(self):
		interval = self.e.within()
		self.assertEqual(interval[0], datetime(2015, 1, 7, 10, 48, 15))
		self.assertEqual(interval[1], datetime(2015, 1, 7, 10, 48, 20))

	def test_when(self):
		self.assertEqual(self.e.when(), datetime(2015, 1, 7, 10, 48, 15))

	def test_during_normal(self):
		''' Normal case: Event g is during Event e '''
		self.assertTrue(self.g.during(self.e))

	def test_during_edge_minimum(self):
		''' Edge case: Event h starts at the same time as Event e and ends within Event e '''
		self.assertTrue(self.h.during(self.e))

	def test_during_edge_maximum(self):
		''' Edge case: Event i starts during Event e and ends right at the same time as Event e '''
		self.assertTrue(self.i.during(self.e))

	def test_during_error_minimum(self):
		''' Error case: Event m starts before Event e and ends right at the beginning of Event e '''
		self.assertFalse(self.m.during(self.e))

	def test_during_error_minimum_2(self):
		''' Error case: Event k starts before Event e and ends during Event e '''
		self.assertFalse(self.k.during(self.e))

	def test_during_error_maximum(self):
		''' Error case: Event n starts right at the end of Event e and ends after Event e '''
		self.assertFalse(self.n.during(self.e))

	def test_during_error_maximum_2(self):
		''' Error case: Event l starts within Event e and ends after Event e '''
		self.assertFalse(self.l.during(self.e))

	def test_during_error_total(self):
		''' Error case: Event q starts before Event e and ends after Event e '''
		self.assertFalse(self.q.during(self.e))

	def test_before_normal(self):
		''' Normal case: Event r ends before Event e starts '''
		self.assertTrue(self.r.before(self.e))

	def test_before_edge(self):
		''' Edge case: Event s ends right before Event e starts '''
		self.assertTrue(self.s.before(self.e))

	def test_before_error_1(self):
		''' Error case: Event m ends right at the beginning of Event e '''
		self.assertFalse(self.m.before(self.e))

	def test_before_error_2(self):
		''' Error case: Event l ends after the beginning of Event e '''
		self.assertFalse(self.l.before(self.e))

	def test_after_normal(self):
		''' Normal case: Event t begins after Event e '''
		self.assertTrue(self.t.after(self.e))

	def test_after_edge(self):
		''' edge case: Event u begins right after Event e ends '''
		self.assertTrue(self.u.after(self.e))

	def test_after_error_1(self):
		''' Error case: Event n starts right at the end of Event e '''
		self.assertFalse(self.n.after(self.e))

	def test_after_error_2(self):
		''' Error case: Event k starts before the end of Event e '''
		self.assertFalse(self.k.after(self.e))

	def test_overlap_normal_1(self):
		''' Normal Case 1: Event k starts before Event e and ends during Event e '''
		self.assertTrue(self.k.overlap(self.e))

	def test_overlap_normal_2(self):
		''' Normal Case 2: Event l begins during Event e and ends after Event e '''
		self.assertTrue(self.l.overlap(self.e))

	def test_overlap_edge_1(self):
		''' Edge Case 1: Event m starts before Event e and ends right at the beginning of Event e '''
		self.assertTrue(self.m.overlap(self.e))

	def test_overlap_edge_2(self):
		''' Edge Case 1: Event n starts right at the end of Event e and ends after Event e '''
		self.assertTrue(self.n.overlap(self.e))

	def test_overlap_error_1(self):
		''' Error Case 1: Event o starts right at the beginning of Event e and ends after Event e '''
		self.assertFalse(self.o.overlap(self.e))

	def test_overlap_error_2(self):
		''' Error Case 2: Event p starts before Event e and ends at the same time as Event e '''
		self.assertFalse(self.p.overlap(self.e))

	def test_overlap_error_3(self):
		''' Error Case 3: Event q starts before Event e and ends after Event e '''
		self.assertFalse(self.q.overlap(self.e))

	def test_overlap_error_4(self):
		''' Error case 4: Event j has the same start time and end time as Event e '''
		self.assertFalse(self.j.overlap(self.e))

if __name__ == '__main__':
	unittest.main()