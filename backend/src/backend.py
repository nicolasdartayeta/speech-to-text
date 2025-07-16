from fastapi.datastructures import UploadFile
from fastapi import FastAPI
import logging

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

trans_pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

summ_pipe = pipeline(
    "image-text-to-text",
    model="google/gemma-3n-e4b-it",
    device=device,
    torch_dtype=torch_dtype,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post('/transcribe')
async def transcribe(audio_file: UploadFile, options: dict) -> dict[str, str | None]:
    response = {}
    audio_bytes = await audio_file.read()
    response['transcription'] = trans_pipe(audio_bytes, return_timestamps=True)["text"]

    if 'summarize' in options and options['summarize']:
        transcript = response["transcription"]
        summ_message = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a professional summarizer in charge of summarizing audio transcriptions."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{transcript}"}
                ]
            }
        ]
        summary = summ_pipe(text=summ_message)
        response['summary'] = summary[0]["generated_text"][-1]["content"]
    return response

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
