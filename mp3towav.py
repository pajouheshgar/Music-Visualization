import os
import sys
import subprocess

if __name__ == '__main__':
    mp3_dir = sys.argv[1]
    wav_dir = sys.argv[2]
    mp3_files = os.listdir(mp3_dir)
    for mp3_file in mp3_files:
        wav_file_name = mp3_file.replace("mp3", "wav")
        convert_command = ["mpg123", "-w", os.path.join(wav_dir, wav_file_name), os.path.join(mp3_dir, mp3_file)]
        subprocess.call(convert_command)
