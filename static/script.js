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
        'Observatorio universitario de negocios internacionales', 'Psicopedagogía', 'Recepción', 
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

const inputOrigen = document.getElementById('origen');
const inputDestino = document.getElementById('destino');
const listaOrigen = document.getElementById('lista-origen');
const listaDestino = document.getElementById('lista-destino');

const masUsados = ['Entrada', 'Entrada estacionamiento', 'Cafetería', 'Auditorio', 'Servicios escolares', 'Unidad de investigación de órtesis y prótesis'];

function generarHTMLOpciones() {
    let html = `<div class="optgroup-label">⭐ MÁS USADOS</div>`;
    masUsados.forEach(nodo => {
        html += `<div class="opcion-item" data-value="${nodo}">${nodo}</div>`;
    });

    Object.keys(categoriasNodos).forEach(categoria => {
        html += `<div class="optgroup-label">${categoria}</div>`;
        categoriasNodos[categoria].forEach(nodo => {
            html += `<div class="opcion-item" data-value="${nodo}">${nodo}</div>`;
        });
    });
    return html;
}

const htmlOpciones = generarHTMLOpciones();
listaOrigen.innerHTML = htmlOpciones;
listaDestino.innerHTML = htmlOpciones;

// Configurar la lógica de búsqueda, click y teclado
function configurarBuscador(input, lista) {
    input.addEventListener('focus', () => {
        lista.classList.add('activa');
        filtrarLista(input, lista);
    });

    input.addEventListener('input', () => {
        lista.classList.add('activa');
        filtrarLista(input, lista);
    });

    lista.addEventListener('mousedown', (e) => {
        if (e.target.classList.contains('opcion-item')) {
            input.value = e.target.getAttribute('data-value');
            lista.classList.remove('activa');
        }
    });

    input.addEventListener('blur', () => {
        setTimeout(() => lista.classList.remove('activa'), 150);
    });
}

// Función que oculta los elementos que no coinciden con la búsqueda
function filtrarLista(input, lista) {
    const texto = input.value.toLowerCase();
    const items = lista.querySelectorAll('.opcion-item');
    const labels = lista.querySelectorAll('.optgroup-label');

    items.forEach(item => {
        if (item.innerText.toLowerCase().includes(texto)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });

    labels.forEach(label => {
        let next = label.nextElementSibling;
        let tieneVisibles = false;
        while (next && next.classList.contains('opcion-item')) {
            if (next.style.display === 'block') tieneVisibles = true;
            next = next.nextElementSibling;
        }
        label.style.display = tieneVisibles ? 'block' : 'none';
    });
}

configurarBuscador(inputOrigen, listaOrigen);
configurarBuscador(inputDestino, listaDestino);

// Lectura de parámetros desde la URL para prellenar los campos de origen y destino 

const parametrosURL = new URLSearchParams(window.location.search);

// Extraer los valores (ej. ?origen=Cafetería&destino=Auditorio)
const origenDesdeQR = parametrosURL.get('origen');
const destinoDesdeQR = parametrosURL.get('destino');

function esLugarValido(lugar) {
    let valido = false;
    Object.values(categoriasNodos).forEach(nodos => {
        if (nodos.includes(lugar)) {
            valido = true;
        }
    });
    return valido;
}

if (origenDesdeQR && esLugarValido(origenDesdeQR)) {
    inputOrigen.value = origenDesdeQR;
} else {
    inputOrigen.value = "Entrada"; 
}

if (destinoDesdeQR && esLugarValido(destinoDesdeQR)) {
    inputDestino.value = destinoDesdeQR;
}

// Función para trazar la ruta
async function trazarRuta() {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    const btn = document.getElementById('btn-trazar');
    
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
