#!/usr/bin/env bash
apt-get install ipython
apt-get install python-pip
pip install selenium
mkdir /root/bin
cd /root/bin
wget https://github.com/mozilla/geckodriver/releases/download/v0.9.0/geckodriver-v0.9.0-linux64.tar.gz
tar -xvzf geckodriver-v0.9.0-linux64.tar.gz
rm geckodriver-v0.9.0-linux64.tar.gz
chmod +x geckodriver
cp geckodriver wires
export PATH=$PATH:/root/bin/wires
export PATH=$PATH:/root/bin/geckodriver

: '
ipython
%cpaste
## Paste the whole following content:
browser = None
def StartSelenium():
	import selenium
	from selenium import webdriver
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
	import binascii
	import hashlib
	firefox_capabilities = DesiredCapabilities.FIREFOX
	firefox_capabilities['marionette'] = True
	firefox_capabilities['binary'] = '/usr/bin/firefox'
	global browser
	browser = webdriver.Firefox(capabilities=firefox_capabilities)
	browser.get('https://www.google.com')
--
##End of paste
'