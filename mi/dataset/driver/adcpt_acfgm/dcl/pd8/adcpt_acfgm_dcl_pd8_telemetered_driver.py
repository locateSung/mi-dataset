#!/usr/bin/env python

"""
@package mi.dataset.driver.pco2a_a.dcl.pco2a_a_dcl_telemetered_driver
@file mi/dataset/driver/pco2a_a/dcl/pco2a_a_dcl_telemetered_driver.py
@author Sung Ahn
@brief Telemetered driver for pco2a_a_dcl data parser.

"""
from mi.dataset.parser.adcpt_acfgm_dcl_pd8 import DataParticleType, \
    AdcpPd8InstrumentDataParticle, AdcptPd8TelemeteredInstrumentDataParticle, AdcptPd8ARecoveredInstrumentDataParticle

from mi.dataset.driver.adcpt_acfgm.dcl.pd8.adcpt_acfgm_dcl_pd8_driver_common import process


def parse(basePythonCodePath, sourceFilePath, particleDataHdlrObj):
    process(sourceFilePath, particleDataHdlrObj, AdcptPd8TelemeteredInstrumentDataParticle)

    return particleDataHdlrObj