import PySimpleGUI as sg
import re
import database
import edit

class ModSelectWindow:
	def __init__(self):
		self.layout = [
			[sg.Text("作成Mod")],
			[sg.Combo(database.mod_list(), key="mod_name", readonly=True)],
			[sg.Button("決定")]
		]
		self.window = sg.Window("作成Mod", self.layout, finalize = True)
	def main(self):
		while True:
			event, values = self.window.read()
			if event is None:
				sg.Popup("終了")
				break
			if event == "決定":
				if (values["mod_name"] == ""):
					sg.Popup("実装するModを選択してください")
				else:
					self.window.close()
					self.mod_name = values["mod_name"].replace('\n', '')
					AddCountryWindow(self.mod_name).main()
					
		self.window.close()

class AddCountryWindow:
	def __init__(self, mod_name):
		self.mod_name = mod_name
		self.layout0 = [
			[sg.Text("ID", size=(8, 1)), sg.InputText(key="id")],
			[sg.Text("和名", size=(8, 1)), sg.InputText(key="japanese")],
			[sg.Text("英名", size=(8, 1)), sg.InputText(key="english")],
			[sg.Text("言語", size=(8, 1)), sg.InputText(key="lang", default_text = "00")],
			[sg.Text("追加モード", size = (8, 1)), sg.Combo(["ステート名追加", "VP名追加"], key="mode", default_value = "ステート名追加", readonly = True)],
			[sg.Submit(button_text="追加")]
		]
		self.window = sg.Window("ステート追加", self.layout0, finalize=True)
	
	def main(self):
		while True:
			event, values = self.window.read()
			if event is None:
				break
			if event == "追加":
				self.add_list = {"id": int(values["id"]), "japanese": values["japanese"], "english": values["english"], "lang": values["lang"]}
				if values["mode"] == "ステート名追加":
					self.mode_name = "state_names"
					sg.Popup("ステート名追加")
				elif values["mode"] == "VP名追加":
					self.mode_name = "victory_points"
					sg.Popup("VP名追加")
				database.csv_edit(self.mod_name, self.mode_name, self.add_list)
				database.csv_open_sort_edit(self.mod_name, self.mode_name, "lang")
				database.csv_open_sort_edit(self.mod_name, self.mode_name, "id")
				edit.Localisation(self.mod_name, self.mode_name).main()
		self.window.close()

if __name__ == "__main__":
	ModSelectWindow().main()
