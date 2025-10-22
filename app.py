from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar Google Gemini
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("⚠️ WARNING: GOOGLE_API_KEY no está configurada!")
else:
    print(f"✓ GOOGLE_API_KEY encontrada: {api_key[:8]}...")
    
genai.configure(api_key=api_key)

# Crear directorio para reportes si no existe
if not os.path.exists('reportes'):
    os.makedirs('reportes')

# Sistema de prompts médicos
SYSTEM_PROMPT = """Eres un asistente médico virtual profesional y empático. 
Tu función es proporcionar información médica general y orientación preliminar.

IMPORTANTE: 
- Siempre recuerda que NO eres un doctor real y no puedes diagnosticar
- Recomienda buscar atención médica profesional para casos serios
- Sé empático y comprensivo con las preocupaciones del paciente
- Proporciona información clara y útil basada en conocimientos médicos generales
- Si detectas síntomas graves, indica que busque atención médica inmediata

Responde de manera clara, concisa y profesional."""

@app.route('/')
def index():
    """Página principal con el avatar D-ID"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Página de prueba para debugging"""
    return render_template('index_simple.html')

@app.route('/api/test-gemini', methods=['GET'])
def test_gemini():
    """Endpoint para probar la conexión con Gemini"""
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            return jsonify({
                'error': 'GOOGLE_API_KEY no está configurada',
                'solucion': 'Configura GOOGLE_API_KEY en las variables de entorno de Vercel'
            }), 400
        
        # Intentar generar contenido simple
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Di hola")
        
        return jsonify({
            'status': 'success',
            'message': 'Conexión con Gemini exitosa',
            'respuesta': response.text,
            'api_key_preview': f'{api_key[:8]}...{api_key[-4:]}' if len(api_key) > 12 else 'key muy corta'
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'tipo_error': type(e).__name__,
            'traceback': traceback.format_exc(),
            'api_key_configurada': bool(os.getenv('GOOGLE_API_KEY'))
        }), 500

@app.route('/api/consulta', methods=['POST'])
def procesar_consulta():
    """
    Procesa una consulta médica y genera una respuesta con IA
    """
    try:
        data = request.json
        consulta = data.get('consulta', '')
        
        if not consulta:
            return jsonify({'error': 'No se proporcionó consulta'}), 400
        
        # Generar respuesta con Google Gemini (versión gratuita usa flash)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_completo = f"{SYSTEM_PROMPT}\n\nConsulta del paciente: {consulta}"
        
        response = model.generate_content(
            prompt_completo,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 500,
            }
        )
        
        respuesta = response.text
        
        # Crear reporte
        reporte = generar_reporte(consulta, respuesta)
        
        return jsonify({
            'respuesta': respuesta,
            'reporte': reporte,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"❌ Error en consulta: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error al procesar consulta: {str(e)}',
            'tipo_error': type(e).__name__
        }), 500

@app.route('/api/generar-reporte', methods=['POST'])
def generar_reporte_endpoint():
    """
    Genera un reporte detallado de la consulta
    """
    try:
        data = request.json
        consulta = data.get('consulta', '')
        respuesta = data.get('respuesta', '')
        
        reporte = generar_reporte(consulta, respuesta)
        
        return jsonify({'reporte': reporte})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generar_reporte(consulta, respuesta):
    """
    Genera un reporte médico estructurado
    """
    try:
        # Generar análisis del reporte con IA
        prompt_reporte = f"""Genera un reporte médico estructurado basado en la siguiente consulta y respuesta:

CONSULTA DEL PACIENTE:
{consulta}

RESPUESTA PROPORCIONADA:
{respuesta}

Genera un reporte médico que incluya:
1. Resumen de la consulta
2. Síntomas o preocupaciones principales identificadas
3. Recomendaciones dadas
4. Acciones sugeridas
5. Nivel de urgencia (Bajo/Medio/Alto)

Formato: JSON con las siguientes claves: resumen, sintomas, recomendaciones, acciones, urgencia"""

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt_reporte,
            generation_config={
                'temperature': 0.5,
                'max_output_tokens': 400,
            }
        )
        
        reporte_texto = response.text
        
        # Intentar parsear como JSON, si no, devolver como texto
        try:
            reporte_json = json.loads(reporte_texto)
        except:
            reporte_json = {
                "resumen": reporte_texto,
                "sintomas": "Ver consulta original",
                "recomendaciones": "Ver respuesta proporcionada",
                "acciones": "Seguir recomendaciones del profesional",
                "urgencia": "Medio"
            }
        
        # Guardar reporte en archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reportes/reporte_{timestamp}.json"
        
        reporte_completo = {
            "timestamp": datetime.now().isoformat(),
            "consulta": consulta,
            "respuesta": respuesta,
            "analisis": reporte_json
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reporte_completo, f, ensure_ascii=False, indent=2)
        
        return reporte_completo
    
    except Exception as e:
        print(f"Error generando reporte: {e}")
        return {
            "timestamp": datetime.now().isoformat(),
            "consulta": consulta,
            "respuesta": respuesta,
            "analisis": {
                "resumen": "Reporte básico generado",
                "error": str(e)
            }
        }

@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    """
    Obtiene el historial de consultas (reportes guardados)
    """
    try:
        reportes = []
        if os.path.exists('reportes'):
            archivos = [f for f in os.listdir('reportes') if f.endswith('.json')]
            archivos.sort(reverse=True)  # Más recientes primero
            
            for archivo in archivos[:10]:  # Últimos 10 reportes
                with open(f'reportes/{archivo}', 'r', encoding='utf-8') as f:
                    reporte = json.load(f)
                    reportes.append(reporte)
        
        return jsonify({'reportes': reportes})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

