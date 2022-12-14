# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import absolute_import
import unittest

from telemetry.internal.util import ts_proxy_server

class TsProxyServerTest(unittest.TestCase):
  def testSmokeStartingTsProxyServer(self):
    with ts_proxy_server.TsProxyServer() as server:
      self.assertIsNotNone(server.port)
    with ts_proxy_server.TsProxyServer(None, 37124, 37125) as server:
      self.assertIsNotNone(server.port)

  def testSmokeUpdatingOutboundPorts(self):
    with ts_proxy_server.TsProxyServer() as server:
      self.assertIsNotNone(server.port)
      server.UpdateOutboundPorts(31242, 14220)

  def testSmokeUpdateOutboundPortsInvalid(self):
    with ts_proxy_server.TsProxyServer() as server:
      self.assertIsNotNone(server.port)
      with self.assertRaises(AssertionError):
        server.UpdateOutboundPorts(31242, 'abcde')

  def testSmokeUpdateTrafficSettings(self):
    with ts_proxy_server.TsProxyServer() as server:
      server.UpdateTrafficSettings(round_trip_latency_ms=100)
      server.UpdateTrafficSettings(download_bandwidth_kbps=5000)
      server.UpdateTrafficSettings(upload_bandwidth_kbps=2000)

      self.assertEquals(server._rtt, 100)
      self.assertEquals(server._inbkps, 5000)
      self.assertEquals(server._outkbps, 2000)

      server.UpdateTrafficSettings(
          round_trip_latency_ms=200, download_bandwidth_kbps=500,
          upload_bandwidth_kbps=2000)
      self.assertEquals(server._rtt, 200)
      self.assertEquals(server._inbkps, 500)
      self.assertEquals(server._outkbps, 2000)
