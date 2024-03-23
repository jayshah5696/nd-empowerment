import dotenv
import os
from pydantic import BaseModel, validator
from pathlib import PosixPath
import bentoml
# load dot env file
# Load the .env file
dotenv.load_dotenv('.env')

# Access the environment variables
tts_api = os.getenv('tts_id')




class SynthesizeInput(BaseModel):
    lang: str
    text: str

class SynthesizeOutput(BaseModel):
    result: PosixPath

    @validator('result', pre=True)
    def convert_to_posixpath(cls, v):
        return PosixPath(v)

def synthesize_text(input_data: SynthesizeInput) -> SynthesizeOutput:
    with bentoml.SyncHTTPClient(tts_api) as client:
        result = client.synthesize(
            lang=input_data.lang,
            text=input_data.text,
        )
    return SynthesizeOutput(result=result)