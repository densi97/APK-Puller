#!/usr/bin/env python3
from ppadb.client import Client as adb
import os

class APKPuller():

	def __init__(self):
		self.client = adb(host="127.0.0.1", port=5037)
		devices = self.client.devices()
		devicelist = ""
		if not devices:
			print("\033[1mNo devices found'\x1b[0m")
			exit()
		for count,d in enumerate(devices):
			devicelist += str(count + 1) + ". " + str(d) + "\n"
		device = input(devicelist + "\033[1mChoose device: \x1b[0m")
		assert(int(device) > 0)
		assert(int(device) <= len(devices))
		self.device = devices[int(device) - 1]
		print("Choosen device is: " +  str(device))

		apk_name = self.choose_apk()

		print("Choosen apk is: " + str(apk_name))

		if self.device.is_installed(str(apk_name)):
			print("\033[92m[*] trying to pull the apk\x1b[0m")
			self.pull_apk(apk_name)
			print("\033[92m[*] apk was pulled sucessfully\x1b[0m")
		else:
			print("\033[91mFailed to pull apk\x1b[0m")


	def choose_apk(self):
		installed_apps = self.device.shell("pm list packages")
		search = input("\033[1mWhich app do you want? \x1b[0m")
		hits = []
		for app in installed_apps.splitlines():
			if search in app:
				hits.append(app)
		if not hits:
			print("\033[91mI'm sorry but I can't find an app with that name.\x1b[0m")
			return self.choose_apk()
		else:
			hitlist = ""
			for count, app in enumerate(hits):
				hitlist += str(count + 1) + ". " + str(app)[8:] + "\n"
			app = input(hitlist + "\033[1mChoose the app you want to download: \x1b[0m")
			assert(int(app) > 0)
			assert(int(app) <= len(hits))
			apk_name = hits[int(app) - 1]
			return apk_name[8:]

	def pull_apk(self, package_name: str):
		path = self.device.shell("pm path " + package_name)
		paths = path.splitlines()
		path = paths[0][8:].strip()
		print(path)
		cwd = os.getcwd()
		self.device.pull(path, os.path.join(cwd,package_name + ".apk"))

		
if __name__ == '__main__':
	apkpuller = APKPuller()
