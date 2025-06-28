# PowerShell Script to Set Up Universal Offline AI Chatbot

Write-Host "`nStarting Setup for Universal Offline AI Chatbot..." -ForegroundColor Cyan

# Step 1: Create Python Virtual Environment
Write-Host "`nCreating Python Virtual Environment..."
python -m venv venv

# Step 2: Activate Virtual Environment
Write-Host "`nActivating Virtual Environment..."
& .\venv\Scripts\Activate.ps1

# Step 3: Install Python Dependencies
Write-Host "`nInstalling Python Requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Check for Ollama Installation
Write-Host "`nChecking for Ollama Installation..."
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "`nOllama not found. Please install it from https://ollama.com before continuing." -ForegroundColor Red
    exit
}

# Step 5: Pull Mistral Model via Ollama
Write-Host "`nPulling Mistral LLM via Ollama..."
ollama pull mistral:instruct

# Step 6: Hugging Face Token Setup
Write-Host "`nSetting Hugging Face Token (used for embeddings)..."
$hfToken = Read-Host "Enter your HuggingFace API Token"
$env:HUGGINGFACEHUB_API_TOKEN = $hfToken
[Environment]::SetEnvironmentVariable("HUGGINGFACEHUB_API_TOKEN", $hfToken, "User")

# Step 7: Create .env file if not exists
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file..."
    "HF_TOKEN=$hfToken" | Out-File -Encoding utf8 .env
} else {
    Write-Host "`n.env file already exists. Ensure it contains HF_TOKEN."
}

# Step 8: Check for data/ folder
if (-not (Test-Path "./data")) {
    Write-Host "`ndata/ folder not found. Creating it now..."
    New-Item -ItemType Directory -Force -Path "./data" | Out-Null
} else {
    Write-Host "`nFound data/ folder. PDF documents will be loaded from here."
}

# Step 9: Docker Check
Write-Host "`nChecking Docker Installation..."
try {
    docker --version
} catch {
    Write-Host "`nDocker not found. Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit
}

# Step 10: Build Docker Image
Write-Host "`nBuilding Docker Image: ai-chatbot"
docker build -t ai-chatbot .

# Step 11: Run Docker Container with volume mount
Write-Host "`nRunning Docker Container at http://localhost:8501"
docker run -p 8501:8501 --env-file .env -v ${PWD}/data:/app/data ai-chatbot
