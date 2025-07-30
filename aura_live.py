"""
AURA400 Live Web Interface
-------------------------
This module implements a web interface for the AURA400 quantum emotional system.
It provides real-time visualization and interaction with the quantum emotional core.

Author: Juan Pablo
Date: July 28, 2025
Version: 2.1 - Fixed
"""

from flask import Flask, render_template_string, jsonify, request, abort, make_response, send_from_directory
from flask_wtf import CSRFProtect
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import os
import uuid
import time
import logging
from werkzeug.exceptions import NotFound

# --- Seguridad y CORS ---
CORS_HEADERS = {
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline';",
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'no-referrer',
    'X-XSS-Protection': '1; mode=block',
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aura400.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', str(uuid.uuid4()))
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Seguridad: Headers en todas las respuestas ---
@app.after_request
def set_secure_headers(response):
    for k, v in CORS_HEADERS.items():
        response.headers[k] = v
    return response

# --- Favicon route ---
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# --- Manejo global de errores mejorado ---
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, NotFound):
        return jsonify({"error": "Not found", "type": "NotFound"}), 404
    logger.error(f"Unhandled error: {str(e)}", exc_info=True)
    return jsonify({"error": str(e), "type": type(e).__name__}), 500

# Numpy random generator
rng = np.random.default_rng(seed=int.from_bytes(os.urandom(8), 'little'))

class QuantumEmotionalCore:
    """
    A quantum-inspired emotional processing system using Qiskit for quantum simulation.
    This core processes emotional states through quantum circuits and provides
    real-time emotional feedback.
    """
    
    def __init__(self):
        """Initialize the Quantum Emotional Core with configuration from environment."""
        self.N_BLOCKS = int(os.getenv('N_BLOCKS', 100))
        self.QUBITS_PER_BLOCK = int(os.getenv('QUBITS_PER_BLOCK', 4))
        self.TOTAL_QUBITS = self.N_BLOCKS * self.QUBITS_PER_BLOCK
        
        # Emotional state vectors - INICIALIZAR CORRECTAMENTE
        self.emotion_state = np.zeros(8)
        self.quantum_intensity = 0.0
        self.phase_coherence = 0.0
        self.entanglement_measure = 0.0
        self.emotional_vector = rng.random(8)
        
        # Sensor feedback initialization
        self.sensor_feedback = {
            "arousal": 0.5,
            "valence": 0.5,
            "dominance": 0.5
        }
        
        # Session and metrics
        self.session_id = str(uuid.uuid4())[:8]
        self.metrics = {
            "executions": 0,
            "errors": 0,
            "avg_intensity": 0.0,
            "last_execution_time": None,
            "success_rate": 100.0,
            "start_time": time.time()
        }
        
        # Initialize quantum backend
        self.backend_type = os.getenv('QUANTUM_BACKEND', "QUANTUM_SIMULATOR")
        self.initialize_quantum_backend()
        logger.info(f"Initialized QuantumEmotionalCore with session {self.session_id}")
        
    def initialize_quantum_backend(self):
        """Initialize the quantum backend with error handling and fallback."""
        try:
            from qiskit_aer import Aer
            self.backend = Aer.get_backend('statevector_simulator')
            self.backend_type = "QISKIT_AER_SIMULATOR"
            self.qiskit_available = True
            self.build_quantum_circuit()
            logger.info("Successfully initialized Qiskit backend")
        except ImportError as e:
            logger.warning(f"Qiskit not available, falling back to classical simulation: {str(e)}")
            self.backend_type = "CLASSICAL_QUANTUM_SIMULATION"
            self.qiskit_available = False
        except Exception as err:
            logger.error(f"Unexpected error initializing quantum backend: {str(err)}")
            self.backend_type = "CLASSICAL_QUANTUM_SIMULATION"
            self.qiskit_available = False
    
    def build_quantum_circuit(self):
        """
        Build the quantum circuit for emotional processing.
        Uses a reduced number of qubits for efficiency while maintaining functionality.
        """
        if not self.qiskit_available:
            return
            
        try:
            from qiskit import QuantumCircuit, QuantumRegister
            
            # Use a practical number of qubits (máximo 8 para evitar problemas de memoria)
            active_qubits = min(8, self.TOTAL_QUBITS)
            qreg = QuantumRegister(active_qubits, 'emotion')
            self.circuit = QuantumCircuit(qreg)
            
            # Initialize quantum state
            self._initialize_quantum_state(qreg)
            
            # Add emotional parameters
            self._add_emotional_parameters(qreg)
            
            # Add entanglement layer
            self._add_entanglement_layer(qreg)
            
            logger.info(f"Built quantum circuit with {active_qubits} qubits")
            
        except Exception as err:
            logger.error(f"Error building quantum circuit: {str(err)}")
            self.qiskit_available = False
            
    def _initialize_quantum_state(self, qreg):
        """Initialize the quantum state with Hadamard gates and CNOT operations."""
        for i in range(min(20, self.N_BLOCKS)):
            base_idx = i % qreg.size
            self.circuit.h(base_idx)
            if base_idx + 1 < qreg.size:
                self.circuit.cx(base_idx, base_idx + 1)
                
    def _add_emotional_parameters(self, qreg):
        """Add parameterized rotation gates for emotional processing."""
        from qiskit.circuit import Parameter
        self.theta_params = []
        for i in range(min(8, qreg.size)):
            param = Parameter(f'theta_{i}')
            self.circuit.ry(param, i)
            self.theta_params.append(param)
            
    def _add_entanglement_layer(self, qreg):
        """Add entanglement operations between qubits."""
        for i in range(0, min(16, qreg.size), 2):
            if i + 1 < qreg.size:
                self.circuit.cz(i, i + 1)
    
    def execute_quantum_emotion_cycle(self):
        """
        Execute one cycle of quantum emotional processing.
        Returns True if successful, False otherwise.
        """
        start_time = time.time()
        try:
            if self.qiskit_available:
                success = self.real_quantum_simulation()
            else:
                success = self.classical_quantum_simulation()
                
            execution_time = time.time() - start_time
            self.metrics["last_execution_time"] = execution_time
            
            self.metrics["executions"] += 1
            if success:
                self.metrics["success_rate"] = (
                    (self.metrics["executions"] - self.metrics["errors"]) / 
                    self.metrics["executions"] * 100
                )
            return success
            
        except Exception as err:
            logger.error(f"Error in quantum emotion cycle: {str(err)}")
            self.metrics["errors"] += 1
            self.metrics["executions"] += 1
            self.metrics["success_rate"] = (
                (self.metrics["executions"] - self.metrics["errors"]) / 
                max(1, self.metrics["executions"]) * 100
            )
            return self.classical_quantum_simulation()
    
    def real_quantum_simulation(self):
        """Execute the quantum circuit using Qiskit."""
        try:
            from qiskit import transpile
            param_values = self.emotional_vector[:len(self.theta_params)]
            param_dict = dict(zip(self.theta_params, param_values))
            # Usar assign_parameters para compatibilidad con Qiskit moderno
            bound_circuit = self.circuit.assign_parameters(param_dict)
            transpiled = transpile(bound_circuit, self.backend)
            job = self.backend.run(transpiled, shots=1024)
            result = job.result()
            statevector = result.get_statevector()
            self._process_quantum_results(statevector)
            return True
        except Exception as err:
            logger.error(f"Error in quantum simulation: {str(err)}")
            return False
            
    def _process_quantum_results(self, statevector):
        """Process the results from quantum execution (Qiskit real)."""
        import qiskit.quantum_info as qi
        probabilities = np.abs(statevector.data) ** 2
        # Intensidad: suma de probabilidades de los 8 primeros estados (uno por emoción)
        self.quantum_intensity = float(np.sum(probabilities[:8]))
        # Coherencia: pureza del estado (Tr(rho^2))
        rho = np.outer(statevector.data, np.conj(statevector.data))
        self.phase_coherence = float(np.real(np.trace(rho @ rho)))
        # Entrelazamiento: entropía de von Neumann de los primeros 2 qubits
        try:
            # Reduce density matrix to first 2 qubits
            reduced = qi.partial_trace(statevector, list(range(2, statevector.num_qubits)))
            eigvals = np.real(np.linalg.eigvalsh(reduced.data))
            eigvals = eigvals[eigvals > 1e-12]  # avoid log(0)
            entropy = -np.sum(eigvals * np.log2(eigvals))
            self.entanglement_measure = float(entropy)
        except Exception:
            self.entanglement_measure = 0.0
        self.update_emotional_state()
        
        # Update metrics
        if self.metrics["executions"] > 0:
            self.metrics["avg_intensity"] = (
                (self.metrics["avg_intensity"] * (self.metrics["executions"] - 1) + 
                 self.quantum_intensity) / self.metrics["executions"]
            )
        else:
            self.metrics["avg_intensity"] = self.quantum_intensity
    
    def classical_quantum_simulation(self):
        """
        Execute a classical simulation when quantum hardware/simulator is unavailable.
        Returns True as it's a deterministic fallback.
        """
        t = time.time()
        base_freq = 0.1
        
        # Generate quasi-quantum behavior
        self.quantum_intensity = (
            np.sin(t * base_freq) * np.cos(t * base_freq * 1.3) + 1
        ) / 2
        self.quantum_intensity *= (1 + 0.3 * np.sin(t * 0.05))
        
        # Update phase coherence and entanglement in classical simulation
        self.phase_coherence = np.angle(
            complex(np.cos(t * base_freq), np.sin(t * base_freq))
        )
        self.entanglement_measure = 0.3 + 0.1 * np.sin(t * 0.02)
        
        self.update_emotional_state()
        
        # Update metrics correctamente
        if self.metrics["executions"] > 0:
            self.metrics["avg_intensity"] = (
                (self.metrics["avg_intensity"] * (self.metrics["executions"] - 1) + self.quantum_intensity) /
                self.metrics["executions"]
            )
        else:
            self.metrics["avg_intensity"] = self.quantum_intensity
        return True

    def update_emotional_state(self):
        """Update emotional state based on current emotional vector and add some dynamics."""
        # Mezcla el vector emocional actual con algo de ruido para dinamismo
        noise = rng.random(8) * 0.1
        base_state = self.emotional_vector + noise
        
        # Normaliza para que sea una distribución de probabilidad
        if np.sum(base_state) > 0:
            self.emotion_state = base_state / np.sum(base_state)
        else:
            self.emotion_state = rng.dirichlet(np.ones(8))

    def get_metrics(self):
        """Return metrics for monitoring, including emotional state vector."""
        return {
            **self.metrics,
            "quantum_intensity": float(self.quantum_intensity),
            "phase_coherence": float(self.phase_coherence),
            "entanglement_measure": float(self.entanglement_measure),
            "session_id": self.session_id,
            "backend": self.backend_type,
            "state": self.emotion_state.tolist()
        }

    def reset(self):
        """Reset emotional state and metrics."""
        self.__init__()
        logger.info("QuantumEmotionalCore reset.")

# Initialize quantum core
quantum_core = QuantumEmotionalCore()

EMOTIONS = [
    {"name": "joy", "color": "#FFD700"},
    {"name": "fear", "color": "#4682B4"},
    {"name": "anger", "color": "#DC143C"},
    {"name": "sadness", "color": "#4169E1"},
    {"name": "surprise", "color": "#FF8C00"},
    {"name": "disgust", "color": "#228B22"},
    {"name": "trust", "color": "#20B2AA"},
    {"name": "anticipation", "color": "#FF69B4"}
]

# --- API: Health ---
@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok", "backend": quantum_core.backend_type, "session": quantum_core.session_id})

# --- API: Métricas Prometheus ---
@app.route('/metrics')
def metrics():
    m = quantum_core.get_metrics()
    prometheus = [
        f"aura400_executions_total {m['executions']}",
        f"aura400_errors_total {m['errors']}",
        f"aura400_avg_intensity {m['avg_intensity']}",
        f"aura400_quantum_intensity {m['quantum_intensity']}",
        f"aura400_phase_coherence {m['phase_coherence']}",
        f"aura400_entanglement_measure {m['entanglement_measure']}",
        f"aura400_success_rate {m['success_rate']}",
    ]
    return make_response("\n".join(prometheus), 200, {"Content-Type": "text/plain; version=0.0.4"})

# --- API: Métricas JSON ---
@app.route('/api/metrics')
def api_metrics():
    # Ejecuta un ciclo cuántico para animación en tiempo real
    quantum_core.execute_quantum_emotion_cycle()
    return jsonify(quantum_core.get_metrics())

# --- API: Reset ---
@app.route('/api/reset', methods=['POST'])
@csrf.exempt
def api_reset():
    quantum_core.reset()
    return jsonify({"status": "reset", "session": quantum_core.session_id})

# --- API: Feel (procesar emoción) ---
@app.route('/api/feel', methods=['POST'])
@csrf.exempt
def api_feel():
    try:
        data = request.get_json(force=True)
        emotion = data.get('emotion', 'joy')
        
        # Validar emoción
        if not any(e['name'] == emotion for e in EMOTIONS):
            return jsonify({"error": "Invalid emotion"}), 400
            
        # Configurar vector emocional
        quantum_core.emotional_vector = np.zeros(8)
        idx = next(i for i, e in enumerate(EMOTIONS) if e['name'] == emotion)
        quantum_core.emotional_vector[idx] = 1.0
        
        # Ejecutar ciclo cuántico
        success = quantum_core.execute_quantum_emotion_cycle()
        
        return jsonify({
            "success": success,
            "emotion": emotion,
            "state": quantum_core.emotion_state.tolist(),
            "metrics": quantum_core.get_metrics()
        })
    except Exception as e:
        logger.error(f"Error in api_feel: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- Dashboard HTML corregido ---
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA400 Live Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #181a1b;
            --bg-light: #f5f5f5;
            --text-dark: #f5f5f5;
            --text-light: #181a1b;
            --primary: #20B2AA;
            --accent: #FFD700;
            --error: #DC143C;
        }
        [data-theme="dark"] {
            background: var(--bg-dark);
            color: var(--text-dark);
        }
        [data-theme="light"] {
            background: var(--bg-light);
            color: var(--text-light);
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0; padding: 0;
            min-height: 100vh;
            transition: background 0.3s, color 0.3s;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            background: rgba(32,178,170,0.08);
            border-radius: 1rem;
            box-shadow: 0 4px 24px #0002;
            padding: 2rem;
        }
        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .emotion-bar {
            display: flex;
            gap: 1rem;
            margin: 1.5rem 0;
            justify-content: center;
            flex-wrap: wrap;
        }
        .emotion {
            flex: 1;
            min-width: 100px;
            background: #2226;
            border-radius: 0.5rem;
            padding: 0.8rem 0.4rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            border: 2px solid transparent;
        }
        .emotion:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .emotion.active {
            border-color: var(--accent);
            background: var(--accent);
            color: #222;
            transform: scale(1.05);
        }
        .emotion.pulse {
            animation: pulse 0.7s;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 var(--accent); }
            70% { box-shadow: 0 0 0 10px rgba(255,215,0,0.2); }
            100% { box-shadow: 0 0 0 0 var(--accent); }
        }
        .emotion.selected {
            border-color: var(--primary);
            background: linear-gradient(90deg, var(--accent) 60%, var(--primary) 100%);
            color: #222;
            box-shadow: 0 0 12px 2px var(--accent);
        }
        .emotion .value-label {
            font-size: 1.08rem;
            font-weight: bold;
            color: var(--primary);
            margin-top: 0.18rem;
            letter-spacing: 0.2px;
        }
        .emotion .tooltip {
            font-size: 0.92rem;
        }
        /* --- INNOVACIÓN VISUAL Y ESTÉTICA --- */
        .dashboard-glow {
            box-shadow: 0 0 40px 0 #20B2AA55, 0 0 0 8px #FFD70022;
            border: 2px solid #FFD70055;
            background: linear-gradient(120deg, #181a1b 80%, #FFD70011 100%);
            animation: dashboardGlow 3s infinite alternate;
        }
        @keyframes dashboardGlow {
            0% { box-shadow: 0 0 40px 0 #20B2AA55, 0 0 0 8px #FFD70022; }
            100% { box-shadow: 0 0 60px 8px #FFD70099, 0 0 0 16px #20B2AA33; }
        }
        .chart-title {
            font-size: 1.18rem;
            color: #FFD700;
            letter-spacing: 0.5px;
            margin-bottom: 0.7rem;
            text-shadow: 0 2px 8px #FFD70033;
            font-weight: 600;
        }
        .metric-value {
            text-shadow: 0 2px 8px #FFD70033;
        }
        .emotion.selected {
            border-width: 3px;
            filter: brightness(1.15) drop-shadow(0 0 8px #FFD700);
        }
        .emotion .value-label {
            text-shadow: 0 1px 4px #FFD70044;
        }
        .emotion {
            transition: box-shadow 0.3s, background 0.3s, color 0.3s, border 0.3s, transform 0.2s, filter 0.3s;
        }
        .emotion:hover {
            filter: brightness(1.1) drop-shadow(0 0 6px #FFD700);
        }
        .chart-box {
            border: 1.5px solid #FFD70033;
            background: linear-gradient(120deg, #2228 80%, #FFD70011 100%);
            box-shadow: 0 4px 24px #FFD70022, 0 0 0 2px #20B2AA22;
        }
        .chart-responsive, .chart-responsive-thin {
            background: linear-gradient(120deg, #181a1b 80%, #FFD70011 100%);
            border: 1.5px solid #FFD70033;
        }
        .legend-pro {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            justify-content: center;
            margin: 0.7rem 0 0.2rem 0;
        }
        .legend-pro-item {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.98rem;
            color: #FFD700;
            background: #222a;
            border-radius: 0.5rem;
            padding: 0.2rem 0.7rem;
            box-shadow: 0 1px 4px #FFD70022;
        }
        .legend-pro-dot {
            width: 16px; height: 16px; border-radius: 50%; display: inline-block;
        }
        /* Animación de entrada para los gráficos */
        .chart-box, .emotion-bar, .metrics, .feedback-message {
            opacity: 0;
            transform: translateY(30px);
            animation: fadeInUp 1.1s forwards;
        }
        .chart-box { animation-delay: 0.2s; }
        .emotion-bar { animation-delay: 0.1s; }
        .metrics { animation-delay: 0.3s; }
        .feedback-message { animation-delay: 0.4s; }
        @keyframes fadeInUp {
            to { opacity: 1; transform: none; }
        }
        /* Botón de reset animado */
        .reset-btn {
            background: linear-gradient(90deg, #FFD700 60%, #20B2AA 100%);
            color: #181a1b;
            font-weight: bold;
            box-shadow: 0 2px 8px #FFD70033;
            border: 2px solid #FFD70099;
            transition: background 0.3s, color 0.3s, box-shadow 0.3s;
        }
        .reset-btn:hover {
            background: linear-gradient(90deg, #20B2AA 60%, #FFD700 100%);
            color: #FFD700;
            box-shadow: 0 4px 16px #20B2AA55;
        }
    </style>
</head>
<body>
    <div class="backend-indicator" id="backendIndicator">
        <span class="backend-dot quantum"></span> Quantum
    </div>
    <button class="theme-toggle" onclick="toggleTheme()">🌗</button>
    <div class="container dashboard-glow">
        <h1>🧠 AURA400 Live Dashboard</h1>
        <div class="legend-pro">
            {% for emo in emotions %}
            <div class="legend-pro-item"><span class="legend-pro-dot" style="background: {{ emo.color }};"></span>{{ emo.name|title }}</div>
            {% endfor %}
        </div>
        <div class="feedback-message" id="feedbackMsg"></div>
        <div class="emotion-bar" id="emotionBar">
            {% for emo in emotions %}
            <div class="emotion" data-emotion="{{ emo.name }}" style="background: {{ emo.color }}44;">
                <div style="font-weight:bold;">{{ emo.name|title }}</div>
                <div class="value-label" id="label-{{ emo.name }}"></div>
                <div class="tooltip">Activar emoción {{ emo.name|title }}</div>
            </div>
            {% endfor %}
        </div>
        <div class="loading" id="loading">⚡ Procesando...</div>
        <div class="charts-container">
            <div class="chart-box">
                <div class="chart-title">🔄 Estado Núcleo (Tiempo Real)</div>
                <div class="chart-responsive"><canvas id="coreChart"></canvas></div>
                <div class="chart-responsive-thin"><canvas id="coreSpark"></canvas></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">👤 Emociones del Usuario</div>
                <div class="chart-responsive"><canvas id="userRadar"></canvas></div>
                <div class="controls">
                    <select id="emotionSelect" multiple size="4">
                        {% for emo in emotions %}
                        <option value="{{ emo.name }}">{{ emo.name|title }}</option>
                        {% endfor %}
                    </select><br>
                    <button class="action-btn" onclick="runUserEmotions()">🚀 Ejecutar Selección</button>
                </div>
            </div>
            <div class="chart-box">
                <div class="chart-title">🌈 Emociones en Acción (Histórico)</div>
                <div class="chart-responsive-thin"><canvas id="emotionsLine"></canvas></div>
            </div>
        </div>
        <div class="metrics" id="metrics">
            <!-- Métricas dinámicas -->
        </div>
        <div style="text-align: center; margin: 2rem 0;">
            <button class="reset-btn" onclick="resetCore()">🔄 Resetear Sistema</button>
        </div>
    </div>
    <script>
        let coreChart, userRadar, coreSpark, emotionsLine;
        const EMOTION_LABELS = {{ emotions | map(attribute='name') | map('title') | list | tojson }};
        const EMOTION_COLORS = {{ emotions | map(attribute='color') | list | tojson }};
        let isUpdating = false;
        let sparkData = [];
        let emotionsHistory = Array(8).fill().map(() => []); // 8 emociones, historial
        let lastBackend = null;

        function showLoading(show = true) {
            document.getElementById('loading').style.display = show ? 'block' : 'none';
        }
        function showFeedback(msg, color = null) {
            const el = document.getElementById('feedbackMsg');
            el.textContent = msg;
            if (color) el.style.color = color;
            else el.style.color = '';
        }
        function updateBackendIndicator(backend) {
            const el = document.getElementById('backendIndicator');
            if (backend.includes('QUANTUM')) {
                el.innerHTML = '<span class="backend-dot quantum"></span> Quantum';
            } else {
                el.innerHTML = '<span class="backend-dot classic"></span> Classic';
            }
        }
        function updateMetrics() {
            if (isUpdating) return;
            isUpdating = true;
            fetch('/api/metrics')
                .then(r => r.json())
                .then(m => {
                    updateBackendIndicator(m.backend);
                    const status = m.success_rate > 95 ? 'ok' : m.success_rate > 80 ? 'warning' : 'error';
                    const html = `
                        <div class='metric'>
                            <div>Estado</div>
                            <div class='metric-value'>
                                <span class='status-indicator status-${status}'></span>
                                ${m.success_rate.toFixed(1)}%
                            </div>
                        </div>
                        <div class='metric'>
                            <div>Ejecutadas</div>
                            <div class='metric-value'>${m.executions}</div>
                        </div>
                        <div class='metric'>
                            <div>Errores</div>
                            <div class='metric-value'>${m.errors}</div>
                        </div>
                        <div class='metric'>
                            <div>Intensidad Q</div>
                            <div class='metric-value'>${m.quantum_intensity.toFixed(3)}</div>
                        </div>
                        <div class='metric'>
                            <div>Coherencia</div>
                            <div class='metric-value'>${m.phase_coherence.toFixed(3)}</div>
                        </div>
                        <div class='metric'>
                            <div>Entrelazamiento</div>
                            <div class='metric-value'>${m.entanglement_measure.toFixed(3)}</div>
                        </div>
                        <div class='metric'>
                            <div>Backend</div>
                            <div class='metric-value' style='font-size:0.9rem;'>${m.backend.replace('_', ' ')}</div>
                        </div>
                        <div class='metric'>
                            <div>Sesión</div>
                            <div class='metric-value' style='font-size:0.9rem;'>${m.session_id}</div>
                        </div>
                    `;
                    document.getElementById('metrics').innerHTML = html;
                    // Update core chart
                    if (coreChart && Array.isArray(m.state) && m.state.length === 8) {
                        coreChart.data.datasets[0].data = m.state;
                        coreChart.update('none');
                        // Update value labels
                        m.state.forEach((v, i) => {
                            document.getElementById('label-' + EMOTION_LABELS[i].toLowerCase()).textContent = (v*100).toFixed(1) + '%';
                        });
                        // Sparkline
                        sparkData.push(m.quantum_intensity);
                        if (sparkData.length > 40) sparkData.shift();
                        if (coreSpark) {
                            coreSpark.data.labels = Array(sparkData.length).fill('');
                            coreSpark.data.datasets[0].data = sparkData;
                            coreSpark.update('none');
                        }
                        // Emotions history
                        m.state.forEach((v, i) => {
                            emotionsHistory[i].push(v);
                            if (emotionsHistory[i].length > 40) emotionsHistory[i].shift();
                        });
                        if (emotionsLine) {
                            emotionsLine.data.labels = Array(emotionsHistory[0].length).fill('');
                            emotionsLine.data.datasets.forEach((ds, i) => {
                                ds.data = emotionsHistory[i];
                            });
                            emotionsLine.update('none');
                        }
                    }
                    // Extra metrics
                    const extra = `
                        <div class='metric'><div>Latencia</div><div class='metric-value'>${(m.last_execution_time*1000).toFixed(1)} ms</div></div>
                        <div class='metric'><div>Intensidad Máx</div><div class='metric-value'>${Math.max(...m.state).toFixed(2)}</div></div>
                        <div class='metric'><div>Intensidad Mín</div><div class='metric-value'>${Math.min(...m.state).toFixed(2)}</div></div>
                        <div class='metric'><div>Prom. Núcleo</div><div class='metric-value'>${(m.state.reduce((a,b)=>a+b,0)/8*100).toFixed(1)}%</div></div>
                        <div class='metric'><div>Tiempo Total</div><div class='metric-value'>${((Date.now()/1000-m.start_time)/60).toFixed(1)} min</div></div>
                    `;
                    document.getElementById('metrics').innerHTML += extra;
                })
                .catch(err => console.error('Error updating metrics:', err))
                .finally(() => {
                    isUpdating = false;
                });
        }
        function setupCharts() {
            // Core bar chart
            const ctx1 = document.getElementById('coreChart').getContext('2d');
            coreChart = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: EMOTION_LABELS,
                    datasets: [{
                        label: 'Intensidad',
                        data: Array(8).fill(0),
                        backgroundColor: EMOTION_COLORS.map((c,i) => `rgba(${parseInt(c.slice(1,3),16)},${parseInt(c.slice(3,5),16)},${parseInt(c.slice(5,7),16)},0.7)`),
                        borderColor: EMOTION_COLORS,
                        borderWidth: 2,
                        borderRadius: 8,
                        hoverBackgroundColor: EMOTION_COLORS.map((c,i) => `rgba(${parseInt(c.slice(1,3),16)},${parseInt(c.slice(3,5),16)},${parseInt(c.slice(5,7),16)},1)`),
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 4/3,
                    plugins: { 
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#222',
                            titleColor: '#FFD700',
                            bodyColor: '#FFD700',
                            borderColor: '#FFD700',
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return `${context.label}: ${(context.parsed.y * 100).toFixed(1)}%`;
                                }
                            }
                        }
                    },
                    scales: { 
                        y: { 
                            min: 0, 
                            max: 1,
                            grid: { color: '#FFD70022' },
                            ticks: {
                                color: '#FFD700',
                                font: { size: 13 },
                                callback: function(value) {
                                    return (value * 100).toFixed(0) + '%';
                                }
                            }
                        },
                        x: {
                            ticks: {
                                color: '#FFD700',
                                font: { size: 13 },
                                maxRotation: 45
                            },
                            grid: { color: '#FFD70022' }
                        }
                    },
                    animation: {
                        duration: 700
                    }
                }
            });
            // Core sparkline
            const ctxSpark = document.getElementById('coreSpark').getContext('2d');
            coreSpark = new Chart(ctxSpark, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Intensidad Q',
                        data: [],
                        borderColor: '#FFD700',
                        backgroundColor: 'rgba(255,215,0,0.13)',
                        tension: 0.5,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 7,
                    plugins: { legend: { display: false } },
                    scales: { y: { min: 0, max: 1, display: false }, x: { display: false } },
                    animation: { duration: 500 }
                }
            });
            // User radar chart
            const ctxRadar = document.getElementById('userRadar').getContext('2d');
            userRadar = new Chart(ctxRadar, {
                type: 'radar',
                data: {
                    labels: EMOTION_LABELS,
                    datasets: [{
                        label: 'Usuario',
                        data: Array(8).fill(0),
                        backgroundColor: 'rgba(32,178,170,0.22)',
                        borderColor: '#FFD700',
                        borderWidth: 2,
                        pointBackgroundColor: EMOTION_COLORS,
                        pointRadius: 7,
                        pointHoverRadius: 13,
                        pointBorderColor: '#FFD700',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 4/3,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#222',
                            titleColor: '#FFD700',
                            bodyColor: '#FFD700',
                            borderColor: '#FFD700',
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return `${context.label}: ${(context.parsed.r * 100).toFixed(1)}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        r: {
                            min: 0,
                            max: 1,
                            angleLines: { color: '#FFD70022' },
                            grid: { color: '#FFD70022' },
                            pointLabels: { color: '#FFD700', font: { size: 14, weight: 'bold' } },
                            ticks: {
                                color: '#FFD700',
                                font: { size: 13 },
                                callback: function(value) { return (value * 100).toFixed(0) + '%'; }
                            }
                        }
                    },
                    animation: { duration: 700 }
                }
            });
            // Emotions line chart
            const ctxLine = document.getElementById('emotionsLine').getContext('2d');
            emotionsLine = new Chart(ctxLine, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: EMOTION_LABELS.map((label, i) => ({
                        label,
                        data: [],
                        borderColor: EMOTION_COLORS[i],
                        backgroundColor: 'rgba(0,0,0,0)',
                        tension: 0.35,
                        pointRadius: 0,
                        borderWidth: 2,
                        hidden: false
                    }))
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2.5,
                    plugins: {
                        legend: { display: true, labels: { color: '#FFD700', font: { size: 12 } } },
                        tooltip: {
                            backgroundColor: '#222',
                            titleColor: '#FFD700',
                            bodyColor: '#FFD700',
                            borderColor: '#FFD700',
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return `${context.dataset.label}: ${(context.parsed.y*100).toFixed(1)}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            min: 0,
                            max: 1,
                            grid: { color: '#FFD70022' },
                            ticks: { color: '#FFD700', font: { size: 12 }, callback: v => (v*100).toFixed(0)+'%' }
                        },
                        x: {
                            grid: { color: '#FFD70022' },
                            ticks: { color: '#FFD700', font: { size: 12 } }
                        }
                    },
                    animation: { duration: 700 }
                }
            });
        }
        // Emoción interactiva avanzada
        document.addEventListener('DOMContentLoaded', () => {
            setupCharts();
            setInterval(updateMetrics, 2000);
            updateMetrics();
            // Emoción click
            document.querySelectorAll('.emotion').forEach(el => {
                el.addEventListener('click', function() {
                    document.querySelectorAll('.emotion').forEach(e2 => e2.classList.remove('selected'));
                    this.classList.add('selected', 'pulse');
                    setTimeout(() => this.classList.remove('pulse'), 700);
                    const emo = this.getAttribute('data-emotion');
                    showFeedback('Procesando emoción: ' + emo.toUpperCase() + '...');
                    fetch('/api/feel', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ emotion: emo })
                    })
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            userRadar.data.datasets[0].data = data.state;
                            userRadar.update();
                            showFeedback('Emoción ' + emo.toUpperCase() + ' activada ✔️', '#20B2AA');
                        } else {
                            showFeedback('Error al procesar emoción', '#DC143C');
                        }
                    })
                    .catch(() => showFeedback('Error de red', '#DC143C'));
                });
            });
        });
        // Selección múltiple avanzada
        function runUserEmotions() {
            const selectedEmotions = Array.from(document.getElementById('emotionSelect').selectedOptions).map(option => option.value);
            if (selectedEmotions.length === 0) {
                showFeedback('Selecciona al menos una emoción', '#DC143C');
                return;
            }
            showLoading(true);
            // Mezcla proporcional
            let vec = Array(8).fill(0);
            selectedEmotions.forEach(e => {
                const idx = EMOTION_LABELS.map(x => x.toLowerCase()).indexOf(e);
                if (idx >= 0) vec[idx] = 1 / selectedEmotions.length;
            });
            fetch('/api/feel', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ emotion: selectedEmotions[0] }) // Solo la primera para backend, pero actualizamos radar con mezcla
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    userRadar.data.datasets[0].data = vec;
                    userRadar.update();
                    showFeedback('Emociones combinadas: ' + selectedEmotions.map(e=>e.toUpperCase()).join(', '), '#FFD700');
                }
            })
            .catch(err => console.error('Error processing emotion:', err))
            .finally(() => showLoading(false));
        }
        function resetCore() {
            showLoading(true);
            fetch('/api/reset', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'reset') {
                    updateMetrics();
                    showFeedback('Sistema reseteado', '#FFD700');
                }
            })
            .catch(err => console.error('Error resetting core:', err))
            .finally(() => showLoading(false));
        }
        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            document.documentElement.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, emotions=EMOTIONS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)