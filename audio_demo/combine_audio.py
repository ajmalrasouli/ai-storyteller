from pydub import AudioSegment
from pydub.playback import play
import os
from pathlib import Path
import numpy as np

def combine_audio_files(input_dir, output_file):
    """Combine all audio files in input directory"""
    # Initialize empty audio segment
    combined = AudioSegment.empty()
    
    # Get all wav files in order
    wav_files = sorted([f for f in os.listdir(input_dir) if f.startswith('section_') and f.endswith('.wav')])
    
    # Load and combine all audio files
    for wav_file in wav_files:
        audio = AudioSegment.from_wav(os.path.join(input_dir, wav_file))
        combined += audio
        
    # Add 1-second pause between sections for better flow
    pause = AudioSegment.silent(duration=1000)
    combined = combined + pause
    
    # Normalize the combined audio for consistent volume
    final_audio = combined.normalize()
    
    # Export to MP3
    final_audio.export(output_file, format="mp3")
    print(f"Combined audio with background music saved to {output_file}")

def main():
    input_dir = "generated_audio"
    output_file = "final_video_narration.mp3"
    
    if not os.path.exists(input_dir):
        print(f"Error: {input_dir} directory not found. Please run generate_speech.py first.")
        return
    
    try:
        combine_audio_files(input_dir, output_file)
        print("\nAudio combination completed!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
