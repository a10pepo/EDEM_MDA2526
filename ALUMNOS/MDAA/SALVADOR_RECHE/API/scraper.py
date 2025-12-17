import requests
from bs4 import BeautifulSoup

def obtener_resumen_rfetm():
    url = "https://rfetm.es/resultados/2025-2026/view.php?liga=MQ==&grupo=0&subgrupo=S&jornada=0&sexo=M"
    response = requests.get(url)
    
    # Si la web responde bien (código 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Buscar el Líder (suele ser la primera fila de la tabla de clasificación)
        # Nota: Esto busca la tabla visualmente. En un caso real habría que ajustar los selectores CSS exactos
        filas = soup.find_all('tr')
        lider = "Desconocido"
        puntos = "0"
        
        # Buscamos filas que tengan datos numéricos de clasificación
        for fila in filas:
            datos = fila.find_all('td')
            if len(datos) > 8 and datos[0].text.strip() == '1': # Posición 1
                lider = datos[1].text.strip()
                puntos = datos[-1].text.strip()
                break
        
        return f"🏓 Actualización RFETM:\nEl líder es {lider} con {puntos} puntos.\n¡La Superdivisión está increiblemente que arde! 🔥"
    
    return "Error al leer la web de la RFETM"