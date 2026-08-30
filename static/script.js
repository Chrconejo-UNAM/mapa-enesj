// Lista de categorías y sus nodos correspondientes 
const categoriasNodos = {
    '📝 AULAS': [
        'III-201', 'III-202', 'III-301', 'III-302', 'III-303', 'III-304',
        'IV-301', 'IV-302', 'IV-303', 'IV-304', 'IV-305',
        'Salones de usos múltiples',
        'V-401', 'V-402', 'V-403', 'V-404', 'VI-201', 'VI-202', 'VI-203', 'VI-204',
        'VI-301', 'VI-302', 'VI-303', 'VI-304', 'VI-401', 'VI-402', 'VI-403', 'VI-404',
        'VI-PB01', 'VI-PB02', 'VI-PB03', 'VI-PB04'
    ],
    '🔬 LABORATORIOS': [
        'IV-101', 'IV-102', 'IV-103', 'V-101', 'V-102'
    ],
    '🖥️ LABORATORIOS DE CÓMPUTO': [
        'V-301', 'V-302', 'V-303', 'V-304'
    ],
    '📚 CID': [
        'CID planta baja', 'CID piso 1', 'CID piso 3', 'CID piso 4', 'PC Puma'
    ],
    '💼 SECRETARÍAS Y SERVICIOS': [
        'Cajas', 'Centro de lenguas', 'Dirección', 'Internacionalización', 'Lactancia', 'Médico', 'Nutrición', 'Objetos perdidos', 
        'Observatorio de negocios internacionales', 'Psicopedagogía', 'Recepción', 
        'Sala de juntas', 'Secretaría académica', 'Secretaría administrativa', 
        'Secretaría de atención a la comunidad y vinculación', 'Secretaría general', 'Servicios escolares', 'Tics', 'Unidad jurídica', 'Personas orientadoras de la comunidad' 
    ],
    '👨‍🏫 ZONA DE DOCENTES': [
        'Zona de docentes 1', 'Zona de docentes 2', 'Zona de docentes 3', 'Zona de docentes 4', 'Zona de docentes 5'
    ],
    '🌿 OTRAS ÁREAS': [
        'Ajedrez', 'Auditorio', 'Cafetería', 'Canchas', 'Deportes', 'Entrada', 
        'Entrada estacionamiento', 'Explanada', 'Gym al aire libre', 'Intendencia de obras', 
        'Jardineras', 'Juegos', 'Microondas', 'Mini circuito', 'Paneles solares',
        'Túnel de viento', 'Vitrinas'
    ]
};

const selectOrigen = document.getElementById('origen');
const selectDestino = document.getElementById('destino');

// Llenar las listas dinámicamente respetando las categorías
Object.keys(categoriasNodos).forEach(categoria => {
    let optgroupOrigen = `<optgroup label="${categoria}">`;
    let optgroupDestino = `<optgroup label="${categoria}">`;
    
    categoriasNodos[categoria].forEach(nodo => {
        optgroupOrigen += `<option value="${nodo}">${nodo}</option>`;
        optgroupDestino += `<option value="${nodo}">${nodo}</option>`;
    });

    optgroupOrigen += `</optgroup>`;
    optgroupDestino += `</optgroup>`;

    selectOrigen.innerHTML += optgroupOrigen;
    selectDestino.innerHTML += optgroupDestino;
});

// Función para trazar la ruta
async function trazarRuta() {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    const btn = document.getElementById('btn-trazar');
    
    // Ocultar todas las alertas antes de iniciar
    document.getElementById('alerta-error').style.display = 'none';
    document.getElementById('alerta-distancia').style.display = 'none';
    document.getElementById('alerta-camino').style.display = 'none';
    document.getElementById('alerta-info-inicial').style.display = 'none';

    if (origen === destino) {
        document.getElementById('alerta-info-inicial').style.display = 'block';
        document.getElementById('alerta-info-inicial').innerHTML = `📍🎯 ¡Ya estás aquí!: ${origen}`;
        return;
    }

    btn.innerText = '⏳ Dibujando la ruta...';
    btn.disabled = true;

    try {
        const response = await fetch('/api/trazar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, destino })
        });

        const data = await response.json();

        if (data.exito) {
            document.getElementById('alerta-distancia').style.display = 'block';
            document.getElementById('alerta-distancia').innerHTML = `✅ ¡Ruta Encontrada! Distancia aproximada: ${data.distancia} metros`;
            
            document.getElementById('alerta-camino').style.display = 'block';
            document.getElementById('alerta-camino').innerHTML = `🧭 <b>Camino a seguir:</b> ${data.camino}`;

            document.getElementById('mapa-img').src = data.imagen;
        } else {
            document.getElementById('alerta-error').style.display = 'block';
            document.getElementById('alerta-error').innerText = `❌ ${data.error}`;
        }
    } catch (error) {
        document.getElementById('alerta-error').style.display = 'block';
        document.getElementById('alerta-error').innerText = '❌ Error de conexión con el servidor.';
    }

    btn.innerText = 'Trazar Ruta';
    btn.disabled = false;
}
