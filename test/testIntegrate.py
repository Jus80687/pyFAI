#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Azimuthal integration
#             https://forge.epn-campus.eu/projects/azimuthal
#
#    File: "$Id$"
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"test suite for masked arrays"

__author__ = "Jérôme Kieffer"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "16/11/2012"


import unittest
import os
import numpy
import logging, time
import sys
import fabio
from utilstest import UtilsTest, Rwp, getLogger
logger = getLogger(__file__)
pyFAI = sys.modules["pyFAI"]

if logger.getEffectiveLevel() <= logging.INFO:
    import pylab

class TestIntegrate1D(unittest.TestCase):
    npt = 1000
    img = UtilsTest.getimage("1883/Pilatus1M.edf")
    data = fabio.open(img).data
    ai = pyFAI.AzimuthalIntegrator(1.58323111834, 0.0334170169115, 0.0412277798782, 0.00648735642526, 0.00755810191106, 0.0, detector=pyFAI.detectors.Pilatus1M())
    ai.wavelength = 1e-10
    Rmax = 3


    def testQ(self):
        res = {}
        for m in ("numpy", "cython", "BBox" , "splitpixel", "lut", "lut_ocl"):
            res[m] = self.ai.integrate1d(self.data, self.npt, method=m, radial_range=(0.5, 5.8))
        for a in res:
            for b in res:
                R = Rwp(res[a], res[b])
                mesg = "testQ: %s vs %s measured R=%s<%s" % (a, b, R, self.Rmax)
                if R > self.Rmax:
                    logger.error(mesg)
                else:
                    logger.info(mesg)
                self.assertTrue(R <= self.Rmax, mesg)

    def testR(self):
        res = {}
        for m in ("numpy", "cython", "BBox" , "splitpixel", "lut", "lut_ocl"):
            res[m] = self.ai.integrate1d(self.data, self.npt, method=m, unit="r_mm", radial_range=(20, 150))
        for a in res:
            for b in res:
                R = Rwp(res[a], res[b])
                mesg = "testR: %s vs %s measured R=%s<%s" % (a, b, R, self.Rmax)
                if R > self.Rmax:
                    logger.error(mesg)
                else:
                    logger.info(mesg)
                self.assertTrue(R <= self.Rmax, mesg)
    def test2th(self):
        res = {}
        for m in ("numpy", "cython", "BBox" , "splitpixel", "lut", "lut_ocl"):
            res[m] = self.ai.integrate1d(self.data, self.npt, method=m, unit="2th_deg", radial_range=(0.5, 5.5))
        for a in res:
            for b in res:
                R = Rwp(res[a], res[b])
                mesg = "test2th: %s vs %s measured R=%s<%s" % (a, b, R, self.Rmax)
                if R > self.Rmax:
                    logger.error(mesg)
                else:
                    logger.info(mesg)
                self.assertTrue(R <= self.Rmax, mesg)


def test_suite_all_Integrate1d():
    testSuite = unittest.TestSuite()
    testSuite.addTest(TestIntegrate1D("testQ"))
    testSuite.addTest(TestIntegrate1D("testR"))
    testSuite.addTest(TestIntegrate1D("test2th"))
    return testSuite

if __name__ == '__main__':
    mysuite = test_suite_all_Integrate1d()
    runner = unittest.TextTestRunner()
    runner.run(mysuite)
#    if logger.getEffectiveLevel() == logging.DEBUG:
#        pylab.legend()
#        pylab.show()
#        raw_input()
#        pylab.clf()
