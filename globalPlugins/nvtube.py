import wx
import threading
import urllib.parse
import webbrowser
import re
import requests
import globalPluginHandler
import gui
import scriptHandler
import ui
import speech

class SearchDialog(wx.Dialog):
	def __init__(self, parent, session):
		super().__init__(parent, title="NVTube v3.0 - Volkan Özdemir Yazılım Hizmetleri", size=(450, 220))
		self.session = session
		
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		lbl = wx.StaticText(panel, label="Aranacak içerik / Search query:")
		vbox.Add(lbl, flag=wx.ALL, border=10)

		self.text = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.text.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
		vbox.Add(self.text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, wx.ID_OK, label="Ara / Search")
		self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, label="Kapat / Close")
		self.donateBtn = wx.Button(panel, label="Bağış Yap / Donate")
		
		btnSizer.Add(self.okBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.donateBtn, 0, wx.ALL, 5)
		
		vbox.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		panel.SetSizer(vbox)
		
		self.okBtn.Bind(wx.EVT_BUTTON, self.on_enter)
		self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)
		self.Centre()
		self.text.SetFocus()

	def onDonate(self, event):
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")

	def on_enter(self, event):
		query = self.text.GetValue().strip()
		if not query:
			return
		
		speech.speakMessage(f"{query} aranıyor / searching...")
		threading.Thread(target=self.search_and_open, args=(query,), daemon=True).start()
		self.Close()

	def search_and_open(self, query):
		try:
			encoded = urllib.parse.quote_plus(query)
			url = f"https://www.youtube.com/results?search_query={encoded}"
			
			with self.session.get(url, timeout=10, stream=True) as response:
				v_id = None
				for chunk in response.iter_content(chunk_size=40960, decode_unicode=True):
					if not chunk: break
					match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', chunk)
					if match:
						v_id = match.group(1)
						break
			
			if v_id:
				webbrowser.open(f"https://www.yout-ube.com/watch?v={v_id}&autoplay=1")
			else:
				ui.message("Sonuç bulunamadı / No results found.")
		except:
			ui.message("Hata oluştu / Error occurred.")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = "NVTube v3.0"

	def __init__(self):
		super().__init__()
		self.session = requests.Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
		}

	@scriptHandler.script(
		description="YouTube Search",
		gesture="kb:NVDA+shift+y"
	)
	def script_openSearchDialog(self, gesture):
		wx.CallAfter(self.show_dialog)

	def show_dialog(self):
		dlg = SearchDialog(gui.mainFrame, self.session)
		dlg.ShowModal()
		dlg.Destroy()