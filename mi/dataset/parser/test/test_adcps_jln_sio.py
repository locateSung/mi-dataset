#!/usr/bin/env python

"""
@package mi.dataset.parser.test.test_adcps_jln_sio
@file mi/dataset/parser/test/test_adcps_jln_sio.py
@author Emily Hahn
@brief An set of tests for the adcps jln series through the sio dataset agent parser
"""

__author__ = 'Emily Hahn'
__license__ = 'Apache 2.0'

import os
from nose.plugins.attrib import attr

from mi.core.log import get_logger
log = get_logger()

from mi.core.exceptions import RecoverableSampleException
from mi.dataset.test.test_parser import ParserUnitTestCase, BASE_RESOURCE_PATH
from mi.dataset.parser.adcps_jln_sio import AdcpsJlnSioParser
from mi.dataset.dataset_parser import DataSetDriverConfigKeys

RESOURCE_PATH = os.path.join(BASE_RESOURCE_PATH, 'adcps_jln', 'sio', 'resource')


@attr('UNIT', group='mi')
class AdcpsJlnSioParserUnitTestCase(ParserUnitTestCase):

    def setUp(self):
        ParserUnitTestCase.setUp(self)
        self.config = \
            {
                DataSetDriverConfigKeys.PARTICLE_MODULE: 'mi.dataset.parser.adcps_jln_sio',
                DataSetDriverConfigKeys.PARTICLE_CLASS: 'AdcpsJlnSioDataParticle'
            }

    def test_simple(self):
        """
        Read test data from 2 files and compare the particles in .yml files.
        """
        with open(os.path.join(RESOURCE_PATH, 'node59p1_1.adcps.dat')) as stream_handle:

            parser = AdcpsJlnSioParser(self.config, stream_handle, self.exception_callback)

            particles = parser.get_records(2)
            self.assert_particles(particles, "adcps_telem_1.yml", RESOURCE_PATH)

            self.assertEqual(self.exception_callback_value, [])

        with open(os.path.join(RESOURCE_PATH, 'node59p1_2.adcps.dat')) as stream_handle:
            parser = AdcpsJlnSioParser(self.config, stream_handle, self.exception_callback)

            particles = parser.get_records(3)
            self.assert_particles(particles, "adcps_telem_2.yml", RESOURCE_PATH)

            self.assertEqual(self.exception_callback_value, [])

    def test_long_stream(self):
        """
        test a longer file
        """
        with open(os.path.join(RESOURCE_PATH, 'node59p1_0.adcps.dat')) as stream_handle:

            parser = AdcpsJlnSioParser(self.config, stream_handle, self.exception_callback)
            # request more particles than are available, make sure we only get the number in the file
            particles = parser.get_records(150)
            self.assertEqual(len(particles), 130)

            self.assertEqual(self.exception_callback_value, [])

    def test_bad_xml_checksum(self):
        """
        test an exception is raised for a bad number of bytes
        """
        with open(os.path.join(RESOURCE_PATH, 'node59p1_bad_xml_checksum.adcps.dat')) as stream_handle:

            parser = AdcpsJlnSioParser(self.config, stream_handle, self.exception_callback)
            # 2 records in file, first has bad xml checksum which should call exception
            particles = parser.get_records(2)
            self.assertEqual(len(particles), 1)

            self.assert_(isinstance(self.exception_callback_value[0], RecoverableSampleException))

    def test_adcps_error(self):
        """
        test an exception is raised for an adcps error message
        """
        with open(os.path.join(RESOURCE_PATH, 'node59p1_error.adcps.dat')) as stream_handle:

            parser = AdcpsJlnSioParser(self.config, stream_handle, self.exception_callback)
            # 2 records with error messages in them
            particles = parser.get_records(2)
            # make sure no particles were returned for the failure messages
            self.assertEqual(len(particles), 0)

            self.assert_(isinstance(self.exception_callback_value[0], RecoverableSampleException))
            self.assert_(isinstance(self.exception_callback_value[1], RecoverableSampleException))