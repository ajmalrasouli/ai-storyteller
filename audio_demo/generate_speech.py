import azure.cognitiveservices.speech as speechsdk
import os
import json
from pathlib import Path

def create_speech_config():
    """Create speech configuration with British male voice"""
    # Using credentials from .env
    speech_key = "6BMxiZqcgJl2qtp5QcaJg5XD3Ae629KvvwfcjefRB6dcqhR6vd6xJQQJ99BDACYeBjFXJ3w3AAAYACOG82Pp"
    speech_region = "eastus"
    
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )
    
    # Set British male voice
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    return speech_config

def process_transcription(transcription_file, output_dir):
    """Process transcription file and generate speech for each section"""
    with open(transcription_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by timecodes
    sections = []
    current_section = []
    current_time = None
    
    for line in content.split('\n'):
        if line.startswith('[') and line.endswith(']'):
            if current_section:
                sections.append((current_time, '\n'.join(current_section)))
            current_section = []
            current_time = line
        elif line.strip():
            current_section.append(line)
    
    if current_section:
        sections.append((current_time, '\n'.join(current_section)))
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate speech for each section
    speech_config = create_speech_config()
    
    for i, (timecode, text) in enumerate(sections):
        if not text.strip():
            continue
            
        # Create audio filename
        filename = f"section_{i:03d}.wav"
        filepath = os.path.join(output_dir, filename)
        
        # Set output format
        audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)
        
        # Create synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        # Generate speech
        print(f"Generating speech for {timecode}...")
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech generated successfully for {timecode}")
        else:
            print(f"Speech generation failed for {timecode}: {result.reason}")

def main():
    transcription_file = "../docs/video-transcription.md"
    output_dir = "generated_audio"
    
    try:
        process_transcription(transcription_file, output_dir)
        print("\nSpeech generation completed!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
