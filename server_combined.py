import os
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, Response, send_file, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# === IA y Audio ===
import google.generativeai as genai
import whisper
from gtts import gTTS
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
CORS(app)

# ===== GEMINI =====
GEMINI_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("Falta GOOGLE_GEMINI_API_KEY en .env")

genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# Inicializar modelo Gemini al arranque
try:
    print("🧩 Inicializando modelo Gemini...")
    # Esto ejecuta una pequeña consulta para que el modelo cargue a memoria
    _ = gemini_model.generate_content("Inicialización del sistema IA-MedAssistant.")
    print("✅ Modelo Gemini listo para usar.")
except Exception as e:
    print("⚠️ Advertencia: no se pudo precargar el modelo Gemini:", e)


# ===== XML UTILITIES =====
def parse_xml_request():
    """Parse XML request body and return dict"""
    try:
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)
        data = {}
        for child in root:
            if child.tag == 'patient':
                data['patient'] = {}
                for patient_child in child:
                    data['patient'][patient_child.tag] = patient_child.text
            elif child.tag == 'studies':
                data['studies'] = [study.text for study in child.findall('study')]
            else:
                data[child.tag] = child.text
        return data
    except Exception:
        return {}

def create_xml_response(data):
    """Create XML response from dict"""
    root = ET.Element('response')
    for key, value in data.items():
        elem = ET.SubElement(root, key)
        elem.text = str(value)
    xml_str = ET.tostring(root, encoding='unicode')
    return Response(xml_str, mimetype='application/xml')

def is_mobile_client():
    """Detect if request is from mobile app"""
    user_agent = request.headers.get('User-Agent', '').lower()
    return 'mobile' in user_agent or 'android' in user_agent or 'ios' in user_agent

@app.route("/tmp/<path:filename>")
def serve_tmp_file(filename):
    """Sirve archivos temporales (como los .mp3 generados por la IA)."""
    tmp_dir = "/tmp"
    return send_from_directory(tmp_dir, filename, mimetype="audio/mpeg")

# ===== IA: Doctor (XML ONLY) =====
@app.post("/api/ai/doctor")
def ai_doctor():
    body = parse_xml_request()
    patient = body.get("patient", {})
    symptoms = body.get("symptoms", "")
    studies  = body.get("studies", [])

    prompt = f"""
Eres un asistente que APOYA a un MÉDICO TITULADO.
Devuelve:
1) Resumen clínico (TENLO EN CUENTA, PERO NO LO MENCIONAS A MENOS DE QUE SE TE PIDA)
2) 3-5 diagnósticos diferenciales con razonamiento corto.
3) Próximos pasos sugeridos.
4) Advertencia: el veredicto es del médico; esto NO sustituye consulta.

Paciente: {patient}
Síntomas: {symptoms}
Estudios/URLs: {studies}
Responde en español en formato claro y con viñetas.
"""
    try:
        resp = gemini_model.generate_content(prompt)
        text = (resp.text or "").strip()
    except Exception as e:
        text = f"(demo) Error con Gemini: {e}"

    return create_xml_response({"recommendation": text})


# ===== IA: Paciente (XML/JSON según cliente) =====
@app.post("/api/ai/patient")
def ai_patient():
    is_mobile = is_mobile_client()
    if is_mobile:
        body = request.json or {}
    else:
        body = parse_xml_request()

    patient = body.get("patient", {})
    symptoms = body.get("symptoms", "")
    studies  = body.get("studies", [])

    prompt = f"""
Eres un asistente que habla con un PACIENTE. Tono empático y claro.
Incluye:
- Explicación sencilla de lo que podría estar pasando (no diagnóstico).
- Señales de alarma si aplican.
- Pasos sugeridos (p.ej. agendar cita).
- A veces el paciente se siente más cómodo hablando contigo, no lo cortes.
- PREGUNTA HASTA QUE LLEGUES A UN DIAGNOSTICO, NO ESPECULES. PERO UNA PREGUNTA A LA VEZ, ANALIZA LO QUE TE CONTESTO Y PREGUNTALE OTRA LUEGO DE SU RESPUESTA. SI YA SABES ALGO SIMPLEMENTE RESPONDELE
- TRATA DE DAR REPSUESTAS BREVES, PERO SIN DEJAR LA SENSACIÓN DE QUE FUE MUY CORTA, ESTO POR QUE TU RESPUESTA SERÁ UTILIZADA PARA GENERAR UN AUDIO Y MANDARSELO AL PACIENTE. RECUERDA, MUY MUY CORTA
- COMO TU RESPUESTA SE PASARA A AUDIO, NO PONGAS CARACTERIS COMO GUIONES, ASTERICOS, ETC...
- NO MUESTRES LA INFORMACIÓN DEL PACIENTE A MENOS QUE SE TE PIDA.

Paciente: {patient}
Síntomas: {symptoms}
Estudios/URLs: {studies}
"""
    try:
        resp = gemini_model.generate_content(prompt)
        text = (resp.text or "").strip()
    except Exception as e:
        text = f"(demo) Error con Gemini: {e}"

    if is_mobile:
        return jsonify({"message": text})
    else:
        return create_xml_response({"message": text})


# ===== IA: File Analyzer JSON =====
@app.post("/api/ai/file/analyze_json")
def ai_file_analyze_json():
    import json

    upload = request.files.get("file")
    if not upload or upload.filename == "":
        return jsonify({"error": "Debes enviar un archivo en form-data con la clave 'file'."}), 400

    content_type = upload.mimetype or "application/octet-stream"
    instructions = request.form.get("instructions", "").strip()
    file_bytes = upload.read()

    prompt = f"""
Analiza el archivo adjunto (imagen, PDF o DOCX).
Extrae texto (OCR si aplica), estructura, tablas y datos clave.

Responde SOLO con un JSON válido (sin explicaciones).
{('Instrucciones del usuario: ' + instructions) if instructions else ''}
"""
    try:
        parts = [{"mime_type": content_type, "data": file_bytes}, prompt]
        resp = gemini_model.generate_content(parts)
        text = (resp.text or "").strip()

        try:
            payload = json.loads(text)
        except Exception:
            payload = {"raw_model_text": text}

        payload.setdefault("filename", upload.filename)
        payload.setdefault("mime_type", content_type)
        return jsonify(payload)
    except Exception as e:
        return jsonify({"error": f"Error procesando archivo con Gemini: {e}"}), 500


# ===== IA: File Analyzer XML =====
@app.post("/api/ai/file/analyze_xml")
def ai_file_analyze_xml():
    import json

    upload = request.files.get("file")
    if not upload or upload.filename == "":
        return create_xml_response({"error": "Debes enviar un archivo en form-data con la clave 'file'."})

    content_type = upload.mimetype or "application/octet-stream"
    instructions = request.form.get("instructions", "").strip()
    file_bytes = upload.read()

    prompt = f"""
Analiza el archivo adjunto (imagen, PDF o DOCX).
Extrae texto (OCR), estructura, tablas y datos clave.
En español
{('Instrucciones del usuario: ' + instructions) if instructions else ''}
"""
    try:
        parts = [{"mime_type": content_type, "data": file_bytes}, prompt]
        resp = gemini_model.generate_content(parts)
        text = (resp.text or "").strip()
        try:
            data = json.loads(text)
        except Exception:
            data = {"raw_model_text": text}
        data.setdefault("filename", upload.filename)
        data.setdefault("mime_type", content_type)

        root = ET.Element("response")
        def build_xml(parent, obj, item_tag="item"):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    child = ET.SubElement(parent, str(k))
                    build_xml(child, v, item_tag=item_tag)
            elif isinstance(obj, list):
                for it in obj:
                    child = ET.SubElement(parent, item_tag)
                    build_xml(child, it, item_tag=item_tag)
            else:
                parent.text = "" if obj is None else str(obj)
        build_xml(root, data)
        xml_str = ET.tostring(root, encoding="unicode")
        return Response(xml_str, mimetype="application/xml")
    except Exception as e:
        return create_xml_response({"error": f"Error procesando archivo con Gemini: {e}"})


# ===== IA: Texto a Voz =====
@app.post("/api/ai/text-to-speech")
def text_to_speech():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "Falta el campo 'text'"}), 400

    tts = gTTS(text=text, lang="es", tld="com.mx")
    out_path = "/tmp/output.mp3"
    tts.save(out_path)
    return send_file(out_path, mimetype="audio/mpeg", as_attachment=False)

@app.post("/api/ai/text-to-speech-xml")
def text_to_speech_xml():
    try:
        xml_data = request.data.decode("utf-8")
        root = ET.fromstring(xml_data)
        text_elem = root.find("text")
        if text_elem is None or not text_elem.text.strip():
            return create_xml_response({"error": "Falta el campo <text> en el XML"})

        text = text_elem.text.strip()
        tts = gTTS(text=text, lang="es", tld="com.mx")
        out_path = "/tmp/output_voice.mp3"
        tts.save(out_path)

        # En este caso devolvemos un XML que indica éxito, más el archivo MP3
        response = create_xml_response({"status": "ok", "message": "Audio generado exitosamente", "file": "output_voice.mp3"})
        return response
    except Exception as e:
        return create_xml_response({"error": str(e)})

# ===== IA: Voz a Texto =====
@app.post("/api/ai/speech-to-text")
def speech_to_text():
    upload = request.files.get("file")
    if not upload:
        return jsonify({"error": "Falta el archivo de audio ('file')"}), 400

    file_path = "/tmp/audio_input.wav"
    upload.save(file_path)

    model = whisper.load_model("base")
    result = model.transcribe(file_path, language="es")

    text = result["text"].strip()
    return jsonify({"text": text})

@app.post("/api/ai/speech-to-text-xml")
def speech_to_text_xml():
    try:
        upload = request.files.get("file")
        if not upload:
            return create_xml_response({"error": "Falta el archivo de audio ('file')"})
        
        file_path = "/tmp/audio_input_xml.wav"
        upload.save(file_path)

        model = whisper.load_model("base")
        result = model.transcribe(file_path, language="es")
        text = result["text"].strip()

        return create_xml_response({"text": text})
    except Exception as e:
        return create_xml_response({"error": str(e)})
    

# ====== MEMORIA Y RESÚMENES (PACIENTE) ======

conversations = {}  # memoria temporal en RAM {session_id: [{"role": "...", "content": "..."}]}

def summarize_text(text):
    """Genera un mini resumen clínico de una respuesta."""
    try:
        prompt = f"""
Eres un médico que está redactando notas clínicas. 
Resume lo siguiente en 3 líneas máximo, con tono médico y conciso:

Texto: {text}
"""
        resp = gemini_model.generate_content(prompt)
        summary = (resp.text or "").strip()
        return summary
    except Exception as e:
        return f"(Error al resumir: {e})"


# ---------- JSON ----------
@app.post("/api/ai/interaction")
def ai_interaction_json():
    """
    Maneja interacción con memoria (versión JSON)
    - Guarda historial
    - Devuelve respuesta + mini resumen
    """
    data = request.json or {}
    session_id = data.get("session_id", "default")
    message = data.get("message", "")
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "Falta 'message'"}), 400

    conversations.setdefault(session_id, [])
    conversations[session_id].append({"role": "user", "content": message})

    # Construye contexto con historial previo
    context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
    full_prompt = f"""
Eres un asistente médico que habla con un PACIENTE. 
Sé empático y claro, pero profesional. Usa el historial para dar continuidad.

Historial:
{context}

Paciente: {message}
"""

    try:
        resp = gemini_model.generate_content(full_prompt)
        answer = (resp.text or "").strip()
        conversations[session_id].append({"role": "assistant", "content": answer})

        summary = summarize_text(answer)

        return jsonify({
            "session_id": session_id,
            "response": answer,
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- XML ----------
@app.post("/api/ai/interaction-xml")
def ai_interaction_xml():
    """
    Versión XML del endpoint con memoria
    """
    try:
        xml_data = request.data.decode("utf-8")
        root = ET.fromstring(xml_data)

        session_elem = root.find("session_id")
        message_elem = root.find("message")

        session_id = session_elem.text if session_elem is not None else "default"
        message = message_elem.text.strip() if message_elem is not None else ""

        if not message:
            return create_xml_response({"error": "Falta <message> en XML"})

        conversations.setdefault(session_id, [])
        conversations[session_id].append({"role": "user", "content": message})

        history = conversations[session_id]
        context = "\n".join([f"{m['role']}: {m['content']}" for m in history[:-1]])

        full_prompt = f"""
Eres un asistente médico que habla con un PACIENTE. Sé empático y claro.
Historial previo:
{context}

Paciente: {message}
"""

        resp = gemini_model.generate_content(full_prompt)
        answer = (resp.text or "").strip()
        conversations[session_id].append({"role": "assistant", "content": answer})

        summary = summarize_text(answer)

        return create_xml_response({
            "session_id": session_id,
            "response": answer,
            "summary": summary
        })
    except Exception as e:
        return create_xml_response({"error": str(e)})


# ====== CONCLUSIÓN FINAL (PACIENTE) ======

# ---------- JSON ----------
@app.post("/api/ai/conclusion")
def ai_conclusion_json():
    """
    Crea un resumen final de toda la conversación del paciente (versión JSON)
    """
    data = request.json or {}
    session_id = data.get("session_id", "default")
    history = conversations.get(session_id, [])

    if not history:
        return jsonify({"error": "No hay historial para esta sesión"}), 400

    full_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    prompt = f"""
Eres un médico escribiendo la CONCLUSIÓN FINAL de una consulta con un paciente.
Haz un resumen clínico en 8–10 líneas que incluya:
- Motivo de consulta
- Síntomas principales
- Evolución durante la conversación
- Posibles diagnósticos diferenciales
- Recomendaciones finales
- Advertencia de que no sustituye una consulta real

Conversación:
{full_text}
"""
    try:
        resp = gemini_model.generate_content(prompt)
        conclusion = (resp.text or "").strip()
        return jsonify({
            "session_id": session_id,
            "conclusion": conclusion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- XML ----------
@app.post("/api/ai/conclusion-xml")
def ai_conclusion_xml():
    """
    Crea un resumen final en XML de la sesión del paciente.
    """
    try:
        xml_data = request.data.decode("utf-8")
        root = ET.fromstring(xml_data)
        session_elem = root.find("session_id")
        session_id = session_elem.text if session_elem is not None else "default"

        history = conversations.get(session_id, [])
        if not history:
            return create_xml_response({"error": "No hay historial para esta sesión"})

        full_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        prompt = f"""
Eres un médico haciendo el CIERRE DE CONSULTA con un paciente.
Redacta un resumen final de 8–10 líneas con tono médico profesional.

Incluye:
- Motivo de consulta
- Síntomas relevantes
- Evolución
- Diagnósticos diferenciales
- Recomendaciones y próximos pasos

Conversación completa:
{full_text}
"""
        resp = gemini_model.generate_content(prompt)
        conclusion = (resp.text or "").strip()
        return create_xml_response({
            "session_id": session_id,
            "conclusion": conclusion
        })
    except Exception as e:
        return create_xml_response({"error": str(e)})


@app.post("/api/ai/voice-session")
def ai_voice_session_json():
    """
    Flujo completo (JSON):
    1️⃣ Recibe audio de voz (usuario)
    2️⃣ Transcribe con Whisper
    3️⃣ Envía texto al modelo de paciente (Gemini)
    4️⃣ Genera resumen clínico
    5️⃣ Convierte respuesta a voz (gTTS)
    6️⃣ Devuelve texto y audio en JSON
    """
    try:
        upload = request.files.get("file")
        if not upload:
            return jsonify({"error": "Falta el archivo de audio ('file')"}), 400

        # 1. Guardar audio temporal
        input_path = "/tmp/input_voice.wav"
        upload.save(input_path)

        # 2. Transcripción (Whisper)
        model = whisper.load_model("base")
        result = model.transcribe(input_path, language="es")
        user_text = result["text"].strip()
        if not user_text:
            return jsonify({"error": "No se pudo transcribir audio"}), 400

        # 3. Enviar texto a IA (modelo paciente)
        prompt = f"""
        Eres un asistente médico empático que conversa con un paciente.
        Paciente: "{user_text}"
        Responde de forma clara, breve y profesional.
        - PREGUNTA HASTA QUE LLEGUES A UN DIAGNOSTICO, NO ESPECULES. PERO UNA PREGUNTA A LA VEZ, ANALIZA LO QUE TE CONTESTO Y PREGUNTALE OTRA LUEGO DE SU RESPUESTA. SI YA SABES ALGO SIMPLEMENTE RESPONDELE
        - TRATA DE DAR REPSUESTAS BREVES, PERO SIN DEJAR LA SENSACIÓN DE QUE FUE MUY CORTA, ESTO POR QUE TU RESPUESTA SERÁ UTILIZADA PARA GENERAR UN AUDIO Y MANDARSELO AL PACIENTE. RECUERDA, MUY MUY CORTA
        - COMO TU RESPUESTA SE PASARA A AUDIO, NO PONGAS CARACTERES COMO GUIONES, ASTERICOS, ETC...
        """
        resp = gemini_model.generate_content(prompt)
        ai_text = (resp.text or "").strip()

        # 4. Resumen clínico breve
        try:
            summary_prompt = f"Redacta una nota médica de 2 líneas máximo: {ai_text}"
            summary_resp = gemini_model.generate_content(summary_prompt)
            summary = (summary_resp.text or "").strip()
        except Exception:
            summary = "(sin resumen disponible)"

        # 5. Texto → voz
        tts = gTTS(text=ai_text, lang="es", tld="com.mx")
        output_path = "/tmp/output_ai.mp3"
        tts.save(output_path)

        # 6. Devolver resultado
        return jsonify({
            "status": "ok",
            "input_text": user_text,
            "ai_response": ai_text,
            "summary": summary,
            "audio_file": "output_ai.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/ai/voice-session-xml")
def ai_voice_session_xml():
    """
    Flujo completo (XML):
    1️⃣ Recibe audio o imagen
    2️⃣ Si es audio → transcribe con Whisper
    3️⃣ Si es imagen → analiza con Gemini (OCR + interpretación)
    4️⃣ Envía el texto resultante a Gemini para generar respuesta empática y breve
    5️⃣ Resume clínicamente
    6️⃣ Convierte la respuesta a voz
    7️⃣ Devuelve todo en XML limpio
    """
    try:
        upload = request.files.get("file")
        if not upload:
            return create_xml_response({"error": "Falta el archivo ('file')"})

        filename = upload.filename.lower()
        mime_type = upload.mimetype or ""
        is_audio = any(ext in filename for ext in [".wav", ".mp3", ".webm", ".m4a"])
        is_image = any(ext in filename for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".pdf"])

        user_text = ""

        # === AUDIO ===
        if is_audio or "audio" in mime_type:
            input_path = "/tmp/input_voice_xml.wav"
            upload.save(input_path)

            model = whisper.load_model("base")
            result = model.transcribe(input_path, language="es")
            user_text = result["text"].strip()
            if not user_text:
                return create_xml_response({"error": "No se pudo transcribir audio"})

        # === IMAGEN / DOCUMENTO ===
        elif is_image:
            file_bytes = upload.read()
            prompt_ocr = """
Eres un asistente médico experto en interpretación de imágenes clínicas.
El usuario te ha enviado una imagen que puede ser un estudio médico, radiografía, herida, análisis o documento visual relacionado con salud.

Tu tarea:
1. Interpreta con detalle lo que se observa: estructuras afectadas, tejidos, posibles patologías, signos de infección o daño.
2. Describe la posible causa o diagnóstico preliminar si es evidente.
3. Si es una imagen médica (como rayos X, tomografía, resonancia, laboratorio o herida), analiza con precisión anatómica y médica.
4. Al final, formula una sola pregunta útil o de seguimiento, del tipo:
  Al dinal explicala y da seguimiento, puedes dar alguna recomendacióm

Nunca digas frases como “No soy médico”, ni respondas de forma ambigua.
Si la imagen es clara, interpreta aunque el caso sea grave.
Habla como si fueras un profesional que ayuda a entender el resultado, no que evade responsabilidad.

SE BREVE, PERO EXPLICA TODO, AUNQUE SEAS BREVE TODO EXPLICADO E INTERPRETADO AL 100
"""
            try:
                parts = [{"mime_type": mime_type, "data": file_bytes}, prompt_ocr]
                resp_ocr = gemini_model.generate_content(parts)
                user_text = (resp_ocr.text or "").strip()
            except Exception as e:
                return create_xml_response({"error": f"Error al analizar la imagen: {e}"})
        else:
            return create_xml_response({"error": "Tipo de archivo no soportado. Envía audio o imagen."})

        # === RESPUESTA IA MÉDICA BREVE ===
        prompt = f"""
Eres una asistente médica virtual amable y empática. 
Tu objetivo es ayudar directamente al paciente de forma clara y breve.

Reglas:
- Responde cortamente, pues tu respuesta se va a grabar y no queremos dejar esperando al usuario, sin guiones, sin listas ni formato.
- Cada intervención tuya debe ser importante aunque sea corta.
- Evita sonar como doctora formal o dar diagnósticos clínicos largos.
- No pongas advertencias ni aclaraciones tipo “no soy médico”.
- Primero intenta ayudar y orientar
- Haz preguntas de su situación hasta encontrar un resultado y darle una conclusión, si desde el primer input que te da el usuario encuentras una conclusión, esta bién
- Si crees que puede ser algo serio, sugiere ir al médico en una sola frase, al final. SOLO SI ES GRAVE.
- Sé humana, cálida y directa, no robótica.

Paciente dice (texto o imagen interpretada): "{user_text}"
Tu respuesta:
"""

        resp = gemini_model.generate_content(prompt)
        ai_text = (resp.text or "").strip()

        # === RESUMEN MÉDICO ===
        try:
            summary_prompt = f"En pocas lineas dame algo como una nota médica, esto ayudará a ver el resumen de la llamada, no des solo un tipo summary, si no algo importante de la interacción, por ejemplo lo que pienses que pueda ser la situación, SE MUY MUY BREVE Y SOLO RESPONDE CONCISO, NADA DE INTRODUCCIÓNES TIPO SE MUY MUY BREVE Y SOLO RESPONDE CONCISO, NADA DE INTRODUCCIÓNES TIPO CLARO QUE SI, AQUI ESTA TU NOTA, SE BREVE PERO IMPORTANTE, ESTAS NOTAS LAS ESTARA VIENDO EK PACIENTE EN TIEMPO REAL, ES COMO UN APOYO PARA EL, NO TE REFIERAS A EL COMO PACIENTE, SOLO DA LA NOTA: {ai_text}"
            summary_resp = gemini_model.generate_content(summary_prompt)
            summary = (summary_resp.text or "").strip()
        except Exception:
            summary = "(sin resumen disponible)"

        # === TEXTO → VOZ (opcional, solo si se desea audio) ===
        output_path = "/tmp/output_ai_xml.mp3"
        try:
            tts = gTTS(text=ai_text, lang="es", tld="com.mx")
            tts.save(output_path)
        except Exception as e:
            print("⚠️ No se pudo generar el audio:", e)
            output_path = None

        # === RESPUESTA XML ===
        response_data = {
            "status": "ok",
            "input_text": user_text,
            "ai_response": ai_text,
            "summary": summary,
        }
        if output_path:
            response_data["audio_file"] = "output_ai_xml.mp3"

        return create_xml_response(response_data)

    except Exception as e:
        return create_xml_response({"error": str(e)})




# ===== RUTAS PRINCIPALES =====
@app.route("/")
def index():
    """Página principal con D-ID avatar"""
    return render_template("index.html")

@app.route("/health")
def health_check():
    """Health check para Vercel"""
    return jsonify({"status": "ok", "message": "Consulta Médica Virtual API funcionando"})

@app.route("/api/test-gemini")
def test_gemini():
    """Endpoint para probar la conexión con Gemini"""
    try:
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'GOOGLE_GEMINI_API_KEY no está configurada',
                'solucion': 'Configura GOOGLE_GEMINI_API_KEY en las variables de entorno de Vercel'
            }), 400
        
        # Probar conexión con Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
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
            'api_key_configurada': bool(os.getenv('GOOGLE_GEMINI_API_KEY'))
        }), 500

# ===== MAIN =====
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Cambiado de 8080 a 5000
    app.run(host="0.0.0.0", port=port, debug=True)
