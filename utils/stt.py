import dotenv
import os
from pydantic import BaseModel
from pathlib import Path
import bentoml


dotenv.load_dotenv('.env')

# Access the environment variables
stt_api = os.getenv('stt_id')

class TranscribeRequest(BaseModel):
    audio_file: Path

class TranscribeResponse(BaseModel):
    segments: list
    word_segments: list

def transcribe_audio(request: TranscribeRequest) -> TranscribeResponse:
    with bentoml.SyncHTTPClient(stt_api) as client:
        result = client.transcribe(audio_file=request.audio_file)
    
    return TranscribeResponse(segments=result['segments'], word_segments=result['word_segments'])
