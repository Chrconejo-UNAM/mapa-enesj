from fastapi import FastAPI
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def generar_grafo():
    G = nx.Graph()
    rutas_ps = [('Salones de usos múltiples', 'Escaleras 1 sótano', 11), ('Escaleras 1 sótano', 'Baños 1 sótano', 5), ('Escaleras 1 sótano', 'Cafetería', 17), ('Cafetería', 'Juegos', 43), ('Juegos', 'Explanada', 3), ('Explanada', 'Escaleras 2 sótano', 12), ('Juegos', 'Tics', 5), ('Juegos', 'Deportes', 8), ('Tics', 'Intendencia de obras', 15), ('Intendencia de obras', 'Túnel de viento', 35), ('Unidad de investigación de ortesis y prótesis', 'Escaleras 3 sótano', 5), ('Escaleras 3 sótano', 'Baños 2 sótano', 5)]
    rutas_pb = [('Auditorio', 'Escaleras 1 planta baja', 29), ('Escaleras 1 planta baja', 'Baños 1 planta baja', 5), ('Escaleras 1 planta baja', 'Entrada', 16), ('Entrada', 'Recepción', 23), ('Recepción','Baños 2 planta baja', 17), ('Baños 2 planta baja','Escaleras 2 planta baja', 5), ('Escaleras 2 planta baja','Vitrinas', 5), ('Vitrinas','VI-PB01', 43), ('Escaleras 2 sótano',  'VI-PB01', 15), ('Escaleras 2 sótano', 'Microondas', 30.5), ('VI-PB01','Nutrición', 13), ('VI-PB01','VI-PB02', 8), ('VI-PB02','Médico', 13), ('VI-PB02', 'Lactancia', 13), ('VI-PB02', 'VI-PB03', 8), ('VI-PB03', 'Psicología', 13), ('VI-PB03', 'VI-PB04', 8), ('VI-PB04', 'CID planta baja', 13), ('VI-PB04', 'Escaleras 3 planta baja', 11), ('Escaleras 3 planta baja', 'Baños 3 planta baja', 5), ('Mini circuito', 'Canchas', 25), ('Canchas', 'Microondas', 30), ('Entrada estacionamiento', 'Microondas', 8), ('Mini circuito', 'Unidad de investigación de ortesis y prótesis', 10)]
    rutas_p1 = [('Escaleras 1 piso 1', 'Baños 1 piso 1', 5), ('Escaleras 1 piso 1', 'IV-101', 9), ('IV-101', 'IV-102', 16), ('IV-102', 'IV-103', 17), ('IV-103', 'Escaleras 2 piso 1', 15), ('Escaleras 2 piso 1', 'Baños 2 piso 1', 5), ('Escaleras 2 piso 1', 'V-101', 10), ('V-101', 'V-102', 18), ('V-102', 'Ajedrez', 31.5), ('CID piso 1', 'Ajedrez', 14), ('Ajedrez', 'Escaleras 3 piso 1', 13), ('Escaleras 3 piso 1', 'Baños 3 piso 1', 5)]
    rutas_p2 = [('III-201', 'III-202', 8), ('III-202', 'Secretaría administrativa', 8), ('Secretaría administrativa', 'Escaleras 1 piso 2', 11), ('Escaleras 1 piso 2', 'Baños 1 piso 2', 5), ('Escaleras 1 piso 2', 'Secretaría académica', 15.5), ('Secretaría académica', 'Secretaría general', 6.5), ('Secretaría general', 'Sala de juntas', 20), ('Sala de juntas', 'Dirección', 7.5), ('Dirección', 'Escaleras 2 piso 2', 8.5), ('Escaleras 2 piso 2', 'Baños 2 piso 2', 5), ('Escaleras 2 piso 2', 'Secretaría de educación y vinculación', 16), ('Secretaría de educación y vinculación', 'Servicios escolares', 17.5), ('Servicios escolares', 'VI-201', 16), ('VI-201', 'VI-202', 8), ('VI-202', 'VI-203', 8), ('VI-203', 'VI-204', 8), ('VI-204', 'Escaleras 3 piso 2', 5), ('Escaleras 3 piso 2', 'Baños 3 piso 2', 5)]
    rutas_p3 = [('III-301', 'III-302', 8), ('III-302', 'III-303', 8), ('III-303', 'III-304', 8), ('III-304', 'Escaleras 1 piso 3', 5), ('Escaleras 1 piso 3', 'Baños 1 piso 3', 5), ('Escaleras 1 piso 3', 'IV-301', 5), ('IV-301', 'IV-302', 8), ('IV-302', 'IV-303', 8), ('IV-303', 'IV-304', 8), ('IV-304', 'IV-305', 8), ('IV-305', 'Escaleras 2 piso 3', 5), ('Escaleras 2 piso 3', 'Baños 2 piso 3', 5), ('Escaleras 2 piso 3', 'V-301', 5), ('V-301', 'V-302', 8), ('V-302', 'V-303', 8), ('V-303', 'V-304', 8), ('V-304', 'VI-301', 8), ('VI-301', 'VI-302', 8), ('VI-302', 'VI-303', 8), ('VI-303', 'CID piso 3', 14), ('VI-303', 'VI-304', 8), ('VI-304', 'Escaleras 3 piso 3', 5), ('Escaleras 3 piso 3', 'Baños 3 piso 3', 5)]
    rutas_p4 = [('Zona de docentes 1', 'Escaleras 1 piso 4', 16), ('Escaleras 1 piso 4', 'Baños 1 piso 4', 5), ('Escaleras 1 piso 4', 'Zona de docentes 2', 17), ('Zona de docentes 2', 'Zona de docentes 3', 8), ('Zona de docentes 3', 'Zona de docentes 4', 8), ('Zona de docentes 4', 'Zona de docentes 5', 8), ('Zona de docentes 5', 'Escaleras 2 piso 4', 12), ('Escaleras 2 piso 4', 'Baños 2 piso 4', 5), ('Escaleras 2 piso 4', 'V-401', 10), ('V-401', 'V-402', 8), ('V-402', 'V-403', 8), ('V-403', 'V-404', 8), ('V-404', 'VI-401', 8), ('VI-401', 'VI-402', 8), ('VI-402', 'CID piso 4', 14), ('VI-402', 'VI-403', 8), ('VI-403', 'VI-404', 8), ('VI-404', 'Escaleras 3 piso 4', 5), ('Escaleras 3 piso 4', 'Baños 3 piso 4', 5)]
    rutas_p5 = [('Paneles solares', 'Escaleras 1 piso 5', 5), ('Escaleras 1 piso 5', 'Baños 1 piso 5', 5), ('Escaleras 1 piso 5', 'Escaleras 2 piso 5', 55), ('Jardineras', 'Escaleras 2 piso 5', 12), ('Gym al aire libre', 'Escaleras 2 piso 5', 30.5 ), ('Escaleras 2 piso 5', 'Baños 2 piso 5', 5), ('Gym al aire libre', 'Escaleras 3 piso 5', 35)]
    escaleras = [('Escaleras 1 sótano', 'Escaleras 1 planta baja', 5), ('Escaleras 2 sótano', 'Vitrinas', 5), ('Escaleras 3 sótano', 'Escaleras 3 planta baja', 5), ('Escaleras 1 planta baja', 'Escaleras 1 piso 1', 5), ('Escaleras 2 planta baja', 'Escaleras 2 piso 1', 5), ('Escaleras 3 planta baja', 'Escaleras 3 piso 1', 5), ('Escaleras 1 piso 1', 'Escaleras 1 piso 2', 5), ('Escaleras 2 piso 1', 'Escaleras 2 piso 2', 5), ('Escaleras 3 piso 1', 'Escaleras 3 piso 2', 5), ('Escaleras 1 piso 2', 'Escaleras 1 piso 3', 5), ('Escaleras 2 piso 2', 'Escaleras 2 piso 3', 5), ('Escaleras 3 piso 2', 'Escaleras 3 piso 3', 5), ('Escaleras 1 piso 3', 'Escaleras 1 piso 4', 5), ('Escaleras 2 piso 3', 'Escaleras 2 piso 4', 5), ('Escaleras 3 piso 3', 'Escaleras 3 piso 4', 5), ('Escaleras 1 piso 4', 'Escaleras 1 piso 5', 5), ('Escaleras 2 piso 4', 'Escaleras 2 piso 5', 5), ('Escaleras 3 piso 4', 'Escaleras 3 piso 5', 5)]

    G.add_weighted_edges_from(rutas_ps + rutas_pb + rutas_p1 + rutas_p2 + rutas_p3 + rutas_p4 + rutas_p5 + escaleras)
    return G

pos = {
    'Escaleras 1 sótano': (7, -0.25), 'Escaleras 1 planta baja': (7, 0.5),
    'Escaleras 2 sótano': (35, 0.75), 'Escaleras 2 planta baja': (26, 1),
    'Escaleras 3 sótano': (50, 0.75), 'Escaleras 3 planta baja': (50, 1.25),
    'Salones de usos múltiples': (2, -0.25),
    'Cafetería': (21, 0.25), 'Juegos': (25.5, 0.375), 'Deportes': (30, 0.375), 'Explanada': (28, 0),
    'Tics': (24.25, 0.75), 'Intendencia de obras': (31, 0.75), 
    'Túnel de viento': (43, 0.5), 'Unidad de investigación de ortesis y prótesis': (48, 0.25),
    'Baños 1 sótano': (9, 0),
    'Baños 2 sótano': (51, 0.875),
    'Auditorio': (1, 0.5),
    'Entrada': (16, 0.75),
    'Recepción': (20, 1),
    'Baños 1 planta baja': (9, 0.625),
    'Baños 2 planta baja': (25, 1.125),
    'Baños 3 planta baja': (51, 1.375),
    'Vitrinas': (31, 1),
    'VI-PB01': (38, 1.25),
    'Microondas': (36, -0.5),
    'VI-PB02': (41, 1.25),
    'VI-PB03': (44, 1.25),
    'VI-PB04': (47, 1.25),
    'Nutrición': (38, 1),
    'Médico': (40, 1),
    'Lactancia': (42, 1),
    'Psicología': (44, 1),
    'CID planta baja': (46, 1),
    'Entrada estacionamiento': (33, -0.75),
    'Canchas': (50, -0.5),
    'Mini circuito': (53.5, 0),
    'Escaleras 1 piso 1': (7, 1.125),
    'Escaleras 2 piso 1': (26, 1.8),
    'Escaleras 3 piso 1': (50, 1.8),
    'Baños 1 piso 1': (9, 1.375),
    'Baños 2 piso 1': (27, 1.9),
    'Baños 3 piso 1': (51, 1.9),
    'IV-101': (13, 1.275), 'IV-102': (18.2, 1.5), 'IV-103': (22, 1.7),
    'V-101': (31, 1.8), 'V-102': (34, 1.8),
    'Ajedrez': (44, 1.8),
    'CID piso 1': (45, 1.5),
    'Escaleras 1 piso 2': (7, 1.8),
    'Escaleras 2 piso 2': (26, 2.30),
    'Escaleras 3 piso 2': (50, 2.45),
    'III-201': (-4, 1.75), 'III-202': (-1.5, 1.75), 'Secretaría administrativa': (4, 1.8),
    'Secretaría académica': (12, 1.95), 'Secretaría general': (15, 2.05), 'Sala de juntas': (19, 2.15), 'Dirección': (22, 2.25),
    'Secretaría de educación y vinculación': (30, 2.45), 'Servicios escolares': (34, 2.45),
    'VI-201': (38, 2.45), 'VI-202': (41, 2.45), 'VI-203': (44, 2.45), 'VI-204': (47, 2.45),
    'Baños 1 piso 2': (9, 1.95), 
    'Baños 2 piso 2': (27, 2.45), 
    'Baños 3 piso 2': (51, 2.55),
    'Escaleras 1 piso 3': (7, 2.3),
    'Escaleras 2 piso 3': (26, 2.9),
    'Escaleras 3 piso 3': (50, 3),
    'III-301': (-4, 2.3), 'III-302': (-1.5, 2.3), 'III-303': (1, 2.3), 'III-304': (4.5, 2.3),
    'IV-301': (12, 2.5), 'IV-302': (15, 2.60), 'IV-303': (17, 2.65), 'IV-304': (20, 2.72), 'IV-305': (22, 2.8),
    'V-301': (29, 3), 'V-302': (31, 3), 'V-303': (33, 3), 'V-304': (35.5, 3),
    'VI-301': (38, 3), 'VI-302': (41, 3), 'VI-303': (44, 3), 'VI-304': (47, 3),
    'CID piso 3': (45, 2.75),
    'Baños 1 piso 3': (9, 2.45), 
    'Baños 2 piso 3': (27, 3.1), 
    'Baños 3 piso 3': (51, 3.15),
    'Escaleras 1 piso 4': (7, 3),
    'Escaleras 2 piso 4': (26, 3.5),
    'Escaleras 3 piso 4': (50, 3.5),
    'Zona de docentes 1': (3, 3),
    'Zona de docentes 2': (14, 3.2), 'Zona de docentes 3': (17, 3.3), 'Zona de docentes 4': (20, 3.4), 'Zona de docentes 5': (22, 3.45),
    'V-401': (29, 3.5), 'V-402': (31, 3.5), 'V-403': (33, 3.5), 'V-404': (35.5, 3.5),
    'VI-401': (38, 3.5), 'VI-402': (41, 3.5), 'VI-403': (44, 3.5), 'VI-404': (47, 3.5),
    'CID piso 4': (42.7, 3.25),
    'Baños 1 piso 4': (9, 3.2), 
    'Baños 2 piso 4': (27, 3.65), 
    'Baños 3 piso 4': (51, 3.65),
    'Escaleras 1 piso 5': (7, 3.6),
    'Escaleras 2 piso 5': (26, 4),
    'Escaleras 3 piso 5': (50, 4),
    'Paneles solares': (0, 3.7),
    'Jardineras': (32, 3.9), 'Gym al aire libre': (39, 3.9),
    'Baños 1 piso 5': (9, 3.85), 'Baños 2 piso 5': (27, 4.2)
}

G = generar_grafo()

class PeticionRuta(BaseModel):
    origen: str
    destino: str

@app.get("/")
def serve_home():
    return FileResponse("index.html")

@app.post("/api/trazar")
def trazar_ruta(peticion: PeticionRuta):
    try:
        distancia, ruta = nx.bidirectional_dijkstra(G, source=peticion.origen, target=peticion.destino, weight='weight')
        
        img = Image.open('static/foto_enes_op.png').convert('RGBA')
        W, H = img.size
        
        # --- SUPERSAMPLING (Renderizar a 3x para bordes ultra suaves) ---
        factor = 3
        capa_ruta = Image.new('RGBA', (W * factor, H * factor), (255, 255, 255, 0))
        draw = ImageDraw.Draw(capa_ruta)

        izq, der, abajo, arriba = -8, 54, -1.5, 6

        def a_pixeles_escalado(x, y):
            px_x = int(((x - izq) / (der - izq)) * W) * factor
            px_y = int(H - (((y - abajo) / (arriba - abajo)) * H)) * factor
            return px_x, px_y

        # --- AJUSTES ESTILO STREAMLIT (TAMAÑOS MÁS GRANDES) ---
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

        # --- COLORES EXACTOS DE STREAMLIT ---
        color_linea = "#D4A106"
        color_inicio = "#002B5C"
        color_destino = "#D4A106"
        fondo_texto_transparente = (0, 43, 92, 170) 

        # 1. Dibujar líneas de la ruta
        for u, v in zip(ruta, ruta[1:]):
            x1, y1 = a_pixeles_escalado(pos[u][0], pos[u][1])
            x2, y2 = a_pixeles_escalado(pos[v][0], pos[v][1])
            draw.line([(x1, y1), (x2, y2)], fill=color_linea, width=grosor_linea)

        # 2. Dibujar nodos intermedios 
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

        def dibujar_etiqueta_inferior(texto, px, py):
            txt_y = py + desplazamiento_texto 
            bbox = draw.textbbox((px, txt_y), texto, font=fuente, anchor="mt")
            draw.rounded_rectangle(
                [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y],
                radius=radio_caja, fill=fondo_texto_transparente
            )
            draw.text((px, txt_y), texto, fill="white", font=fuente, anchor="mt")

        # 3. Dibujar Origen
        px_orig, py_orig = a_pixeles_escalado(pos[peticion.origen][0], pos[peticion.origen][1])
        draw.ellipse([(px_orig - radio_ext, py_orig - radio_ext), (px_orig + radio_ext, py_orig + radio_ext)], 
                     fill=color_inicio, outline="white", width=grosor_borde_ext)
        dibujar_etiqueta_inferior(f"Inicio: {peticion.origen}", px_orig, py_orig)

        # 4. Dibujar Destino
        px_dest, py_dest = a_pixeles_escalado(pos[peticion.destino][0], pos[peticion.destino][1])
        draw.ellipse([(px_dest - radio_ext, py_dest - radio_ext), (px_dest + radio_ext, py_dest + radio_ext)], 
                     fill=color_destino, outline="white", width=grosor_borde_ext)
        dibujar_etiqueta_inferior(f"Destino: {peticion.destino}", px_dest, py_dest)
        
        capa_ruta = capa_ruta.resize((W, H), Image.Resampling.LANCZOS)
        img_final = Image.alpha_composite(img, capa_ruta)
        
        buffer = io.BytesIO()
        img_final.save(buffer, format="WEBP", quality=85) 
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        return {
            "exito": True,
            "distancia": distancia,
            "camino": " ➔ ".join(ruta),
            "imagen": f"data:image/webp;base64,{img_b64}" 
        }

    except nx.NetworkXNoPath:
        return {"exito": False, "error": "No se encontró una ruta válida entre estos dos puntos."}
    except Exception as e:
        return {"exito": False, "error": str(e)}
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
