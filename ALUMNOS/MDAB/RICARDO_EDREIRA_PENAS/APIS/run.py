"""
Punto de entrada de la aplicación.
Ejecutar con: python run.py
"""

from app import crear_app
from app.config import es_modo_desarrollo

app = crear_app()

if __name__ == '__main__':
    modo_debug = es_modo_desarrollo()
    
    if modo_debug:
        print("🔧 Modo: DESARROLLO (los posts NO se publican realmente)")
    else:
        print("🚀 Modo: PRODUCCIÓN (los posts SE PUBLICAN en X)")
    
    print("\n🌐 Abre tu navegador en: http://127.0.0.1:5000\n")
    
    app.run(host='127.0.0.1', port=5000, debug=modo_debug)
