import os
import wave
import numpy as np
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer

def add_background_music(audio_file, output_file):
    # Load narration
    with wave.open(audio_file, 'rb') as w:
        params = w.getparams()
        frames = w.readframes(w.getnframes())
        narration = np.frombuffer(frames, dtype=np.int16)
        
        # Create background music (simple sine wave)
        sample_rate = params.framerate
        duration = len(narration) // 2  # 16-bit samples
        t = np.linspace(0, duration, duration, False)
        
        # Create a simple cartoon-like melody
        # Using multiple frequencies to create a playful sound
        frequencies = [440, 554, 659]  # A4, C5, E5
        music = np.zeros(duration, dtype=np.int16)
        
        for freq in frequencies:
            # Create sine wave with higher amplitude
            note = np.sin(2 * np.pi * freq * t / sample_rate)
            note = (note * 32767 * 0.5).astype(np.int16)  # Increased to 50% volume
            music += note
        
        # Mix narration with music
        combined = narration + music
        combined = np.clip(combined, -32767, 32767)  # Prevent clipping
        
        # Save to WAV
        with wave.open(output_file, 'wb') as w:
            w.setparams(params)
            w.writeframes(combined.tobytes())

def combine_audio_files(playlist_file, output_file, speech_key, speech_region):
    # Read the playlist file
    with open(playlist_file, "r", encoding="utf-8") as f:
        files = f.read().splitlines()
    
    # Process each file in the playlist
    combined_audio = None
    
    for file_path in files:
        try:
            # Load the MP3 file
            with wave.open(file_path, 'rb') as w:
                frames = w.readframes(w.getnframes())
                audio = np.frombuffer(frames, dtype=np.int16)
                
                # Add pause between files
                if combined_audio is not None:
                    pause = np.zeros(44100, dtype=np.int16)  # 1 second pause
                    combined_audio = np.concatenate([combined_audio, pause])
                
                # Add audio
                combined_audio = np.concatenate([combined_audio, audio]) if combined_audio is not None else audio
            
            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    if combined_audio is not None:
        # Save combined audio to WAV
        temp_wav = output_file.replace('.mp3', '_temp.wav')
        with wave.open(temp_wav, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(44100)
            w.writeframes(combined_audio.tobytes())
            
        # Add background music
        add_background_music(temp_wav, temp_wav)
        
        # Convert to MP3
        os.system(f'ffmpeg -i "{temp_wav}" "{output_file}"')
        os.remove(temp_wav)
        
        print(f"Successfully created final audio with background music: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python combine_audio.py <speech_key> <speech_region> <output_file>")
        sys.exit(1)
    
    speech_key = sys.argv[1]
    speech_region = sys.argv[2]
    output_file = sys.argv[3]
    
    playlist_file = "audio_demo/playlist.txt"
    combine_audio_files(playlist_file, output_file, speech_key, speech_region)
