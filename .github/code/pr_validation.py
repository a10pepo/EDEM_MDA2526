import os
import subprocess
import sys


ALLOWED_ROOT_FILES = {"README.md"}
ALLOWED_ROOT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def get_expected_deliverables():
    profesores_paths = [
        os.path.join(os.getcwd(), "PROFESORES/COMUN"),
        os.path.join(os.getcwd(), "PROFESORES/MIA"),
        os.path.join(os.getcwd(), "PROFESORES/MDA"),
    ]

    deliverables = []
    for profesores_path in profesores_paths:
        if not os.path.isdir(profesores_path):
            continue
        deliverables.extend(
            d
            for d in os.listdir(profesores_path)
            if os.path.isdir(os.path.join(profesores_path, d))
        )

    return {deliverable.lower() for deliverable in deliverables}


def validate_folder_structure(path, expected_deliverables):
    for student in os.listdir(path):
        student_path = os.path.join(path, student)
        if not os.path.isdir(student_path):
            continue

        for entry in os.listdir(student_path):
            entry_path = os.path.join(student_path, entry)
            if os.path.isdir(entry_path):
                if entry.lower() not in expected_deliverables:
                    print(
                        "Esta Carpeta no es correcta, comprueba el nombre exacto de la carpeta:",
                        entry,
                    )
                    sys.exit(1)
            elif (
                entry not in ALLOWED_ROOT_FILES
                and os.path.splitext(entry)[1].lower() not in ALLOWED_ROOT_EXTENSIONS
            ):
                print(
                    "Elimina el fichero fuera de la carpeta del usuario (solo README.md e imagenes estan permitidos):",
                    entry_path,
                )
                sys.exit(1)


def get_modified_files():
    diff_candidates = [
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        ["git", "diff", "--name-only", "HEAD^..HEAD"],
        ["git", "diff", "--name-only", "HEAD"],
    ]

    for command in diff_candidates:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    return []


def validate_modified_files(modified_files):
    print(f"\n🔍 Verificando archivos modificados... Total: {len(modified_files)}")

    profesores_files = [path for path in modified_files if path.startswith("PROFESORES/")]
    if profesores_files:
        print("\n❌ ERROR: No se permite modificar archivos en la carpeta PROFESORES")
        for path in profesores_files:
            print(f"  - {path}")
        sys.exit(1)

    alumnos_files = [path for path in modified_files if path.startswith("ALUMNOS/")]
    student_roots = set()
    subject_roots = set()

    for path in alumnos_files:
        parts = path.split("/")
        if len(parts) < 4:
            print(f"\n❌ ERROR: Ruta de alumno no válida: {path}")
            sys.exit(1)

        student_root = "/".join(parts[:3])
        student_roots.add(student_root)

        if len(parts) >= 5:
            subject_roots.add("/".join(parts[:4]))

    if len(student_roots) > 1:
        print("\n❌ ERROR: El PR modifica carpetas de más de un alumno")
        for path in sorted(student_roots):
            print(f"  - {path}")
        sys.exit(1)

    if len(subject_roots) > 1:
        print("\n❌ ERROR: Solo se permite entregar una asignatura por rama/PR")
        for path in sorted(subject_roots):
            print(f"  - {path}")
        sys.exit(1)

    if student_roots:
        print(f"✅ Cambios limitados a un único alumno: {sorted(student_roots)[0]}")
    if subject_roots:
        print(f"✅ Cambios limitados a una única asignatura: {sorted(subject_roots)[0]}")
    print("✅ No se detectaron modificaciones prohibidas en PROFESORES ni en otros alumnos")


if __name__ == "__main__":
    expected_deliverables = get_expected_deliverables()
    validate_modified_files(get_modified_files())
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAA"), expected_deliverables)
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MDAB"), expected_deliverables)
    validate_folder_structure(os.path.join(os.getcwd(), "ALUMNOS/MIA"), expected_deliverables)
