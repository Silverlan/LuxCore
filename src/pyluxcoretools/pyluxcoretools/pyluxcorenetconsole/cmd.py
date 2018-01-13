#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################################################
# Copyright 1998-2018 by authors (see AUTHORS.txt)
#
#   This file is part of LuxCoreRender.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import argparse
import time
import logging
from functools import partial

import pyluxcore
import pyluxcoretools.utils.loghandler
import pyluxcoretools.pyluxcorenetconsole.renderfarm as renderfarm
import pyluxcoretools.pyluxcorenetnode.netbeacon as netbeacon

logger = logging.getLogger(pyluxcoretools.utils.loghandler.loggerName + ".luxcorenetconsole")

class LuxCoreNetConsole:
	def NodeDiscoveryCallBack(self, ipAddress, port):
		self.farm.DiscoveredNode(ipAddress, port, renderfarm.NodeDiscoveryType.AUTO_DISCOVERED)

	def Exec(self, argv):
		parser = argparse.ArgumentParser(description="Python LuxCoreNetConsole")

		self.farm = renderfarm.RenderFarm()

		# Start the beacon receiver
		beacon = netbeacon.NetBeaconReceiver(partial(LuxCoreNetConsole.NodeDiscoveryCallBack, self))
		beacon.Start()

		while True:
			time.sleep(1.0)
			print("RenderFarm[\n" + self.farm.ToString() + "]")

		# Start the beacon receiver
		beacon.Stop()

		logger.info("Done.")

def main(argv):
	try:
		pyluxcore.Init(pyluxcoretools.utils.loghandler.LuxCoreLogHandler)
		logger.info("LuxCore %s" % pyluxcore.Version())

		netConsole = LuxCoreNetConsole()
		netConsole.Exec(argv[1:])
	finally:
		pyluxcore.SetLogHandler(None)

if __name__ == "__main__":
	main(sys.argv)
