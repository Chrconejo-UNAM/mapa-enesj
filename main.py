# SISTEMA DE NAVEGACIÓN ENES JURIQUILLA (UNAM)

# Descripción 
# Backend en FastAPI utilizando teoría de grafos y el algoritmo de 
# Dijkstra para calcular y trazar rutas óptimas dentro de las instalaciones 
# de la ENES Juriquilla, generando mapas visuales dinámicos e instrucciones 
# de navegación detalladas

# INTEGRANTES: 
# - Ávila González Jimena
# - Macías García Mayra
# - Pérez Rodríguez José Luis
# - Ramírez Conejo Christian Alexis

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import networkx as nx
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import os
import uvicorn

# Configuración de la aplicación
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protocolos de seguridad
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; frame-ancestors 'none';"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response
    
# Montar la carpeta de archivos estáticos (CSS e imagenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Generar el grafo de la ENESJ
def generar_grafo():
    G = nx.Graph()

    rutas_ps = [('Salones de usos múltiples', 'Escaleras 1 sótano', 11), ('Escaleras 1 sótano', 'Cafetería', 17), ('Cafetería', 'Juegos', 43), ('Cafetería', 'Pared morada', 30), ('Pared morada', 'Explanada', 3), ('Pared morada', 'Elevador sótano', 5), ('Explanada', 'Escaleras 2 sótano', 12), ('Juegos', 'Tics', 5), ('Juegos', 'Deportes', 8), ('Tics', 'Intendencia de obras', 15), ('Intendencia de obras', 'Túnel de viento', 35), ('Unidad de investigación de órtesis y prótesis', 'Escaleras 3 sótano', 5)]

    rutas_pb = [('Auditorio', 'Escaleras 1 planta baja', 29), ('Escaleras 1 planta baja', 'Entrada', 16), ('Entrada', 'Recepción', 20), ('Escaleras 2 planta baja','Vitrinas', 5), ('Vitrinas','VI-PB01', 43), ('Escaleras 2 sótano',  'VI-PB01', 15), ('Escaleras 2 sótano', 'Microondas', 30.5), ('VI-PB01','Nutrición', 13), ('VI-PB01','VI-PB02', 8), ('VI-PB02','Médico', 13), ('VI-PB02', 'Lactancia', 13), ('VI-PB02', 'VI-PB03', 8), ('VI-PB03', 'Psicopedagogía', 13), ('VI-PB03', 'VI-PB04', 8), ('VI-PB04', 'CID planta baja', 13), ('VI-PB04', 'Escaleras 3 planta baja', 11), ('Mini circuito', 'Canchas', 25), ('Canchas', 'Microondas', 30), ('Entrada estacionamiento', 'Microondas', 8), ('Mini circuito', 'Unidad de investigación de órtesis y prótesis', 10)]

    rutas_p1 = [('Escaleras 1 piso 1', 'IV-101', 9), ('IV-101', 'IV-102', 17), ('IV-102', 'IV-103', 17), ('IV-103', 'Escaleras 2 piso 1', 15), ('Escaleras 2 piso 1', 'V-101', 10), ('V-101', 'V-102', 18), ('V-102', 'Ajedrez', 31.5), ('CID piso 1', 'Ajedrez', 14), ('Ajedrez', 'Escaleras 3 piso 1', 13)]

    rutas_p2 = [('III-201', 'III-202', 8), ('III-202', 'Secretaría administrativa', 8), ('Secretaría administrativa', 'Escaleras 1 piso 2', 11), ('Escaleras 1 piso 2', 'Secretaría académica', 15.5), ('Secretaría académica', 'Secretaría general', 6.5), ('Secretaría general', 'Sala de juntas', 19.9), ('Sala de juntas', 'Dirección', 7.5), ('Dirección', 'Escaleras 2 piso 2', 8.5), ('Escaleras 2 piso 2', 'Unidad Jurídica', 16), ('Secretaría de atención a la comunidad y vinculación', 'Servicios escolares', 17.5), ('Servicios escolares', 'VI-201', 16), ('VI-201', 'VI-202', 8), ('VI-202', 'VI-203', 8), ('VI-203', 'VI-204', 8), ('VI-204', 'Escaleras 3 piso 2', 5)]

    rutas_p3 = [('III-301', 'III-302', 8), ('III-302', 'III-303', 8), ('III-303', 'III-304', 8), ('III-304', 'Escaleras 1 piso 3', 5), ('Escaleras 1 piso 3', 'IV-301', 9), ('IV-301', 'IV-302', 10), ('IV-302', 'IV-303', 9.8), ('IV-303', 'IV-304', 10), ('IV-304', 'IV-305', 10), ('IV-305', 'Escaleras 2 piso 3', 9), ('Escaleras 2 piso 3', 'V-301', 5), ('V-301', 'V-302', 8), ('V-302', 'V-303', 8), ('V-303', 'V-304', 8), ('V-304', 'VI-301', 8), ('VI-301', 'VI-302', 8), ('VI-302', 'VI-303', 8), ('VI-303', 'CID piso 3', 14), ('VI-303', 'VI-304', 8), ('VI-304', 'Escaleras 3 piso 3', 5)]

    rutas_p4 = [('Zona de docentes 1', 'Escaleras 1 piso 4', 16), ('Escaleras 1 piso 4', 'Zona de docentes 2', 11), ('Zona de docentes 2', 'Zona de docentes 3', 10), ('Zona de docentes 3', 'Zona de docentes 4', 9.7), ('Zona de docentes 4', 'Zona de docentes 5', 10), ('Zona de docentes 5', 'Escaleras 2 piso 4', 17), ('Escaleras 2 piso 4', 'V-401', 10), ('V-401', 'V-402', 8), ('V-402', 'V-403', 8), ('V-403', 'V-404', 8), ('V-404', 'VI-401', 8), ('VI-401', 'VI-402', 8), ('VI-402', 'CID piso 4', 14), ('VI-402', 'VI-403', 8), ('VI-403', 'VI-404', 8), ('VI-404', 'Escaleras 3 piso 4', 5)]

    rutas_p5 = [('Paneles solares', 'Escaleras 1 piso 5', 5), ('Escaleras 1 piso 5', 'Escaleras 2 piso 5', 57.6), ('Jardineras', 'Escaleras 2 piso 5', 12), ('Gym al aire libre', 'Escaleras 2 piso 5', 30.5 ), ('Gym al aire libre', 'Escaleras 3 piso 5', 35)]

    escaleras = [('Elevador sótano', 'Escaleras 2 planta baja', 5), ('Escaleras 1 sótano', 'Escaleras 1 planta baja', 5), ('Escaleras 2 sótano', 'Vitrinas', 5), ('Escaleras 3 sótano', 'Escaleras 3 planta baja', 5), ('Escaleras 1 planta baja', 'Escaleras 1 piso 1', 5), ('Escaleras 2 planta baja', 'Escaleras 2 piso 1', 5), ('Escaleras 3 planta baja', 'Escaleras 3 piso 1', 5), ('Escaleras 1 piso 1', 'Escaleras 1 piso 2', 5), ('Escaleras 2 piso 1', 'Escaleras 2 piso 2', 5), ('Escaleras 3 piso 1', 'Escaleras 3 piso 2', 5), ('Escaleras 1 piso 2', 'Escaleras 1 piso 3', 5), ('Escaleras 2 piso 2', 'Escaleras 2 piso 3', 5), ('Escaleras 3 piso 2', 'Escaleras 3 piso 3', 5), ('Escaleras 1 piso 3', 'Escaleras 1 piso 4', 5), ('Escaleras 2 piso 3', 'Escaleras 2 piso 4', 5), ('Escaleras 3 piso 3', 'Escaleras 3 piso 4', 5), ('Escaleras 1 piso 4', 'Escaleras 1 piso 5', 5), ('Escaleras 2 piso 4', 'Escaleras 2 piso 5', 5), ('Escaleras 3 piso 4', 'Escaleras 3 piso 5', 5)]

    G.add_weighted_edges_from(rutas_ps + rutas_pb + rutas_p1 + rutas_p2 + rutas_p3 + rutas_p4 + rutas_p5 + escaleras)
    return G

# Posiciones de los nodos en el mapa (x, y)
pos = {
    # Sótano
    'Elevador sótano': (27.75, 0.375),
    'Escaleras 1 sótano': (5.8, -0.25), 
    'Escaleras 2 sótano': (35, 0.75), 
    'Escaleras 3 sótano': (50, 0.75), 

    'Salones de usos múltiples': (2, -0.25),
    'Cafetería': (21, 0.25), 
    'Tics': (24.25, 0.75), 
    'Juegos': (25.5, 0.5), 
    'Pared morada': (26, 0.25),
    'Explanada': (28, 0), 
    'Deportes': (30, 0.375), 
    'Intendencia de obras': (31, 0.75), 
    'Túnel de viento': (43, 0.5), 
    'Unidad de investigación de órtesis y prótesis': (48, 0.25),

    # Planta baja
    'Escaleras 1 planta baja': (5.7, 0.5),
    'Escaleras 2 planta baja': (27.75, 1),
    'Escaleras 3 planta baja': (50, 1.25),
    
    'Auditorio': (1, 0.5),
    'Entrada': (16, 0.75),
    'Recepción': (20, 1),
    'Vitrinas': (31, 1),
    'Entrada estacionamiento': (33, -0.75),
    'Microondas': (36, -0.5),
    'VI-PB01': (38, 1.25),
    'Nutrición': (38, 1),
    'Médico': (40, 1),
    'VI-PB02': (41, 1.25),
    'Lactancia': (42, 1),
    'VI-PB03': (44, 1.25),
    'Psicopedagogía': (44, 1),
    'CID planta baja': (46, 1),
    'VI-PB04': (47, 1.25),
    'Canchas': (50, -0.5),
    'Mini circuito': (53.5, 0),

    # Piso 1
    'Escaleras 1 piso 1': (5.6, 1.125),
    'Escaleras 2 piso 1': (27.75, 1.75),
    'Escaleras 3 piso 1': (50, 1.8),

    'IV-101': (13, 1.275), 
    'IV-102': (18.2, 1.5), 
    'IV-103': (22, 1.7),
    'V-101': (31, 1.8), 
    'V-102': (34, 1.8),
    'Ajedrez': (44, 1.8),
    'CID piso 1': (45, 1.5),

    # Piso 2
    'Escaleras 1 piso 2': (5.45, 1.8),
    'Escaleras 2 piso 2': (27.75, 2.40),
    'Escaleras 3 piso 2': (50, 2.45),

    'III-201': (-4, 1.75), 
    'III-202': (-1.5, 1.75), 
    'Secretaría administrativa': (4, 1.8),
    'Secretaría académica': (12, 1.95), 
    'Secretaría general': (15, 2.05), 
    'Sala de juntas': (19, 2.15), 
    'Dirección': (22, 2.25),
    'Unidad Jurídica': (29, 2.43),
    'Secretaría de atención a la comunidad y vinculación': (30, 2.45), 
    'Servicios escolares': (34, 2.45),
    'VI-201': (38, 2.45), 
    'VI-202': (41, 2.45), 
    'VI-203': (44, 2.45), 
    'VI-204': (47, 2.45),

    # Piso 3
    'Escaleras 1 piso 3': (5.35, 2.3),
    'Escaleras 2 piso 3': (27.75, 3),
    'Escaleras 3 piso 3': (50, 3),

    'III-301': (-4, 2.3), 
    'III-302': (-1.5, 2.3), 
    'III-303': (1, 2.3), 
    'III-304': (4.5, 2.3),
    'IV-301': (12, 2.5), 
    'IV-302': (15, 2.60), 
    'IV-303': (17, 2.65), 
    'IV-304': (20, 2.72), 
    'IV-305': (22, 2.8),
    'V-301': (29, 3), 
    'V-302': (31, 3), 
    'V-303': (33, 3), 
    'V-304': (35.5, 3),
    'VI-301': (38, 3), 
    'VI-302': (41, 3), 
    'VI-303': (44, 3), 
    'CID piso 3': (45, 2.75),
    'VI-304': (47, 3),

    # Piso 4
    'Escaleras 1 piso 4': (5.25, 3),
    'Escaleras 2 piso 4': (27.75, 3.5),
    'Escaleras 3 piso 4': (50, 3.5),

    'Zona de docentes 1': (3, 3),
    'Zona de docentes 2': (14, 3.2), 
    'Zona de docentes 3': (17, 3.3), 
    'Zona de docentes 4': (20, 3.4), 
    'Zona de docentes 5': (22, 3.45),
    'V-401': (29, 3.5), 
    'V-402': (31, 3.5), 
    'V-403': (33, 3.5), 
    'V-404': (35.5, 3.5),
    'VI-401': (38, 3.5), 
    'VI-402': (41, 3.5), 
    'CID piso 4': (42.7, 3.25),
    'VI-403': (44, 3.5), 
    'VI-404': (47, 3.5),

    # Piso 5
    'Escaleras 1 piso 5': (5.15, 3.6),
    'Escaleras 2 piso 5': (27.75, 4),
    'Escaleras 3 piso 5': (50, 4),

    'Paneles solares': (0, 3.7),
    'Jardineras': (32, 4.1), 
    'Gym al aire libre': (39, 3.9)
}

G = generar_grafo()


class PeticionRuta(BaseModel):
    origen: str
    destino: str

# Conexión con la interfaz web (HTML)
@app.get("/")
def serve_home():
    return FileResponse("index.html")

# Trazar la ruta entre dos puntos y generar la imagen con la ruta trazada
@app.post("/api/trazar")
def trazar_ruta(peticion: PeticionRuta):
    try:
        alias_nodos = {
            "Objetos perdidos": "Secretaría de atención a la comunidad y vinculación",
            "Unidad jurídica": "Secretaría de atención a la comunidad y vinculación",
            "Centro de lenguas": "Secretaría de atención a la comunidad y vinculación",
            "Personas orientadoras de la comunidad": "Zona de docentes 1",
            "Observatorio de negocios internacionales": "Zona de docentes 1",
            "Internacionalización": "Zona de docentes 1",
            "PC Puma": "CID planta baja",
            "Cajas": "Secretaría administrativa"
        }

        # Validación de nodos de origen y destino
        origen_real = alias_nodos.get(peticion.origen, peticion.origen)
        destino_real = alias_nodos.get(peticion.destino, peticion.destino)

        if not G.has_node(origen_real) or not G.has_node(destino_real):
            return {"exito": False, "error": "El punto de origen o destino no es válido."}
        
        distancia, ruta = nx.single_source_dijkstra(G, source=origen_real, target=destino_real, weight='weight')
        
        img = Image.open('static/foto_enes_op.webp').convert('RGBA')
        W, H = img.size
        
        # Aumentar la resolución de la capa de dibujo para mejorar la calidad de las líneas y el texto
        factor = 3
        capa_ruta = Image.new('RGBA', (W * factor, H * factor), (255, 255, 255, 0))
        draw = ImageDraw.Draw(capa_ruta)

        izq, der, abajo, arriba = -8, 54, -1.5, 6

        def a_pixeles_escalado(x, y):
            px_x = int(((x - izq) / (der - izq)) * W) * factor
            px_y = int(H - (((y - abajo) / (arriba - abajo)) * H)) * factor
            return px_x, px_y

        # Ajustar los parámetros de dibujo según el factor
        grosor_linea = 10 * factor        
        radio_int = 7 * factor            
        grosor_borde_int = 2 * factor     
        
        radio_ext = 16 * factor            
        grosor_borde_ext = 3 * factor     
        
        tamano_fuente = 20 * factor       
        desplazamiento_texto = 20 * factor 
        
        pad_x = 7 * factor                
        pad_y = 5 * factor                
        radio_caja = 8 * factor            

        color_linea = "#D4A106"
        color_inicio = "#002B5C"
        color_destino = "#D4A106"
        fondo_texto_transparente = (0, 43, 92, 170) 

        # Dibujar líneas de la ruta
        for u, v in zip(ruta, ruta[1:]):
            x1, y1 = a_pixeles_escalado(pos[u][0], pos[u][1])
            x2, y2 = a_pixeles_escalado(pos[v][0], pos[v][1])
            draw.line([(x1, y1), (x2, y2)], fill=color_linea, width=grosor_linea)

        # Dibujar nodos intermedios 
        for nodo in ruta[1:-1]:
            px, py = a_pixeles_escalado(pos[nodo][0], pos[nodo][1])
            draw.ellipse([(px - radio_int, py - radio_int), (px + radio_int, py + radio_int)], 
                         fill="white", outline=color_inicio, width=grosor_borde_int)
            
        try:
            fuentes_bonitas = ["arialbd.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"]
            for font_name in fuentes_bonitas:
                try:
                    fuente = ImageFont.truetype(font_name, tamano_fuente)
                    break
                except IOError:
                    continue
            else:
                fuente = ImageFont.load_default()
        except:
            fuente = ImageFont.load_default()

        # Funcion para dibujar etiquetas de manera inteligente, evitando que se superpongan con la ruta
        def dibujar_etiqueta_inteligente(texto, px, py, px_adyacente, py_adyacente):
            if py_adyacente > py:
                txt_y = py - desplazamiento_texto 
                anchor = "mb"
            else:
                txt_y = py + desplazamiento_texto 
                anchor = "mt"
                
            bbox = draw.textbbox((px, txt_y), texto, font=fuente, anchor=anchor)
            draw.rounded_rectangle(
                [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y],
                radius=radio_caja, fill=fondo_texto_transparente
            )
            draw.text((px, txt_y), texto, fill="white", font=fuente, anchor=anchor)

        # Dibujar Origen
        px_orig, py_orig = a_pixeles_escalado(pos[origen_real][0], pos[origen_real][1])
        draw.ellipse([(px_orig - radio_ext, py_orig - radio_ext), (px_orig + radio_ext, py_orig + radio_ext)], 
                     fill=color_inicio, outline="white", width=grosor_borde_ext)
        
        # Encontrar el nodo que le sigue al origen para calcular a dónde va la línea
        if len(ruta) > 1:
            px_orig_ady, py_orig_ady = a_pixeles_escalado(pos[ruta[1]][0], pos[ruta[1]][1])
        else:
            px_orig_ady, py_orig_ady = px_orig, py_orig - 1
            
        dibujar_etiqueta_inteligente(f"Inicio: {origen_real}", px_orig, py_orig, px_orig_ady, py_orig_ady)

        # Dibujar Destino
        px_dest, py_dest = a_pixeles_escalado(pos[destino_real][0], pos[destino_real][1])
        draw.ellipse([(px_dest - radio_ext, py_dest - radio_ext), (px_dest + radio_ext, py_dest + radio_ext)], 
                     fill=color_destino, outline="white", width=grosor_borde_ext)
        
        # Encontrar el nodo anterior al destino para calcular de dónde viene la línea
        if len(ruta) > 1:
            px_dest_ady, py_dest_ady = a_pixeles_escalado(pos[ruta[-2]][0], pos[ruta[-2]][1])
        else:
            px_dest_ady, py_dest_ady = px_dest, py_dest - 1

        dibujar_etiqueta_inteligente(f"Destino: {destino_real}", px_dest, py_dest, px_dest_ady, py_dest_ady)
        
        # Redimensionar la capa de dibujo con suavizado LANCZOS y pegar sobre el fondo
        capa_ruta = capa_ruta.resize((W, H), Image.Resampling.LANCZOS)
        img_final = Image.alpha_composite(img, capa_ruta)
        
        # Convertir la imagen final a formato WEBP y codificarla en base64
        buffer = io.BytesIO()
        img_final.save(buffer, format="WEBP", quality=85) 
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        # Mostrar nombres seleccionados (alias) y no reales 
        camino_mostrar = ruta.copy()
        camino_mostrar[0] = peticion.origen
        camino_mostrar[-1] = peticion.destino

        # Implementación de elevadores
        camino_resumido = []
        i = 0
        while i < len(camino_mostrar):
            nodo = camino_mostrar[i]
            
            # Revisamos si el nodo es una escalera
            if "Escaleras" in nodo:
                palabras = nodo.split()
                prefix = f"{palabras[0]} {palabras[1]}" 
                
                j = i
                # Avanzamos mientras los nodos siguientes tengan el mismo prefijo (escaleras)
                while j < len(camino_mostrar) and camino_mostrar[j].startswith(prefix):
                    j += 1
                
                nodos_escalera = j - i

                # Si solo hay un nodo de escalera, lo agregamos tal cual
                if nodos_escalera == 1:
                    camino_resumido.append(nodo)
                # Si hay más de un nodo de escalera, resumimos la instrucción
                else:
                    nodo_origen = camino_mostrar[i]
                    nodo_destino = camino_mostrar[j - 1]

                    nivel_original = nodo_destino.replace(prefix, "").strip().lower()
                    if "planta baja" in nivel_original:
                        destino_formato = f"la {nivel_original}"
                    else:
                        destino_formato = f"el {nivel_original}"
                    
                    # Excepción para el sótano de las escaleras 2 (sin elevador)
                    if "Escaleras 2 sótano" in [nodo_origen, nodo_destino]:
                        camino_resumido.append(f"🚶‍♂️ {prefix} hasta {destino_formato}")
                    else:
                        elevador_nombre = prefix.replace("Escaleras", "Elevador (o escaleras)")
                        camino_resumido.append(f"🛗 {elevador_nombre} hasta {destino_formato}")
                
                i = j
            else:
                camino_resumido.append(nodo)
                i += 1

        # Generar intrucciones resumidas para el usuario
        return {
            "exito": True,
            "distancia": round(distancia, 1),
            "camino": " ➔ ".join(camino_resumido),
            "imagen": f"data:image/webp;base64,{img_b64}" 
        }

    
    # Manejo de errores
    except nx.NetworkXNoPath:
        return {"exito": False, "error": "No se encontró una ruta válida entre estos dos puntos."}
    except Exception as e:
        return {"exito": False, "error": str(e)}
    
# Iniciar el servidor con uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    
