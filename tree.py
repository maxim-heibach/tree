import os
import re

# Aufgabenteil a) und b)
def print_directory(path, indentation_level = 0, old_prefix = ""):
    entries = sorted(os.scandir(path), key = lambda f: f.name.lower()) 
    if len(entries) > 0:
        last_entry = entries[len(entries)-1]
    else: # falls Verzeichnis leer ist
        last_entry = 0    
    nfiles = 0
    ndirectories = 0
   
    for entry in entries: 
        # Definition des Präfixes für die Baumstruktur abhängig von der Position des Verzeichnisses bzw. der Datei.
        # chr(9472): Strich waagrecht ─ 
        # chr(9474): Strich senkrecht │  ->  "│   "
        # chr(9492): L-Verbindung └  ->  "└── "
        # chr(9500): T-Verbindung ├  ->  "├── "  
        # leere Element: "    "   
        if entry.name == last_entry.name:
            prefix = "└── "    
            # Präfix baut sich ab identation_level > 0 durch das alte Präfix auf. Hierzu wird die L- oder 
            # T- Verbindung zunächst entfernt und jenachdem durch ein senkrechtes oder leeres Element ergänzt, 
            # bevor die Verbindung wieder hinzugefügt wird. Hierdurch wird das Pattern der vorherigen Präfixe 
            # erhalten und das aktuelle Präfix an die jeweilige Situation angepasst. 
            if indentation_level > 0 and "└── " in old_prefix:
                prefix = re.sub("└── ", "", old_prefix) + "    " + "└── "  
            elif indentation_level > 0 and "├── " in old_prefix:
                prefix = re.sub("├── ", "", old_prefix) + "│   " + "└── "  
        else:
            prefix = "├── "
            if indentation_level > 0 and "└── " in old_prefix:
                prefix = re.sub("└── ", "", old_prefix) + "    " + "├── "  
            elif indentation_level > 0 and "├── " in old_prefix:
                prefix = re.sub("├── ", "", old_prefix) + "│   " + "├── "              
 
        # Verzeichnis und rekursiver Aufruf 
        if entry.is_dir():            
            print(prefix + entry.name + os.sep)
            ndirectories += 1
            sub_nfiles, sub_ndirectories = print_directory(entry.path, indentation_level + 1, old_prefix = prefix)
            nfiles += sub_nfiles
            ndirectories += sub_ndirectories
        
        # Datei 
        else:
            print(prefix + entry.name)
            nfiles += 1

    return nfiles, ndirectories

if __name__ == "__main__":
    nfiles, ndirectories = print_directory(".")

    # Aufgabenteil c)
    print("\n{} directories, {} files".format(ndirectories, nfiles))
