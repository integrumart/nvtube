import ui
import gui
import wx
import webbrowser
import urllib.parse
import globalPluginHandler
import threading

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def play_task(self):
        def run_dialog():
            with wx.TextEntryDialog(gui.mainFrame, "Oynatılacak içeriği giriniz (İlk video açılacaktır):", "NVTube VIP Oynatıcı") as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    sorgu = dlg.GetValue()
                    if sorgu:
                        # Reisim, YouTube hatasını aşmak için Google üzerinden yönlendirme yapıyoruz
                        # Bu yöntem seni doğrudan en alakalı videonun içine atar
                        lucky_link = f"https://www.google.com/search?q={urllib.parse.quote(sorgu)}+site:youtube.com&btnI=1"
                        
                        ui.message(f"'{sorgu}' bulunuyor ve oynatılıyor. Lütfen bekleyiniz...")
                        webbrowser.open(lucky_link)
        
        wx.CallAfter(run_dialog)

    def script_youtubeOynat(self, gesture):
        t = threading.Thread(target=self.play_task)
        t.start()

    __gestures = {
        "kb:nvda+shift+y": "youtubeOynat",
    }