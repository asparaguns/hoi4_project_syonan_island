import database
import re

class Localisation:
	def __init__(self, mod_name, mode_name):
		self.mod_name = mod_name
		self.mode_name = mode_name
		self.endonym_list = database.csv_open(mod_name, mode_name)
		self.lang_list = database.csv_open(mod_name, "lang")
		
	def add_scripted_localisation(self):
		self.file = open('./{0}/common/scripted_localisation/_{0}_endonym_{1}.txt'.format(self.mod_name, self.mode_name), 'w', encoding='UTF-8')
		for self.endonym_id in database.csv_filter_sort(self.endonym_list, "lang", "00", "id"):
			self.file.write('defined_text = {\n')
			if self.mode_name == "state_names":
				self.file.write('\tname = GetStateName{0}\n'.format(self.endonym_id["id"]))
			elif self.mode_name == "victory_points":
				self.file.write('\tname = GetVictoryPoints{0}'.format(self.endonym_id["id"]))
			for self.endonym_lang in database.csv_filter_sort(self.endonym_list, "id", self.endonym_id["id"], "lang"):
				if self.endonym_lang["lang"] != "00":
					self.file.write('\ttext = {\n')
					self.file.write('\t\ttrigger = {{\tendonym_{}_trigger = yes\t}}\n'.format(self.endonym_lang["lang"]))
					if self.mode_name == "state_names":
						self.file.write('\t\tlocalization_key = STATE_{0}_{1}\n'.format(self.endonym_lang["id"], self.endonym_lang["lang"]))
					elif self.mode_name == "victory_points":
						self.file.write('\t\tlocalization_key = VICTORY_POINTS_{0}_{1}\n'.format(self.endonym_lang["id"], self.endonym_lang["lang"]))
					self.file.write('\t}\n')
			if self.mode_name == "state_names":
				self.file.write('\ttext = {{\tlocalization_key = STATE_{0}_default'.format(self.endonym_id["id"]))
			elif self.mode_name == "victory_points":
				self.file.write('\ttext = {{\tlocalization_key = VICTORY_POINTS_{0}_default'.format(self.endonym_id["id"]))
			self.file.write('\t}\n')
			self.file.write('}\n')
			
	def add_localisation_namespaces(self, lang_type):
		self.file = open('./{0}/localisation/{1}/map/{0}_{2}_l_{1}.yml'.format(self.mod_name, lang_type, self.mode_name), 'w', encoding = 'UTF-8-sig')
		self.file.write('l_{}:\n'.format(lang_type))
		for self.endonym_id in database.csv_filter_sort(self.endonym_list, "lang", "00", "id"):
			if self.mode_name == "state_names":
				self.file.write(' STATE_{0}:0 "[{1}.Controller.GetStateName{1}]"\n'.format(self.endonym_id["id"], self.endonym_id["id"]))
			elif self.mode_name == "victory_points":
				self.file.write(' VICTORY_POINTS_{0}:0 "[{1}.Controller.GetVictoryPoints{1}]"\n'.format(self.endonym_id["id"], self.endonym_id["id"]))
	def add_localisation_default(self, lang_type):
		self.file = open('./{0}/localisation/{1}/map/{0}_{2}_default_l_{1}.yml'.format(self.mod_name, lang_type, self.mode_name), 'w', encoding = 'UTF-8-sig')
		self.file.write('l_{}:\n'.format(lang_type))
		for self.endonym_id in database.csv_filter_sort(self.endonym_list, "lang", "00", "id"):
			if self.mode_name == "state_names":
				self.file.write(' STATE_{0}_default:0 "{1}"\n'.format(self.endonym_id["id"], self.endonym_id[lang_type]))
			elif self.mode_name == "victory_points":
				self.file.write(' VICTORY_POINTS_{0}_default:0 "{1}"\n'.format(self.endonym_id["id"], self.endonym_id[lang_type]))
	def add_localisation_endonym(self, lang_type):
		self.file = open('./{0}/localisation/{1}/map/{0}_{2}_endonym_l_{1}.yml'.format(self.mod_name, lang_type, self.mode_name), 'w', encoding = 'UTF-8-sig')
		self.file.write('l_{}:\n'.format(lang_type))
		for self.endonym_id in database.csv_filter_sort(self.endonym_list, "lang", "00", "id"):
			for self.endonym_lang in database.csv_filter_sort(self.endonym_list, "id", self.endonym_id["id"], "lang"):
				if self.endonym_lang["lang"] != "00":
					if self.mode_name == "state_names":
						self.file.write(' STATE_{0}_{1}:0 "{2}"\n'.format(self.endonym_lang["id"], self.endonym_lang["lang"], self.endonym_lang[lang_type]))
					elif self.mode_name == "victory_points":
						self.file.write(' VICTORY_POINTS_{0}_{1}:0 "{2}"\n'.format(self.endonym_lang["id"], self.endonym_lang["lang"], self.endonym_lang[lang_type]))
	def add_localisation(self, lang_type):
		self.add_localisation_namespaces(lang_type)
		self.add_localisation_default(lang_type)
		self.add_localisation_endonym(lang_type)
		
	def main(self):
		self.add_scripted_localisation()
		self.add_localisation("japanese")
		self.add_localisation("english")


def add_sub_ideology(mod_name, mode_name):
	Localisation(mod_name, mode_name).main()
