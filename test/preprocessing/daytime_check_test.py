#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.preprocessing.dayperiodizer import DayPeriodizer


class DaytimeCheckTest(unittest.TestCase):
    def test_daytime_check(self):
        input_times = ['18:29:04', '07:46:31', '03:24:09', '00:29:44', '19:45:15']
        output_periods = ['Evening', 'Morning', 'Night', 'Night', 'Evening']

        periodizer = DayPeriodizer(6, 12, 18, 24)
        function_output = []
        for time in input_times:
            function_output.append(periodizer.day_periodize(time))

        self.assertEqual(output_periods, function_output)
    

if __name__ == '__main__':
    unittest.main()