import librosa
import glob
import numpy as np
from librosa.feature.rhythm import tempo as rhythm_tempo
from scipy.stats import pearsonr
import pandas as pd

def analyse_audio(file):
    y, sr = librosa.load(file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    tempos = []
        
    # librosa's tempo function
    tempo_librosa = rhythm_tempo(onset_envelope=onset_env, sr=sr)[0]
    tempos.append(tempo_librosa)
    
    # onset-based tempo estimation
    onset_tempo = librosa.onset.onset_strength(y=y, sr=sr)
    tempo_onset = np.mean(rhythm_tempo(onset_envelope=onset_tempo, sr=sr))
    tempos.append(tempo_onset)
    
    # compute spectral flux onset strength envelope across multiple channels.
    spectral_flux = librosa.onset.onset_strength_multi(y=y, sr=sr)
    tempo_spectral = np.mean(rhythm_tempo(onset_envelope=spectral_flux, sr=sr))
    tempos.append(tempo_spectral)

    # compute additional rhythmic features
    beat_frames = librosa.beat.beat_track(y=y, sr=sr)[1]
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_intervals = np.diff(beat_times)
    
    return {
        'primary_tempo': np.median(tempos),  # use median of multiple methods
        'tempo_variations': tempos,
        'beat_intervals': beat_intervals,
        'tempo_std': np.std(tempos),
        'beat_consistency': np.std(beat_intervals)
    }

def match_songs(song1_analysis, song2_analysis, tolerance=5):
    if song1_analysis is None or song2_analysis is None:
        return False, {}
    
    tempo_diff = abs(song1_analysis['primary_tempo'] - song2_analysis['primary_tempo'])

    tempo_std_diff = abs(song1_analysis['tempo_std'] - song2_analysis['tempo_std'])
    beat_consistency_diff = abs(song1_analysis['beat_consistency'] - song2_analysis['beat_consistency'])


    is_tempo_match = (
        tempo_diff <= tolerance and
        abs(song1_analysis['tempo_std'] - song2_analysis['tempo_std']) < 2 and  # similar tempo variation
        abs(song1_analysis['beat_consistency'] - song2_analysis['beat_consistency'])) < 0.1  # smilar beat consistency
    
    
    return is_tempo_match, {
        'Tempo Difference': tempo_diff,
        'Tempo Variation Difference': abs(song1_analysis['tempo_std'] - song2_analysis['tempo_std']),
        'Beat Consistency Difference': abs(song1_analysis['beat_consistency'] - song2_analysis['beat_consistency'])
    }



def find_matches(files, tolerance=5):
    tempos = {}
    matches = []

    # Extract tempos for all files
    for audio in files:
        analysis = analyse_audio(audio)
        if analysis is not None: 
            tempos[audio] = analysis
        else:
            print(f"Analysis for {audio} failed.")
    
    print(f"Extracted tempos: {tempos}")

    # Compare tempos between files
    file_keys = list(tempos.keys())
    for i, file1 in enumerate(file_keys):
        for j, file2 in enumerate(file_keys):
            if i < j:  # Avoid duplicate comparisons
                is_match, match_details = match_songs(
                    tempos[file1], 
                    tempos[file2], 
                    tolerance
                )
                print(f"Comparing {file1} and {file2}: Match? {is_match}")

                if is_match:
                        matches.append({
                            'file1': file1,
                            'file2': file2,
                            'tempo1': tempos[file1]['primary_tempo'],
                            'tempo2': tempos[file2]['primary_tempo'],
                            'match_details': match_details
                        })
    return matches

if __name__ == "__main__":
    # Define audio directory and tolerance
    audio_directory = "./fma_small/fma_small/000"
    audio_files = glob.glob(f"{audio_directory}/*.mp3")
    tolerance = 5

    # find matches
    matching_files = find_matches(audio_files, tolerance)

    # save matches

    audio_data = [] 

    print("Matching Files Based on Tempo:")
for match in matching_files:
    # Print match details
    print("\nMatch found:")
    print(f"File 1: {match['file1']}")
    print(f"File 2: {match['file2']}")
    print(f"Tempos: {match['tempo1']:.2f} BPM, {match['tempo2']:.2f} BPM")
    print("Match Details:")
    for key, value in match['match_details'].items():
        print(f"  {key}: {value:.4f}")

    # Append match data to audio_data list
    audio_data.append({
        "File 1": match['file1'],
        "File 2": match['file2'],
        "Tempo 1 (BPM)": match['tempo1'],
        "Tempo 2 (BPM)": match['tempo2'],
        "Tempo Difference": match['match_details']['Tempo Difference'],
        "Tempo Variation Difference": match['match_details']['Tempo Variation Difference'],
        "Beat Consistency Difference": match['match_details']['Beat Consistency Difference']
    })

    # save the audio data to a CSV file
    audio_df = pd.DataFrame(audio_data)
    audio_csv_file = "match_tempo.csv"
    audio_df.to_csv(audio_csv_file, index=False)

        