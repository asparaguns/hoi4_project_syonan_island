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
			for emdonym in self.lang_list:
				if emdonym["id"] != "00":
					self.endonym_lang = database.csv_filter(self.endonym_list, "id", self.endonym_id["id"])
					self.endonym_lang = database.csv_filter(self.endonym_lang, "lang", emdonym["id"])
					if len(self.endonym_lang) != 0:
						self.endonym_lang = self.endonym_lang[0]
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
				self.file.write(' STATE_{0}:0 "[{1}.GetStateName{1}]"\n'.format(self.endonym_id["id"], self.endonym_id["id"]))
			elif self.mode_name == "victory_points":
				self.file.write(' VICTORY_POINTS_{0}:0 "[{1}.GetVictoryPoints{1}]"\n'.format(self.endonym_id["id"], self.endonym_id["id"]))
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

class Language:
	def __init__(self, mod_name):
		self.mod_name = mod_name
		self.lang_list = database.csv_open(mod_name, "lang")
		
	def add_scripted_triger(self):
		self.file = open('./{0}/common/scripted_trigger/_{0}_endonym.txt'.format(self.mod_name), 'r', encoding='UTF-8')
		text_list = self.file.read().splitlines()
		lang_list = []
		not_have_lang = []
		not_have_lang_next = []
		new_text = []
		for endonym_lang in self.lang_list:
			if endonym_lang["id"] != "00":
				lang_list.append(endonym_lang["id"])
				if "endonym_{}_trigger = {{\t#{}".format(endonym_lang["id"], endonym_lang["name"]) not in text_list:
					not_have_lang.append(endonym_lang["id"])
		for i in not_have_lang:
			if lang_list[len(lang_list) - 1] != i:
				not_have_lang_next.append(lang_list[lang_list.index(i) + 1])
			else:
				last_lang = database.csv_filter(self.lang_list, "id", i)[0]
				text_list.append("endonym_{}_trigger = {{\t#{}".format(last_lang["id"], last_lang["name"]))
				text_list.append("}")
		text_list.reverse()
		i = 0
		for text in text_list:
			i += 1
			for lang in not_have_lang_next:
				lang_dict = database.csv_filter(self.lang_list, "id", lang)[0]
				not_have_lang_dict = database.csv_filter(self.lang_list, "id", not_have_lang[not_have_lang_next.index(lang)])[0]
				if "endonym_{}_trigger = {{\t#{}".format(lang_dict["id"], lang_dict["name"]) == text:
					tmp = "endonym_{}_trigger = {{\t#{}".format(not_have_lang_dict["id"], not_have_lang_dict["name"])
					text_list.insert(i, "}")
					text_list.insert(i + 1, "\tcontroller = {{\n\t\tOR = {{\n\t\t\thas_country_flag = endonym_{}_flag\n\t\t\tAND = {{\n\t\t\t\thas_endonym_lang_flag = no\n\t\t\t}}\n\t\t}}\n\t}}".format(not_have_lang_dict["id"]))
					text_list.insert(i + 2, tmp)
		text_list.reverse()
		self.file = open('./{0}/common/scripted_trigger/_{0}_endonym.txt'.format(self.mod_name), 'w', encoding='UTF-8')
		for line2 in text_list:
			self.file.write(line2)
			self.file.write("\n")
		
	def main(self):
		self.add_scripted_triger()
		

def add_sub_ideology(mod_name, mode_name):
	Localisation(mod_name, mode_name).main()
