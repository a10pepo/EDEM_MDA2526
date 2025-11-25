import os

def validate_folder_structure(path):
    
    # Get only directories, not files like .gitkeep
    comun_path = os.path.join(os.getcwd(), "PROFESORES/COMUN")
    mia_path = os.path.join(os.getcwd(), "PROFESORES/MIA")
    mda_path = os.path.join(os.getcwd(), "PROFESORES/MDA")
    
    deliverables = [d for d in os.listdir(comun_path) if os.path.isdir(os.path.join(comun_path, d))]
    deliverables += [d for d in os.listdir(mia_path) if os.path.isdir(os.path.join(mia_path, d))]
    deliverables += [d for d in os.listdir(mda_path) if os.path.isdir(os.path.join(mda_path, d))]
    
    # Create a lowercase version for case-insensitive comparison
    deliverables_lower = [d.lower() for d in deliverables]
    
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            for user_file in os.listdir(full_path):
                user_path = os.path.join(full_path, user_file)
                if os.path.isdir(user_path):
                    if user_file.lower() not in deliverables_lower:
                        print("Esta Carpeta no es correcta, comprueba el nombre exacto de la carpeta: ", user_file)
                        exit(1)
                    else:
                        print("Carpeta correcta: ", user_file, " para el usuario ", file)
                else:
                    if "README.md" not in user_file:
                        print("Elimina el fichero fuera de la carpeta del usuario (solo README.md esta permitido): ", user_path)
     

if __name__ == "__main__":
    # iterate over all the files in the folder
    # check if the file is a directory
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAA"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAB"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MIA"))