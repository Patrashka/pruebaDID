// ===== CONFIGURACIÓN GLOBAL =====
const CONFIG = {
    API_BASE_URL: window.location.origin,
    SESSION_ID: 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
    VOICE_RECOGNITION_SUPPORTED: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
};

// ===== ESTADO DE LA APLICACIÓN =====
let appState = {
    isRecording: false,
    recognition: null,
    conversationHistory: [],
    currentReport: '',
    avatarLoaded: false
};

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏥 Inicializando Consulta Médica Virtual...');
    
    initializeApp();
    setupEventListeners();
    updateCurrentTime();
    initializeVoiceRecognition();
    
    // Actualizar hora cada minuto
    setInterval(updateCurrentTime, 60000);
    
    console.log('✅ Aplicación inicializada correctamente');
});

// ===== INICIALIZACIÓN DE LA APLICACIÓN =====
function initializeApp() {
    // Verificar soporte de reconocimiento de voz
    if (!CONFIG.VOICE_RECOGNITION_SUPPORTED) {
        console.warn('⚠️ Reconocimiento de voz no soportado en este navegador');
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) {
            voiceBtn.style.display = 'none';
        }
    }
    
    // Configurar el estado inicial del avatar
    updateAvatarStatus('connecting', 'Conectando...');
    
    // Configurar el textarea para auto-resize
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('input', autoResizeTextarea);
    }
}

// ===== CONFIGURACIÓN DE EVENT LISTENERS =====
function setupEventListeners() {
    // Botón de envío
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
    
    // Botón de voz
    const voiceBtn = document.getElementById('voice-btn');
    if (voiceBtn) {
        voiceBtn.addEventListener('click', toggleVoiceRecording);
    }
    
    // Enter para enviar mensaje
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
    
    // Event listeners para D-ID
    setupDIDEventListeners();
}

// ===== CONFIGURACIÓN DE EVENT LISTENERS PARA D-ID =====
function setupDIDEventListeners() {
    // Escuchar eventos del avatar D-ID
    window.addEventListener('message', function(event) {
        if (event.origin !== 'https://agent.d-id.com') return;
        
        const data = event.data;
        console.log('📡 Evento D-ID recibido:', data);
        
        switch (data.type) {
            case 'agent:ready':
                handleAvatarReady();
                break;
            case 'agent:speaking':
                handleAvatarSpeaking();
                break;
            case 'agent:stopped':
                handleAvatarStopped();
                break;
            case 'agent:error':
                handleAvatarError(data.error);
                break;
        }
    });
}

// ===== MANEJO DE EVENTOS DEL AVATAR D-ID =====
function handleAvatarReady() {
    console.log('✅ Avatar D-ID listo');
    updateAvatarStatus('online', 'Avatar conectado');
    appState.avatarLoaded = true;
    
    // Ocultar loading spinner
    const loadingElement = document.querySelector('.avatar-loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

function handleAvatarSpeaking() {
    console.log('🗣️ Avatar hablando');
    updateAvatarStatus('online', 'Avatar hablando...');
}

function handleAvatarStopped() {
    console.log('🔇 Avatar detenido');
    updateAvatarStatus('online', 'Avatar conectado');
}

function handleAvatarError(error) {
    console.error('❌ Error en avatar D-ID:', error);
    updateAvatarStatus('offline', 'Error en avatar');
}

// ===== ACTUALIZACIÓN DEL ESTADO DEL AVATAR =====
function updateAvatarStatus(status, text) {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');
    
    if (statusIndicator) {
        statusIndicator.className = `status-indicator ${status}`;
    }
    
    if (statusText) {
        statusText.textContent = text;
    }
}

// ===== RECONOCIMIENTO DE VOZ =====
function initializeVoiceRecognition() {
    if (!CONFIG.VOICE_RECOGNITION_SUPPORTED) return;
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    appState.recognition = new SpeechRecognition();
    
    appState.recognition.continuous = false;
    appState.recognition.interimResults = false;
    appState.recognition.lang = 'es-ES';
    
    appState.recognition.onstart = function() {
        console.log('🎤 Iniciando reconocimiento de voz...');
        appState.isRecording = true;
        updateVoiceUI(true);
    };
    
    appState.recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        console.log('🎤 Texto reconocido:', transcript);
        
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            messageInput.value = transcript;
            autoResizeTextarea();
        }
        
        appState.isRecording = false;
        updateVoiceUI(false);
    };
    
    appState.recognition.onerror = function(event) {
        console.error('❌ Error en reconocimiento de voz:', event.error);
        appState.isRecording = false;
        updateVoiceUI(false);
        
        showNotification('Error en reconocimiento de voz: ' + event.error, 'error');
    };
    
    appState.recognition.onend = function() {
        console.log('🎤 Reconocimiento de voz finalizado');
        appState.isRecording = false;
        updateVoiceUI(false);
    };
}

function toggleVoiceRecording() {
    if (!CONFIG.VOICE_RECOGNITION_SUPPORTED) {
        showNotification('Reconocimiento de voz no soportado en este navegador', 'warning');
        return;
    }
    
    if (appState.isRecording) {
        appState.recognition.stop();
    } else {
        appState.recognition.start();
    }
}

function updateVoiceUI(isRecording) {
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    
    if (voiceBtn) {
        if (isRecording) {
            voiceBtn.classList.add('recording');
            voiceBtn.title = 'Detener grabación';
        } else {
            voiceBtn.classList.remove('recording');
            voiceBtn.title = 'Grabar audio';
        }
    }
    
    if (voiceStatus) {
        voiceStatus.style.display = isRecording ? 'flex' : 'none';
    }
}

// ===== ENVÍO DE MENSAJES =====
async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) {
        showNotification('Por favor, escribe tu consulta médica', 'warning');
        return;
    }
    
    // Agregar mensaje del usuario al chat
    addMessageToChat(message, 'user');
    
    // Limpiar input
    messageInput.value = '';
    autoResizeTextarea();
    
    // Deshabilitar botón de envío
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.textContent = '⏳';
    }
    
    try {
        // Enviar consulta al backend
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/ai/voice-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: CONFIG.SESSION_ID
            })
        });
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        // Agregar respuesta del bot al chat
        addMessageToChat(data.ai_response, 'bot');
        
        // Actualizar reporte médico
        updateMedicalReport(data.summary);
        
        // Reproducir audio si está disponible
        if (data.audio_file) {
            playAudioResponse(data.audio_file);
        }
        
        // Actualizar historial de conversación
        appState.conversationHistory.push({
            role: 'user',
            content: message
        });
        appState.conversationHistory.push({
            role: 'assistant',
            content: data.ai_response
        });
        
    } catch (error) {
        console.error('❌ Error al enviar mensaje:', error);
        showNotification('Error al procesar la consulta. Verifica tu conexión.', 'error');
        
        // Agregar mensaje de error al chat
        addMessageToChat('Lo siento, hubo un error al procesar tu consulta. Por favor, inténtalo de nuevo.', 'bot');
    } finally {
        // Rehabilitar botón de envío
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.textContent = '📤';
        }
    }
}

// ===== AGREGAR MENSAJES AL CHAT =====
function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'bot') {
        messageContent.innerHTML = `<strong>Asistente Médico:</strong> ${message}`;
    } else {
        messageContent.textContent = message;
    }
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTimeString();
    
    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(messageTime);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll al final
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Animación de entrada
    messageDiv.classList.add('fade-in');
}

// ===== ACTUALIZACIÓN DEL REPORTE MÉDICO =====
function updateMedicalReport(summary) {
    const reportContent = document.getElementById('report-content');
    if (!reportContent) return;
    
    if (summary && summary.trim()) {
        appState.currentReport = summary;
        
        // Limpiar placeholder si existe
        const placeholder = reportContent.querySelector('.report-placeholder');
        if (placeholder) {
            placeholder.remove();
        }
        
        // Agregar nuevo resumen
        const summaryDiv = document.createElement('div');
        summaryDiv.className = 'medical-summary slide-up';
        summaryDiv.innerHTML = `
            <div class="summary-header">
                <span class="summary-time">${getCurrentTimeString()}</span>
            </div>
            <div class="summary-content">${summary}</div>
        `;
        
        reportContent.appendChild(summaryDiv);
        
        // Scroll al final del reporte
        reportContent.scrollTop = reportContent.scrollHeight;
    }
}

// ===== REPRODUCCIÓN DE AUDIO =====
function playAudioResponse(audioFile) {
    const audio = new Audio(`${CONFIG.API_BASE_URL}/tmp/${audioFile}`);
    
    audio.onloadstart = function() {
        console.log('🔊 Cargando audio...');
    };
    
    audio.oncanplay = function() {
        console.log('🔊 Reproduciendo audio...');
        audio.play().catch(error => {
            console.warn('⚠️ No se pudo reproducir el audio:', error);
        });
    };
    
    audio.onerror = function(error) {
        console.error('❌ Error al cargar audio:', error);
    };
}

// ===== UTILIDADES =====
function autoResizeTextarea() {
    const textarea = document.getElementById('message-input');
    if (textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
}

function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.textContent = getCurrentTimeString();
    }
}

function getCurrentTimeString() {
    const now = new Date();
    return now.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos para la notificación
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        borderRadius: '10px',
        color: 'white',
        fontWeight: '500',
        zIndex: '10000',
        maxWidth: '300px',
        wordWrap: 'break-word',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Colores según el tipo
    const colors = {
        info: '#667eea',
        success: '#48bb78',
        warning: '#ed8936',
        error: '#f56565'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// ===== MANEJO DE ERRORES GLOBALES =====
window.addEventListener('error', function(event) {
    console.error('❌ Error global:', event.error);
    showNotification('Ha ocurrido un error inesperado', 'error');
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('❌ Promise rechazada:', event.reason);
    showNotification('Error de conexión con el servidor', 'error');
});

// ===== FUNCIONES DE UTILIDAD ADICIONALES =====
function formatMessageForDisplay(message) {
    // Convertir saltos de línea a <br>
    return message.replace(/\n/g, '<br>');
}

function sanitizeInput(input) {
    // Limpiar input del usuario
    return input.trim().replace(/[<>]/g, '');
}

// ===== EXPORTAR FUNCIONES PARA DEBUGGING =====
window.MedicalApp = {
    CONFIG,
    appState,
    sendMessage,
    addMessageToChat,
    updateMedicalReport,
    showNotification
};

console.log('🏥 Consulta Médica Virtual - JavaScript cargado correctamente');
