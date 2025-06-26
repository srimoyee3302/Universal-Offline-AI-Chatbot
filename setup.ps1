# PowerShell Script to Set Up Universal Offline AI Chatbot

Write-Host "Creating Python Virtual Environment..."
python -m venv venv

Write-Host "Activating Virtual Environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Installing Requirements..."
pip install -r requirements.txt

Write-Host "Checking for Ollama..."
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama not found. Please install it from https://ollama.com"
    exit
}

Write-Host "Pulling Mistral LLM via Ollama..."
ollama pull mistral:instruct

Write-Host "Setting Hugging Face Token (you only need to do this once)"
$hfToken = Read-Host "Enter your HuggingFace API Token"
$env:HUGGINGFACEHUB_API_TOKEN = $hfToken

# Persist the token for future sessions (user scope)
[Environment]::SetEnvironmentVariable("HUGGINGFACEHUB_API_TOKEN", $hfToken, "User")

# Step 4: Check Docker installation
Write-Host "`n Checking Docker installation..." -ForegroundColor Cyan
docker --version

# Step 5: Build Docker image
Write-Host "`n Building Docker image: ai-chatbot" -ForegroundColor Cyan
docker build -t ai-chatbot .

# Step 6: Run Docker container with environment file
Write-Host "`n Running Docker container using .env" -ForegroundColor Cyan
docker run --env-file .env ai-chatbot
