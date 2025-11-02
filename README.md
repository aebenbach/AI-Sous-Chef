# AI-Sous-Chef

A cooking assistant that lets you talk to your recipe.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
uv sync
```

## Speech Model

Download a Vosk speech recognition model from [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models).

**Recommended:**    
`vosk-model-small-en-us-0.15` (lightweight but less accurate).  
or  
`vosk-model-en-us-0.22` (large but more accurate)  

Unzip the model and place it in the `models/` directory.

## API Keys

You’ll need API keys for both OpenAI and PicoVoice.
Set them in a `.env` file:

```
OPENAI_API_KEY=<your_openai_key>
PICOVOICE_API_KEY=<your_picovoice_key>
```

## Run the App

1. Download a recipe PDF and save to `recipes/pdf`

2. Start the application with:

```bash
python -m app.main --recipe <recipe-name>
```

3. Use the wakeword "Jarvis" then ask your question!
