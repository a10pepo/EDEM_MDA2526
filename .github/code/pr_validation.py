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
        # Try multiple approaches to get modified files
        modified_files = []
        
        # Approach 1: Try origin/main...HEAD (works locally)
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'origin/main...HEAD'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        else:
            # Approach 2: Try HEAD^..HEAD (works for push events)
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD^..HEAD'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            else:
                # Approach 3: Get changed files from git status (last resort)
                result = subprocess.run(
                    ['git', 'diff', '--name-only', 'HEAD'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        
        print(f"\n🔍 Verificando archivos modificados... Total: {len(modified_files)}")
        
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
            
    except Exception as e:
        print("⚠️  No se pudo verificar archivos modificados")
        print(f"Error: {e}")
        pass
     

if __name__ == "__main__":
    # First check if PROFESORES folder is being modified
    check_profesores_modified()
    
    # iterate over all the files in the folder
    # check if the file is a directory
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAA"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAB"))
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MIA"))
