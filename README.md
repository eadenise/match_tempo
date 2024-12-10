**Audio Tempo and Beat Matching**

**Overview**
This Python project leverages librosa and scipy to analyze audio files, extract rhythmic features, and identify songs with matching tempos and beat consistency. It provides a framework for tempo estimation, beat interval analysis, and clustering based on rhythmic similarity. The results are saved in a CSV file for easy reference and further processing.

**Features:
Audio Analysis:**
Extracts audio features including tempo, tempo variations, and beat intervals.
Uses multiple methods for tempo estimation to enhance accuracy.
**Song Matching:**
Compares songs based on their primary tempo, tempo variation, and beat consistency.
Allows customizable tolerance for matching criteria.
**Output:**
Matches are logged and saved in a CSV file with detailed information about the comparisons.
Technologies Used
**Libraries:**
librosa: For audio processing and feature extraction.
numpy: For numerical computations.
scipy: For statistical calculations (e.g., Pearson correlation).
pandas: For saving results in CSV format.
**Input Format:**
Compatible with MP3 audio files.
**How It Works**
Audio Analysis:

For each audio file, the program extracts the following:
Primary tempo (median of multiple methods).
Variations in tempo using librosa's rhythm features.
Beat intervals derived from beat tracking.
Results are returned as a dictionary for each file.
Song Matching:

Songs are compared based on:
Tempo difference (within a user-defined tolerance).
Similarity in tempo variations.
Consistency of beat intervals.
Matching criteria can be customized by adjusting the tolerance parameter.
Output:

Matching results are saved as a CSV file with details such as:
**File names.**
Tempos of the matching songs.
Differences in rhythmic features.
Setup and Installation
**Requirements**
Python 3.7 or higher
**Libraries:**
pip install librosa numpy scipy pandas
**File Structure**
Place your MP3 files in a directory (e.g., ./fma_small/fma_small/000).
The program will recursively process all .mp3 files in the specified directory.
**Usage**
**Run the Program**
Define your audio directory and optional tolerance:
audio_directory = "./fma_small/fma_small/000"
tolerance = 5
**Execute the script:**
python match_tempo.py
**View the results in the terminal and the generated match_tempo.csv file.**
Sample CSV Output:
File 1,File 2,Tempo 1 (BPM),Tempo 2 (BPM),Tempo Difference,Tempo Variation Difference,Beat Consistency Difference
song1.mp3,song2.mp3,120.0,121.0,1.0,0.5,0.05
song3.mp3,song4.mp3,100.0,101.0,1.0,0.3,0.02
**Customization**
Adjust the tolerance parameter to control how lenient the matching criteria are for tempo differences.
Extend the analyse_audio function to include additional features, such as spectral centroid or chroma.
**Potential Applications**
Music Playlist Curation: Group songs with similar tempos for seamless transitions.
Audio Loop Matching: Identify loops that share similar rhythmic characteristics.
Music Recommendation Systems: Suggest songs based on rhythmic similarity.
