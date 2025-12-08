import json
import os
import re

# --- CONFIGURACIÓN ---
SEARCH_DIR = "target"
OUTPUT_DIR = "exports"
OUTPUT_FILE = "index_estatico.html"
# ---------------------

def embed_dbt_docs():
    print(f"🕵️  Analizando archivos en: {SEARCH_DIR}...")

    # 1. Leer HTML
    try:
        with open(os.path.join(SEARCH_DIR, "index.html"), "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ Error: No encuentro 'index.html'. Ejecuta 'dbt docs generate' primero.")
        return

    # 2. Leer JSONs
    try:
        with open(os.path.join(SEARCH_DIR, "manifest.json"), "r", encoding="utf-8") as f:
            manifest_json = json.dumps(json.load(f)).replace('\\', '\\\\').replace('"', '\\"')
        
        with open(os.path.join(SEARCH_DIR, "catalog.json"), "r", encoding="utf-8") as f:
            catalog_json = json.dumps(json.load(f)).replace('\\', '\\\\').replace('"', '\\"')
    except Exception as e:
        print(f"❌ Error leyendo JSONs: {e}")
        return

    # 3. REGEX ADAPTADA A TU VERSIÓN (DBT 1.10+)
    # El patrón que encontramos en tu log es: n = [o("manifest", "manifest.json" + t), o("catalog", "catalog.json" +
    # Esta regex busca exactamente esa estructura, ignorando espacios y nombres de variables (n, o, t).
    
    regex_pattern = r'([a-zA-Z0-9_$]+)\s*=\s*\[\s*([a-zA-Z0-9_$]+)\s*\(\s*["\']manifest["\']\s*,\s*["\']manifest\.json["\'][^\]]*\)\s*,\s*\2\s*\(\s*["\']catalog["\']\s*,\s*["\']catalog\.json["\'][^\]]*\)\s*\]'
    
    match = re.search(regex_pattern, html_content)

    if match:
        variable_name = match.group(1) # Debería ser "n" según tu log
        print(f"✅ ¡Patrón encontrado! Variable JS detectada: '{variable_name}'")
        
        # Creamos el reemplazo inyectando los JSONs
        # Importante: Mantenemos la estructura de objetos que espera la nueva versión
        new_js_code = (
            f'{variable_name}=[{{label: "manifest", data: JSON.parse("{manifest_json}")}}, '
            f'{{label: "catalog", data: JSON.parse("{catalog_json}")}}]'
        )
        
        # Reemplazamos en el HTML
        final_html = html_content.replace(match.group(0), new_js_code)
        
        # 4. Guardar
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        final_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"🎉 ¡ÉXITO! Archivo guardado en: {final_path}")
        print("   -> Ve a la carpeta exports, descarga el archivo y ábrelo.")
    
    else:
        print("⚠️  Aún no coincide la Regex. El código ha vuelto a cambiar.")
        # Debug por si acaso
        start = html_content.find("manifest.json")
        if start != -1:
            print(html_content[start-60 : start+60])

if __name__ == "__main__":
    embed_dbt_docs()