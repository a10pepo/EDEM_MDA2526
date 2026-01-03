import os
import sys
import subprocess

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

def check_profesores_modified():
    """
    Check if any files in PROFESORES folder are being modified in this PR/commit.
    Exits with error code 1 if any PROFESORES files are modified.
    """
    try:
        # Get the list of modified files
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'origin/main...HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        
        modified_files = result.stdout.strip().split('\n')
        
        # Check if any file is in PROFESORES folder
        profesores_files = [f for f in modified_files if f.startswith('PROFESORES/')]
        
        if profesores_files:
            print("\n❌ ERROR: No se permite modificar archivos en la carpeta PROFESORES")
            print("\nArchivos modificados en PROFESORES:")
            for file in profesores_files:
                print(f"  - {file}")
            print("\nPor favor, revierte estos cambios antes de continuar.")
            sys.exit(1)
        else:
            print("✅ No se detectaron modificaciones en la carpeta PROFESORES")
            
    except subprocess.CalledProcessError:
        # If git diff fails, we might not be in a PR context
        # In that case, we'll skip this check
        print("⚠️  No se pudo verificar archivos modificados (posiblemente no es un PR)")
        pass
     

if __name__ == "__main__":
    # First check if PROFESORES folder is being modified
    check_profesores_modified()
    
    # iterate over all the files in the folder
    # check if the file is a directory
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAA"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAB"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MIA"))
