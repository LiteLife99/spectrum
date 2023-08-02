import torch
import whisperx
import gc
from utils.configUtil import config

HF_TOKEN = config["HF_TOKEN"]
device = 'cuda' if torch.cuda.is_available() else "cpu"
batch_size = 8 if torch.cuda.is_available() else 32 
compute_type = 'float16' if torch.cuda.is_available() else 'float32'

print('specs:', device, batch_size, compute_type)

model = whisperx.load_model('large-v2', device, compute_type=compute_type)
diarize_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device)

model_align, model_align_metadata = whisperx.load_align_model(language_code="en", device=device) 
print('load align model done')

def extract_transcription(filename):
    print('filename:', filename)
    audio = whisperx.load_audio(filename)
    print('audio load done')
    result = model.transcribe(audio, batch_size=batch_size)
    print('transcribe done')
    
    audio_transcription = ''
    audio_data = []
    for segment in result['segments']:
        audio_transcription += segment['text'] + '\n'
        seg_dict = {}
        seg_dict['start'] = segment['start']
        seg_dict['end'] = segment['end']
        seg_dict['text'] = segment['text']
        audio_data.append(seg_dict.copy())

    return {'transcription_text': audio_transcription, 'language': result['language'], 'result': result, 'transcribe_result': audio_data, 'audio': audio}

def diarization(filename, min_speakers, max_speakers):
    result_dict = extract_transcription(filename)
    print('transcribe done')
    result_align = whisperx.align(result_dict['result']["segments"], model_align, model_align_metadata, result_dict['audio'], device, return_char_alignments=False)
    print('align done')
    diarize_segments = diarize_model(filename, min_speakers=min_speakers, max_speakers=max_speakers)
    print('diarize_segments done')
    result_align_assign = whisperx.assign_word_speakers(diarize_segments, result_align)
    print('result_align_assign done')

    diarize_data = []
    for segment in result_align_assign['segments']:
        seg_dict = {}
        seg_dict['start'] = segment['start']
        seg_dict['end'] = segment['end']
        seg_dict['text'] = segment['text']
        seg_dict['speaker'] = segment['speaker']
        diarize_data.append(seg_dict.copy())

    return {'language': result_dict['language'], 'diarize_result': diarize_data}