#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from src.preprocessing.create_labels import daytime_check


class DaytimeCheckTest(unittest.TestCase):
    def test_daytime_check(self):
        input_times = ['18:29:04', '07:46:31', '03:24:09', '00:29:44', '19:45:15']
        output_periods = ['Evening', 'Morning', 'Night', 'Night', 'Evening']

        function_output = []
        for time in input_times:
            function_output.append(daytime_check(time))

        self.assertEqual(output_periods, function_output)
    

if __name__ == '__main__':
    unittest.main()