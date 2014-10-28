#!/usr/bin/env python

"""
@package mi.dataset.driver.adcpt_acfgm.dcl.pd8.adcp_acfgm_dcl_pd8_driver_common
@file mi/dataset/driver/adcpt_acfgm/dcl/pd8/adcp_acfgm_dcl_pd8_driver_common.py
@author Sung Ahn
@brief For creating a adcpt_acfgm_dcl_pd8_driver_common driver.

"""

from mi.core.log import get_logger
from mi.dataset.parser.adcpt_acfgm_dcl_pd8 import AdcpPd8Parser
from mi.dataset.dataset_driver import DataSetDriver
from mi.dataset.dataset_parser import DataSetDriverConfigKeys

log = get_logger()

from mi.dataset.parser.adcpt_acfgm_dcl_pd8 import DataParticleType, \
    AdcpPd8InstrumentDataParticle, AdcptPd8TelemeteredInstrumentDataParticle


MODULE_NAME = 'mi.dataset.parser.adcpt_acfgm_dcl_pd8'

def process(source_file_path, particle_data_hdlr_obj, particle_classes):
    with open(source_file_path, "r") as stream_handle:
        parser = AdcpPd8Parser(
            {DataSetDriverConfigKeys.PARTICLE_MODULE: MODULE_NAME,
             DataSetDriverConfigKeys.PARTICLE_CLASS: None,
             DataSetDriverConfigKeys.PARTICLE_CLASSES_DICT: particle_classes},
            stream_handle,
            lambda state, ingested: None,
            lambda data: log.trace("Found data: %s", data),
            lambda ex: particle_data_hdlr_obj.setParticleDataCaptureFailure()
        )
        driver = DataSetDriver(parser, particle_data_hdlr_obj)
        driver.processFileStream()