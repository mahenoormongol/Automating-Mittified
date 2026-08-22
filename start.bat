@echo off
title Mittified - Setup ^& Launch
color 0A
echo.
echo  ==========================================
echo  ::        MITTIFIED - Auto Setup         ::
echo  ::  Pakistani Drama/News Instagram Bot   ::
echo  ==========================================
echo.

:: ── Step 0: Find this script's directory ──
cd /d "%~dp0"
set "PROJECT_DIR=%cd%"
set "VENV_PY=%PROJECT_DIR%\.venv\Scripts\python.exe"
set "VENV_PIP=%PROJECT_DIR%\.venv\Scripts\pip.exe"
echo [*] Project directory: %PROJECT_DIR%
echo.

:: ── Step 1: Check Python ──
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo  Please install Python 3.11+ from:
    echo  https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% found
echo.

:: ── Step 2: Create virtual environment ──
echo [2/6] Setting up virtual environment...
if not exist "%VENV_PY%" (
    echo  Creating .venv ...
    python -m venv "%PROJECT_DIR%\.venv"
    if not exist "%VENV_PY%" (
        echo [ERROR] Failed to create virtual environment!
        echo  Try manually: python -m venv .venv
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created
) else (
    echo  [OK] Virtual environment already exists
)
echo.

:: ── Step 3: Install dependencies ──
echo [3/6] Installing Python packages...
echo  This might take 2-3 minutes on first run...
"%VENV_PIP%" install --quiet --upgrade pip 2>nul
"%VENV_PIP%" install --quiet -r "%PROJECT_DIR%\requirements.txt" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Some packages had issues. Retrying with full output...
    "%VENV_PIP%" install -r "%PROJECT_DIR%\requirements.txt"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Package installation failed. Please check the errors above.
        echo  You can try manually: .venv\Scripts\pip install -r requirements.txt
        pause
        exit /b 1
    )
)
:: instagrapi hard-pins pydantic, so install it without pulling its own pydantic
echo  Installing instagrapi (separate to avoid pydantic conflict)...
"%VENV_PIP%" install --quiet --no-deps instagrapi>=2.1,<3 2>nul
echo [OK] All packages installed
echo.

:: ── Step 4: Install Playwright browsers ──
echo [4/6] Setting up Playwright (browser automation)...
"%VENV_PY%" -m playwright install chromium >nul 2>&1
if %errorlevel% neq 0 (
    echo [NOTE] Playwright browser install had issues. Image generation via Gemini may not work.
    echo  You can manually run: .venv\Scripts\python -m playwright install chromium
) else (
    echo [OK] Playwright Chromium installed
)
echo.

:: ── Step 5: Create .env if missing ──
echo [5/6] Checking configuration...
if not exist "%PROJECT_DIR%\.env" (
    if exist "%PROJECT_DIR%\.env.example" (
        copy "%PROJECT_DIR%\.env.example" "%PROJECT_DIR%\.env" >nul
        echo [OK] Created .env from template - configure via dashboard
    ) else (
        echo [NOTE] No .env file found. The dashboard will guide you through setup.
        echo # Mittified - configure via dashboard at http://localhost:8000> "%PROJECT_DIR%\.env"
    )
) else (
    echo [OK] .env file exists
)
echo.

:: ── Step 6: Create data directories ──
echo [6/6] Creating data directories...
if not exist "%PROJECT_DIR%\data\media\generated" mkdir "%PROJECT_DIR%\data\media\generated"
if not exist "%PROJECT_DIR%\data\media\carousels" mkdir "%PROJECT_DIR%\data\media\carousels"
if not exist "%PROJECT_DIR%\data\media\stories" mkdir "%PROJECT_DIR%\data\media\stories"
if not exist "%PROJECT_DIR%\data\media\thumbnails" mkdir "%PROJECT_DIR%\data\media\thumbnails"
if not exist "%PROJECT_DIR%\data\media\videos" mkdir "%PROJECT_DIR%\data\media\videos"
if not exist "%PROJECT_DIR%\data\browser_sessions" mkdir "%PROJECT_DIR%\data\browser_sessions"
echo [OK] Data directories ready
echo.

:: ── All done - Launch ──
echo  ==========================================
echo  ::         Setup Complete!               ::
echo  ==========================================
echo.
echo  Starting Mittified dashboard...
echo  Opening http://localhost:8000 in your browser...
echo.
echo  Press Ctrl+C to stop the server.
echo  ------------------------------------------
echo.

:: Open browser after a short delay (in background)
start "" cmd /c "timeout /t 3 /noq >nul & start http://localhost:8000"

:: Run the app using the venv python directly
set PYTHONUNBUFFERED=1
"%VENV_PY%" "%PROJECT_DIR%\run.py"

:: If we get here, the server stopped
echo.
echo  Mittified server stopped.
pause
