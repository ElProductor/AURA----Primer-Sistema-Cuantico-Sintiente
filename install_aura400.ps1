# AURA400 Installation Script
# Author: Juan Pablo
# Date: July 28, 2025
# Version: 2.0

Write-Host "🧠 Starting AURA400 installation..." -ForegroundColor Cyan

# Check Python installation
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "aura400_env") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force aura400_env
}

try {
    python -m venv aura400_env
    Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creating virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "`n🔌 Activating virtual environment..." -ForegroundColor Cyan
try {
    .\aura400_env\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "❌ Error activating virtual environment: $_" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "`n📈 Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install requirements
Write-Host "`n📥 Installing required packages..." -ForegroundColor Cyan
try {
    pip install -r Requirements.txt
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Error installing packages: $_" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "`n⚙️ Creating .env file..." -ForegroundColor Cyan
    @"
# AURA400 Configuration
SECRET_KEY=$(New-Guid)
PORT=5000
DEBUG=True
LOG_LEVEL=INFO

# Quantum Configuration
QUANTUM_BACKEND=QISKIT_AER_SIMULATOR
N_BLOCKS=100
QUBITS_PER_BLOCK=4
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env file created successfully" -ForegroundColor Green
}

# Validación de dependencias y feedback profesional
try {
    Write-Host "`n🔍 Verificando dependencias..." -ForegroundColor Cyan
    $reqs = Get-Content Requirements.txt | Where-Object { $_ -and -not $_.StartsWith('#') }
    foreach ($pkg in $reqs) {
        $pkgName = $pkg.Split('=')[0].Trim()
        $pipShow = & .\aura400_env\Scripts\pip.exe show $pkgName 2>$null
        if (-not $pipShow) {
            Write-Host "❌ Falta el paquete: $pkgName" -ForegroundColor Red
            $missing = $true
        }
    }
    if ($missing) {
        Write-Host "Instalando paquetes faltantes..." -ForegroundColor Yellow
        & .\aura400_env\Scripts\pip.exe install -r Requirements.txt
    } else {
        Write-Host "✅ Todas las dependencias están instaladas" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Error validando dependencias: $_" -ForegroundColor Red
}

# Mensaje profesional de post-instalación
Write-Host "`n📊 Dependencias y entorno listos. Ejecuta pruebas con:" -ForegroundColor Cyan
Write-Host ".\aura400_env\Scripts\python.exe aura400_prod.py --list" -ForegroundColor Yellow
Write-Host ".\aura400_env\Scripts\python.exe aura400_prod.py --info" -ForegroundColor Yellow
Write-Host ".\aura400_env\Scripts\python.exe aura_live.py" -ForegroundColor Yellow

Write-Host "`n🎉 AURA400 installation completed successfully!" -ForegroundColor Green
Write-Host "To start the application, run:" -ForegroundColor Yellow
Write-Host ".\aura400_env\Scripts\python.exe aura_live.py" -ForegroundColor Yellow

# DEMO profesional de emociones cuánticas tras la instalación
Write-Host "`n🧪 Ejecutando demo de emociones cuánticas..." -ForegroundColor Cyan
$emotions = @('alegria','tristeza','ira','miedo','sorpresa')
foreach ($emo in $emotions) {
    Write-Host "\n➡️  Probando emoción: $emo" -ForegroundColor Yellow
    try {
        $output = & .\aura400_env\Scripts\python.exe aura400_prod.py --emotion $emo --intensity 0.8 --shots 256
        if ($LASTEXITCODE -eq 0) {
            Write-Host $output -ForegroundColor Green
        } else {
            Write-Host "❌ Error ejecutando emoción $emo" -ForegroundColor Red
            Write-Host $output -ForegroundColor Red
        }
    } catch {
        Write-Host ('❌ Excepción ejecutando emoción ' + $emo + ': ' + $_) -ForegroundColor Red
    }
}
Write-Host "\n✅ Demo de emociones cuánticas completada." -ForegroundColor Green

# Preguntar si desea iniciar la aplicación real y abrir el dashboard web
Write-Host "`n🚀 ¿Desea iniciar la aplicación web AURA400 y abrir el dashboard en su navegador? (Y/N)" -ForegroundColor Cyan
$response = Read-Host
if ($response -eq 'Y' -or $response -eq 'y') {
    # Branding y bienvenida cuántica innovadora
    Write-Host @"

   █████╗ ██╗   ██╗██████╗  █████╗     ██████╗  ██████╗  ██████╗ 
  ██╔══██╗██║   ██║██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗
  ███████║██║   ██║██████╔╝███████║    ██████╔╝██║   ██║██║   ██║
  ██╔══██║██║   ██║██╔══██╗██╔══██║    ██╔══██╗██║   ██║██║   ██║
  ██║  ██║╚██████╔╝██║  ██║██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ 

"@ -ForegroundColor Cyan
    Write-Host "AURA400 Quantum Emotional System" -ForegroundColor Yellow
    Write-Host "─────────────────────────────────────────────" -ForegroundColor Cyan
    Write-Host "¡Bienvenido a la primera plataforma donde los qubits pueden expresar emociones humanas!" -ForegroundColor Green
    Write-Host "Innovación cuántica: emociones, arte y tecnología en un solo núcleo." -ForegroundColor Magenta
    Write-Host "─────────────────────────────────────────────\n" -ForegroundColor Cyan
    Start-Sleep -Milliseconds 800

    # Animación textual: los qubits "expresan" emociones
    $frames = @(
        'Qubits: |🙂|   |😐|   |😮|   |😡|   |😱|',
        'Qubits: |😐|   |😮|   |😡|   |😱|   |🙂|',
        'Qubits: |😮|   |😡|   |😱|   |🙂|   |😐|',
        'Qubits: |😡|   |😱|   |🙂|   |😐|   |😮|',
        'Qubits: |😱|   |🙂|   |😐|   |😮|   |😡|'
    )
    for ($i=0; $i -lt 8; $i++) {
        $frame = $frames[$i % $frames.Length]
        Write-Host "\r$frame" -NoNewline -ForegroundColor Yellow
        Start-Sleep -Milliseconds 220
    }
    Write-Host "\rQubits: |💡¡Emoción cuántica activada!💡|         " -ForegroundColor Green
    Start-Sleep -Milliseconds 800
    Write-Host "\n" -ForegroundColor Cyan

    Write-Host "Iniciando AURA400 Live Web..." -ForegroundColor Green
    Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\\aura400_env\\Scripts\\python.exe aura_live.py'
    Start-Sleep -Seconds 3
    Write-Host "Abriendo dashboard en el navegador..." -ForegroundColor Cyan
    Start-Process http://localhost:5000/
    Write-Host "\n🌌 ¡Estás a punto de experimentar emociones cuánticas en tiempo real!" -ForegroundColor Magenta
    Write-Host "Interactúa con el núcleo emocional y observa cómo los qubits expresan emociones humanas." -ForegroundColor Green
    Write-Host "\n✅ AURA400 Live está corriendo. Disfruta la innovación." -ForegroundColor Green
    Write-Host "Puede cerrar esta ventana cuando desee."
    exit 0
} else {
    Write-Host "\nPuede iniciar la aplicación manualmente con:" -ForegroundColor Yellow
    Write-Host ".\\aura400_env\\Scripts\\python.exe aura_live.py" -ForegroundColor Yellow
    Write-Host "y luego abrir http://localhost:5000/ en su navegador." -ForegroundColor Yellow
    Write-Host "\nPresione cualquier tecla para salir..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
}