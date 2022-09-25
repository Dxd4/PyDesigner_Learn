from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sys, os
import requests
import re
import random
import time

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
 
	return os.path.join(base_path, relative_path)

class Ui(QtWidgets.QMainWindow):
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi(resource_path('VomAzur/VomAzur.ui'), self)
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.CloseButton.clicked.connect(self.close)
		self.show()
		self.progressBar.setValue(0)
		QtCore.QTimer.singleShot(0, self.get_views)
		QtCore.QTimer.singleShot(0, self.prgBar)
	def prgBar(self):
		percent = int(self.lcdNumber.value()/10000)
		cur_value = self.progressBar.value()
		if cur_value < percent:
			self.progressBar.setValue(cur_value+1)
			QtCore.QTimer.singleShot(10, self.prgBar)
	def get_views(self):
		url = "https://www.youtube.com/channel/UChO6RshLXnuce6KCkh8Pnyw/videos"
		headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
				}

		#youtube
		try:
			request = requests.get(url,headers=headers)
		except:
			reply = QMessageBox.question(self, 'ИНЕТ ВРУБИ', 'Интернета нет, ебланище',QMessageBox.Ok)
			sys.exit()
		text = request.content.decode("UTF-8").replace("\xa0", "")
		test = re.compile('viewCountText":{"simpleText":"\d+')
		text = test.findall(text)
		result = 0
		for x in text:
			result += int(x.replace('viewCountText":{"simpleText":"',''))
		self.label_views_1.setText(str(result))

		#youtube music
		result_music = result+random.randrange(50,1000)
		self.label_views_2.setText(str(result_music))

		#soundcloud
		url = "https://api-v2.soundcloud.com/users/481828179/tracks?representation=&client_id=n4QiowDdp97ZZ2pGZDX2ErvOZDzkXvYA&app_locale=en"
		request = requests.get(url,headers=headers)
		text = request.content.decode("UTF-8").replace("\xa0", "")
		test = re.compile('"playback_count":\d+')
		text = test.findall(text)
		result_snd = 0
		for x in text:
			result_snd += int(x.replace('"playback_count":',''))
		self.label_views_3.setText(str(result_snd))

		self.lcdNumber.display(result+result_music+result_snd)
		


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()