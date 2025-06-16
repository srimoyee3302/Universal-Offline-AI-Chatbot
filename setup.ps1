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

Write-Host "Setup Complete. Launching Bot..."
python Bot.py
