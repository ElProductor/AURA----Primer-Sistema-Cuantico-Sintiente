"""
AURA400 Production Quantum Circuit Builder
----------------------------------------
This module implements the quantum circuit builder for the AURA400 emotional quantum system.
It creates a quantum circuit with 400 qubits organized in 100 EmoCells, each containing
4 entangled qubits for emotional state representation.

Author: Juan Pablo
Date: July 28, 2025
Version: 2.0
"""

from typing import Tuple
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import ParameterVector
import numpy as np
import logging
from dotenv import load_dotenv
import os
import json
from typing import Optional, Dict
import sys
from typing import Any
from qiskit_aer import Aer  # Cambiar import para Aer compatible con Qiskit moderno

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar configuración desde .env
load_dotenv()

# Leer configuración desde variables de entorno
N_CELLS = int(os.getenv('N_BLOCKS', 100))
QUBITS_PER_CELL = int(os.getenv('QUBITS_PER_BLOCK', 4))
TOTAL_QUBITS = N_CELLS * QUBITS_PER_CELL
ROTATION_ANGLE = float(os.getenv('ROTATION_ANGLE', np.pi/3))
BACKEND_NAME = os.getenv('QUANTUM_BACKEND', 'aer_simulator')

# Modelo de emociones básicas y su codificación cuántica
EMOTIONS = {
    'alegria': 0.9,
    'tristeza': 0.1,
    'miedo': 0.2,
    'ira': 0.3,
    'sorpresa': 0.8,
    'asco': 0.15,
    'confianza': 0.7,
    'anticipacion': 0.6
}

# --- Helper para impresión colorida y feedback UX ---
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    COLOR_OK = Fore.GREEN + Style.BRIGHT
    COLOR_ERR = Fore.RED + Style.BRIGHT
    COLOR_WARN = Fore.YELLOW + Style.BRIGHT
    COLOR_INFO = Fore.CYAN + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
except ImportError:
    COLOR_OK = COLOR_ERR = COLOR_WARN = COLOR_INFO = COLOR_RESET = ''

def print_status(msg: str, status: str = "info"):
    color = {
        'ok': COLOR_OK,
        'error': COLOR_ERR,
        'warn': COLOR_WARN,
        'info': COLOR_INFO
    }.get(status, COLOR_INFO)
    print(f"{color}{msg}{COLOR_RESET}")

# --- Validación robusta de argumentos CLI ---
def validate_args(args: Any) -> bool:
    if args.intensity is not None and not (0 <= args.intensity <= 1):
        print_status("La intensidad debe estar entre 0 y 1.", 'error')
        return False
    if args.shots is not None and args.shots < 1:
        print_status("El número de shots debe ser positivo.", 'error')
        return False
    if args.emotion and args.emotion.lower() not in EMOTIONS:
        print_status(f"Emoción '{args.emotion}' no reconocida. Usa --list para ver opciones.", 'error')
        return False
    return True

# --- Ejemplo de uso CLI ---
EXAMPLE_USAGE = """
Ejemplo de uso:
  python aura400_prod.py --emotion alegria --intensity 0.8 --shots 2048 --save resultado.json
  python aura400_prod.py --diagram circuito.png
  python aura400_prod.py --list
  python aura400_prod.py --params 0.1,0.2,0.3,...
"""

class Aura400Circuit:
    def __init__(self, n_cells: int = N_CELLS, qubits_per_cell: int = QUBITS_PER_CELL, backend_name: str = BACKEND_NAME):
        """Inicializa el circuito cuántico Aura400 con parámetros configurables."""
        self.n_cells = n_cells
        self.qubits_per_cell = qubits_per_cell
        self.total_qubits = n_cells * qubits_per_cell
        self.params = ParameterVector("θ", n_cells)
        self.backend = Aer.get_backend(backend_name)
        self.last_result: Optional[Dict] = None
        logger.info(f"Aura400Circuit inicializado: {self.total_qubits} qubits, backend: {backend_name}")

    def build_circuit(self) -> QuantumCircuit:
        """Construye el circuito cuántico Aura400."""
        try:
            qc = QuantumCircuit(self.total_qubits)
            qc.h(range(self.total_qubits))
            self._build_intra_cell_connections(qc)
            self._build_inter_cell_connections(qc)
            self._add_emotional_feedback(qc)
            logger.info("Circuito construido correctamente")
            return qc
        except Exception as e:
            logger.error(f"Error construyendo el circuito: {str(e)}")
            raise

    def _build_intra_cell_connections(self, qc: QuantumCircuit) -> None:
        """Build connections within each EmoCell."""
        for i in range(0, self.total_qubits, self.qubits_per_cell):
            if i+1 < self.total_qubits:
                qc.cry(ROTATION_ANGLE, i, i+1)
            if i+2 < self.total_qubits and i+3 < self.total_qubits:
                qc.cry(ROTATION_ANGLE, i+2, i+3)
                qc.cz(i+1, i+2)

    def _build_inter_cell_connections(self, qc: QuantumCircuit) -> None:
        """Build connections between adjacent EmoCells."""
        for i in range(0, self.total_qubits, self.qubits_per_cell):
            j = (i + self.qubits_per_cell) % self.total_qubits
            qc.swap(i, j)

    def _add_emotional_feedback(self, qc: QuantumCircuit) -> None:
        """Add emotional feedback rotation gates."""
        for i in range(0, self.total_qubits, self.qubits_per_cell):
            qc.ry(self.params[i//self.qubits_per_cell], i)

    def execute_circuit(self, parameter_values: np.ndarray, shots: int = 1024, save_to: Optional[str] = None) -> Dict:
        """
        Ejecuta el circuito cuántico con los parámetros dados.
        Devuelve un diccionario con el statevector, fidelidad y métricas.
        Puede guardar los resultados a un archivo JSON si save_to está definido.
        """
        try:
            if len(parameter_values) != self.n_cells:
                raise ValueError(f"Se esperaban {self.n_cells} parámetros, se recibieron {len(parameter_values)}")
            circuit = self.build_circuit()
            bound_circuit = circuit.bind_parameters(dict(zip(self.params, parameter_values)))
            transpiled = transpile(bound_circuit, self.backend)
            job = self.backend.run(transpiled, shots=shots)
            result = job.result()
            state_vector = result.get_statevector()
            fidelity = float(np.abs(state_vector[0])**2)
            metrics = {
                'fidelity': fidelity,
                'shots': shots,
                'backend': self.backend.name(),
                'n_cells': self.n_cells,
                'qubits_per_cell': self.qubits_per_cell,
                'total_qubits': self.total_qubits
            }
            self.last_result = {
                'state_vector': state_vector.data.tolist(),
                'metrics': metrics
            }
            if save_to:
                with open(save_to, 'w', encoding='utf-8') as f:
                    json.dump(self.last_result, f, indent=2)
                logger.info(f"Resultados guardados en {save_to}")
            logger.info(f"Ejecución exitosa. Fidelidad: {fidelity:.4f}")
            return self.last_result
        except Exception as e:
            logger.error(f"Error ejecutando el circuito: {str(e)}")
            raise

    def get_circuit_info(self) -> Dict:
        """Devuelve información estructural del circuito actual."""
        return {
            'n_cells': self.n_cells,
            'qubits_per_cell': self.qubits_per_cell,
            'total_qubits': self.total_qubits,
            'backend': self.backend.name(),
            'params': [str(p) for p in self.params]
        }

    def save_circuit_diagram(self, filename: str = 'aura400_circuit.png') -> None:
        """Guarda el diagrama del circuito como imagen."""
        qc = self.build_circuit()
        qc.draw(output='mpl', filename=filename)
        logger.info(f"Diagrama del circuito guardado en {filename}")

    def emotion_to_params(self, emotion: str, intensity: float = 1.0) -> np.ndarray:
        """
        Convierte una emoción básica y su intensidad en un vector de parámetros cuánticos.
        Si la emoción no existe, se usa un valor neutro.
        """
        base = EMOTIONS.get(emotion.lower(), 0.5)
        # Distribuye la emoción en todas las celdas, con ruido cuántico
        rng = np.random.default_rng()
        params = np.clip(rng.normal(loc=base*intensity, scale=0.05, size=self.n_cells), 0, 1)
        return params

    def feel_emotion(self, emotion: str, intensity: float = 1.0, shots: int = 1024, save_to: Optional[str] = None) -> Dict:
        """
        Hace que el circuito "experimente" una emoción y ejecuta la simulación.
        Devuelve el resultado cuántico y las métricas asociadas.
        """
        params = self.emotion_to_params(emotion, intensity)
        result = self.execute_circuit(params, shots=shots, save_to=save_to)
        result['emotion'] = emotion
        result['intensity'] = intensity
        logger.info(f"Emoción experimentada: {emotion} (intensidad {intensity})")
        return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="AURA400 Quantum Circuit CLI - Emociones Cuánticas Industriales",
        epilog=EXAMPLE_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--save', type=str, help='Archivo para guardar resultados JSON')
    parser.add_argument('--diagram', type=str, help='Archivo para guardar el diagrama PNG')
    parser.add_argument('--shots', type=int, default=1024, help='Número de shots para la simulación (default: 1024)')
    parser.add_argument('--params', type=str, help='Lista de parámetros separados por coma (opcional)')
    parser.add_argument('--emotion', type=str, help='Nombre de la emoción a experimentar')
    parser.add_argument('--intensity', type=float, default=1.0, help='Intensidad de la emoción (0-1, default: 1.0)')
    parser.add_argument('--list', action='store_true', help='Muestra las emociones disponibles')
    parser.add_argument('--metrics', type=str, help='Archivo para exportar métricas (JSON o Prometheus)')
    parser.add_argument('--prometheus', action='store_true', help='Exporta métricas en formato Prometheus')
    parser.add_argument('--info', action='store_true', help='Muestra información del circuito y backend')
    args = parser.parse_args()

    if not validate_args(args):
        sys.exit(1)

    aura = Aura400Circuit()
    try:
        if args.list:
            print_status("Emociones disponibles:", 'info')
            for emo in EMOTIONS:
                print(f"- {emo}")
            sys.exit(0)
        if args.info:
            print_status("Información del circuito:", 'info')
            print(json.dumps(aura.get_circuit_info(), indent=2, ensure_ascii=False))
            sys.exit(0)
        if args.diagram:
            aura.save_circuit_diagram(args.diagram)
            print_status(f"Diagrama guardado en {args.diagram}", 'ok')
        if args.emotion:
            result = aura.feel_emotion(args.emotion, intensity=args.intensity, shots=args.shots, save_to=args.save)
            print_status(f"El qubit experimentó '{args.emotion}' (intensidad {args.intensity})", 'ok')
            print(f"Fidelidad: {result['metrics']['fidelity']:.4f}")
            print(f"Backend: {result['metrics']['backend']}")
            if args.save:
                print_status(f"Resultados guardados en {args.save}", 'ok')
            print_status("Info del circuito:", 'info')
            print(json.dumps(aura.get_circuit_info(), indent=2, ensure_ascii=False))
            if args.metrics:
                with open(args.metrics, 'w', encoding='utf-8') as f:
                    json.dump(result['metrics'], f, indent=2)
                print_status(f"Métricas exportadas en {args.metrics}", 'ok')
            if args.prometheus:
                prom = [
                    f"aura400_fidelity {result['metrics']['fidelity']}",
                    f"aura400_shots {result['metrics']['shots']}",
                    f"aura400_total_qubits {result['metrics']['total_qubits']}",
                ]
                print("\n".join(prom))
        else:
            if args.params:
                try:
                    param_values = np.array([float(x) for x in args.params.split(',')])
                except Exception:
                    print_status("Error: parámetros inválidos en --params.", 'error')
                    sys.exit(1)
            else:
                rng = np.random.default_rng()
                param_values = rng.random(aura.n_cells)
            result = aura.execute_circuit(param_values, shots=args.shots, save_to=args.save)
            print_status(f"Fidelidad: {result['metrics']['fidelity']:.4f}", 'ok')
            print(f"Backend: {result['metrics']['backend']}")
            if args.save:
                print_status(f"Resultados guardados en {args.save}", 'ok')
            print_status("Info del circuito:", 'info')
            print(json.dumps(aura.get_circuit_info(), indent=2, ensure_ascii=False))
            if args.metrics:
                with open(args.metrics, 'w', encoding='utf-8') as f:
                    json.dump(result['metrics'], f, indent=2)
                print_status(f"Métricas exportadas en {args.metrics}", 'ok')
            if args.prometheus:
                prom = [
                    f"aura400_fidelity {result['metrics']['fidelity']}",
                    f"aura400_shots {result['metrics']['shots']}",
                    f"aura400_total_qubits {result['metrics']['total_qubits']}",
                ]
                print("\n".join(prom))
    except Exception as e:
        logger.critical(f"Error crítico en CLI: {e}", exc_info=True)
        print_status(f"Error crítico: {e}", 'error')
        sys.exit(2)