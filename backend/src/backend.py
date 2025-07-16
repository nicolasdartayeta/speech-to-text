from fastapi.datastructures import UploadFile
from fastapi import FastAPI
import logging

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

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

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

from fastapi import Query

@app.post('/transcribe')
async def transcribe(audio_file: UploadFile, summarize: bool = Query(False)) -> dict[str, str | None]:
    response = {}
    audio_bytes = await audio_file.read()
    response['transcription'] = trans_pipe(audio_bytes, return_timestamps=True)["text"]

    if summarize:
        transcript = response["transcription"]
        summary = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=transcript,
            config=types.GenerateContentConfig(
                system_instruction="You are a professional summarizer in charge of summarizing audio transcriptions. You must mantain the original language of the transcription. Just return the summary without any additional text, context, or explanation.",
            ),
        )
        response['summary'] = summary.text

    return response

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
