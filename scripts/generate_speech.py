import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

def create_speech_config(speech_key, speech_region):
    if not speech_key or not speech_region:
        raise ValueError("Please provide speech key and region")
    
    return SpeechConfig(subscription=speech_key, region=speech_region)

def generate_speech(text, output_file, speech_key, speech_region):
    speech_config = create_speech_config(speech_key, speech_region)
    
    # Set output format to MP3
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    
    # Configure audio output
    audio_config = AudioOutputConfig(filename=output_file)
    
    # Create synthesizer
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    # Generate speech
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == 0:  # 0 is the value for SynthesizingAudioCompleted in newer SDK versions
        print(f"Successfully generated speech for: {output_file}")
    else:
        print(f"Speech generation failed: {result.reason}")

def main(speech_key, speech_region):
    # Create output directory if it doesn't exist
    output_dir = "audio_demo"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create playlist file
    playlist_file = os.path.join(output_dir, "playlist.txt")
    with open(playlist_file, "w", encoding="utf-8") as playlist:
        # Read the transcription
        with open("docs/video-transcription.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split into sections
        sections = content.split("###")[1:]  # Skip first empty section
        
        # Process each section with sequence numbers
        for i, section in enumerate(sections, 1):
            title = section.split("\n")[0].strip()  # Get section title
            text = "\n".join(section.split("\n")[1:])  # Get section content
            
            # Skip timestamps and empty lines
            text = "\n".join(line for line in text.split("\n") if not line.startswith("[") and line.strip())
            
            # Create output filename with sequence number
            filename = f"{output_dir}/{i:02d}_{title.lower().replace(' ', '_')}.mp3"
            
            # Generate speech
            generate_speech(text, filename, speech_key, speech_region)
            
            # Add to playlist
            playlist.write(f"{filename}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python generate_speech.py <speech_key> <speech_region>")
        sys.exit(1)
    
    speech_key = sys.argv[1]
    speech_region = sys.argv[2]
    main(speech_key, speech_region)
