import database
import edit

mod_name = "test"
mode_name = "state_names"

database.check_folder(mod_name)
database.csv_open_sort_edit(mod_name, "lang", "id")
database.csv_open_sort_edit(mod_name, "lang", "type")
database.csv_open_sort_edit(mod_name, "lang", "continent")
database.csv_open_sort_edit(mod_name, mode_name, "lang")
database.csv_open_sort_edit(mod_name, mode_name, "id")
edit.Localisation(mod_name, mode_name).main()
edit.Language(mod_name).main()