import wget
import tarfile
import os
from sys import platform

# Installs geckodriver in proper directory for reportscanner.py

geckodriver = "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"

def installGeckodriver():
	dir_path = "./src/geckodriver/"
	fname = "geckodriver-v0.26.0-linux64.tar.gz"
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
		os.chmod(dir_path, 755)
	wget.download(geckodriver, out=dir_path)
	tar_ref = tarfile.open(dir_path + fname)
	# print(dir_path)
	tar_ref.extractall(dir_path)
	tar_ref.close()
	os.remove(dir_path + fname)

if __name__ == '__main__':
	if platform == "linux" or platform == "linux2":
		installGeckodriver()