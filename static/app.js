// Estado de la aplicación
let reconocimientoVoz = null;
let grabando = false;
let reporteActual = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    inicializarApp();
});

function inicializarApp() {
    // Inicializar Speech Recognition
    inicializarReconocimientoVoz();
    
    // Event listeners
    document.getElementById('btn-voice').addEventListener('click', toggleGrabacion);
    document.getElementById('btn-enviar').addEventListener('click', enviarConsulta);
    document.getElementById('btn-limpiar').addEventListener('click', limpiarFormulario);
    document.getElementById('btn-ver-reporte').addEventListener('click', mostrarModalReporte);
    document.getElementById('btn-descargar-reporte').addEventListener('click', descargarReporte);
    
    // Modal
    document.querySelector('.close').addEventListener('click', cerrarModal);
    document.getElementById('modal-reporte').addEventListener('click', (e) => {
        if (e.target.id === 'modal-reporte') {
            cerrarModal();
        }
    });
    
    // Historial
    document.getElementById('historial-toggle').addEventListener('click', toggleHistorial);
    document.getElementById('close-historial').addEventListener('click', toggleHistorial);
    
    // Cargar historial inicial
    cargarHistorial();
    
    console.log('Aplicación inicializada correctamente');
}

// Speech Recognition
function inicializarReconocimientoVoz() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        reconocimientoVoz = new SpeechRecognition();
        
        reconocimientoVoz.continuous = false;
        reconocimientoVoz.interimResults = false;
        reconocimientoVoz.lang = 'es-ES';
        
        reconocimientoVoz.onstart = () => {
            grabando = true;
            actualizarUIGrabacion(true);
            console.log('Reconocimiento de voz iniciado');
        };
        
        reconocimientoVoz.onresult = (event) => {
            const texto = event.results[0][0].transcript;
            const input = document.getElementById('consulta-input');
            
            if (input.value.trim()) {
                input.value += ' ' + texto;
            } else {
                input.value = texto;
            }
            
            console.log('Texto reconocido:', texto);
        };
        
        reconocimientoVoz.onerror = (event) => {
            console.error('Error en reconocimiento de voz:', event.error);
            grabando = false;
            actualizarUIGrabacion(false);
            
            let mensaje = 'Error en el reconocimiento de voz';
            if (event.error === 'no-speech') {
                mensaje = 'No se detectó ninguna voz';
            } else if (event.error === 'not-allowed') {
                mensaje = 'Permiso de micrófono denegado';
            }
            
            mostrarNotificacion(mensaje, 'error');
        };
        
        reconocimientoVoz.onend = () => {
            grabando = false;
            actualizarUIGrabacion(false);
            console.log('Reconocimiento de voz finalizado');
        };
        
        console.log('Reconocimiento de voz inicializado');
    } else {
        console.warn('Reconocimiento de voz no soportado en este navegador');
        document.getElementById('btn-voice').disabled = true;
        document.getElementById('btn-voice').title = 'No soportado en este navegador';
    }
}

function toggleGrabacion() {
    if (!reconocimientoVoz) {
        mostrarNotificacion('Reconocimiento de voz no disponible', 'error');
        return;
    }
    
    if (grabando) {
        reconocimientoVoz.stop();
    } else {
        try {
            reconocimientoVoz.start();
        } catch (error) {
            console.error('Error al iniciar grabación:', error);
            mostrarNotificacion('Error al iniciar la grabación', 'error');
        }
    }
}

function actualizarUIGrabacion(activo) {
    const btnVoz = document.getElementById('btn-voice');
    const indicador = document.getElementById('recording-indicator');
    
    if (activo) {
        btnVoz.classList.add('recording');
        btnVoz.querySelector('.text').textContent = 'Detener';
        indicador.classList.remove('hidden');
    } else {
        btnVoz.classList.remove('recording');
        btnVoz.querySelector('.text').textContent = 'Hablar';
        indicador.classList.add('hidden');
    }
}

// Enviar consulta
async function enviarConsulta() {
    const consultaInput = document.getElementById('consulta-input');
    const consulta = consultaInput.value.trim();
    
    if (!consulta) {
        mostrarNotificacion('Por favor, escribe o graba tu consulta', 'warning');
        return;
    }
    
    // Mostrar loading
    mostrarLoading(true);
    ocultarRespuesta();
    
    try {
        const response = await fetch('/api/consulta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ consulta: consulta })
        });
        
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        
        const data = await response.json();
        
        // Guardar reporte actual
        reporteActual = data.reporte;
        
        // Mostrar respuesta
        mostrarRespuesta(data.respuesta);
        
        // Intentar comunicar con el avatar D-ID
        try {
            comunicarConAvatar(data.respuesta);
        } catch (avatarError) {
            console.warn('Error al comunicar con avatar:', avatarError);
        }
        
        // Actualizar historial
        cargarHistorial();
        
        mostrarNotificacion('Consulta procesada exitosamente', 'success');
        
    } catch (error) {
        console.error('Error al procesar consulta:', error);
        mostrarNotificacion('Error al procesar la consulta. Verifica tu conexión y la API key.', 'error');
    } finally {
        mostrarLoading(false);
    }
}

function comunicarConAvatar(texto) {
    // Intentar comunicar con el agente D-ID
    const didAgent = document.querySelector('did-agent');
    
    if (didAgent && typeof didAgent.speak === 'function') {
        didAgent.speak(texto);
    } else {
        console.log('Avatar D-ID no disponible o no soporta el método speak');
    }
}

function mostrarRespuesta(respuesta) {
    const container = document.getElementById('respuesta-container');
    const textoRespuesta = document.getElementById('respuesta-texto');
    
    textoRespuesta.textContent = respuesta;
    container.classList.remove('hidden');
    
    // Scroll suave a la respuesta
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function ocultarRespuesta() {
    document.getElementById('respuesta-container').classList.add('hidden');
}

function mostrarLoading(mostrar) {
    const loading = document.getElementById('loading');
    if (mostrar) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function limpiarFormulario() {
    document.getElementById('consulta-input').value = '';
    ocultarRespuesta();
    reporteActual = null;
    mostrarNotificacion('Formulario limpiado', 'info');
}

// Modal de reporte
function mostrarModalReporte() {
    if (!reporteActual) {
        mostrarNotificacion('No hay reporte disponible', 'warning');
        return;
    }
    
    const modal = document.getElementById('modal-reporte');
    const contenido = document.getElementById('reporte-contenido');
    
    contenido.innerHTML = generarHTMLReporte(reporteActual);
    modal.classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-reporte').classList.add('hidden');
}

function generarHTMLReporte(reporte) {
    const analisis = reporte.analisis || {};
    const fecha = new Date(reporte.timestamp).toLocaleString('es-ES');
    
    let html = `
        <div class="reporte-item">
            <h4>📅 Fecha y Hora</h4>
            <p>${fecha}</p>
        </div>
        
        <div class="reporte-item">
            <h4>💬 Consulta Original</h4>
            <p>${reporte.consulta}</p>
        </div>
        
        <div class="reporte-item">
            <h4>💊 Respuesta Proporcionada</h4>
            <p>${reporte.respuesta}</p>
        </div>
    `;
    
    if (analisis.resumen) {
        html += `
            <div class="reporte-item">
                <h4>📋 Resumen</h4>
                <p>${analisis.resumen}</p>
            </div>
        `;
    }
    
    if (analisis.sintomas) {
        html += `
            <div class="reporte-item">
                <h4>🩺 Síntomas Identificados</h4>
                <p>${analisis.sintomas}</p>
            </div>
        `;
    }
    
    if (analisis.recomendaciones) {
        html += `
            <div class="reporte-item">
                <h4>✅ Recomendaciones</h4>
                <p>${analisis.recomendaciones}</p>
            </div>
        `;
    }
    
    if (analisis.acciones) {
        html += `
            <div class="reporte-item">
                <h4>🎯 Acciones Sugeridas</h4>
                <p>${analisis.acciones}</p>
            </div>
        `;
    }
    
    if (analisis.urgencia) {
        const urgenciaColor = analisis.urgencia === 'Alto' ? 'danger' : 
                             analisis.urgencia === 'Medio' ? 'warning' : 'success';
        html += `
            <div class="reporte-item" style="border-left-color: var(--${urgenciaColor}-color)">
                <h4>⚠️ Nivel de Urgencia</h4>
                <p><strong>${analisis.urgencia}</strong></p>
            </div>
        `;
    }
    
    return html;
}

function descargarReporte() {
    if (!reporteActual) {
        mostrarNotificacion('No hay reporte para descargar', 'warning');
        return;
    }
    
    const texto = `
REPORTE DE CONSULTA MÉDICA
========================================

Fecha: ${new Date(reporteActual.timestamp).toLocaleString('es-ES')}

CONSULTA:
${reporteActual.consulta}

RESPUESTA:
${reporteActual.respuesta}

ANÁLISIS:
${JSON.stringify(reporteActual.analisis, null, 2)}

========================================
IMPORTANTE: Este reporte es informativo y no reemplaza una consulta médica profesional.
    `.trim();
    
    const blob = new Blob([texto], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reporte_medico_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    mostrarNotificacion('Reporte descargado', 'success');
}

// Historial
function toggleHistorial() {
    const sidebar = document.getElementById('historial-sidebar');
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('hidden');
}

async function cargarHistorial() {
    try {
        const response = await fetch('/api/historial');
        const data = await response.json();
        
        const contenido = document.getElementById('historial-contenido');
        
        if (data.reportes && data.reportes.length > 0) {
            contenido.innerHTML = data.reportes.map(reporte => {
                const fecha = new Date(reporte.timestamp).toLocaleString('es-ES', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                return `
                    <div class="historial-item" onclick="cargarConsultaHistorial('${reporte.timestamp}')">
                        <div class="fecha">${fecha}</div>
                        <div class="consulta">${reporte.consulta}</div>
                    </div>
                `;
            }).join('');
        } else {
            contenido.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No hay consultas previas</p>';
        }
    } catch (error) {
        console.error('Error al cargar historial:', error);
    }
}

function cargarConsultaHistorial(timestamp) {
    // Esta función se puede expandir para mostrar el detalle de una consulta del historial
    console.log('Cargar consulta:', timestamp);
    mostrarNotificacion('Funcionalidad de detalle en desarrollo', 'info');
}

// Notificaciones
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notif = document.createElement('div');
    notif.className = `notificacion notif-${tipo}`;
    notif.textContent = mensaje;
    
    // Estilos inline
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${tipo === 'success' ? '#10b981' : tipo === 'error' ? '#ef4444' : tipo === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        font-weight: 600;
    `;
    
    document.body.appendChild(notif);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// Agregar animaciones CSS para notificaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('App.js cargado correctamente');

