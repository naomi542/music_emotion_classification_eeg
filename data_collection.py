from playsound import playsound
import os
import numpy as np
import pandas as pd
import datetime
from datetime import timezone
import time


pwd = os.getcwd()
song_dir = os.path.join(pwd, 'Data_Collection', 'Cropped_Songs')
sound_close_eyes_path = os.path.join(song_dir, 'sound to close eyes.wav')
sound_open_eyes_path = os.path.join(song_dir, 'sound to open eyes.wav')

collected_data_dir = os.path.join(pwd, 'Data_Collection', 'Data')

def get_utc_time():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    return utc_timestamp
utc_timestamp = int(get_utc_time())


def rate_enjoyment():
    """
        Prompt participant to rate their enjoyment of the song
        Output:
            score (int): Rating from 1-5 of their enjoyment or familiarity
    """
    print(f'Please rate how enjoyable you found the song')
    scoring_prompt = 'Press 1 for enjoyable, Press 2 for neutral, Press 3 for unenjoyable. '
    score = input(scoring_prompt)
    return int(score)


def play_song(song_id):
    """
        Play song and record start and end timestamps
        Input:
            song_id: int of desired song ID
        Output:
            song_start_utc, song_end_utc
    """
    song_start_utc = get_utc_time() 
    # play song
    song_path = os.path.join(song_dir, f'{song_id}.esh.wav')
    playsound(song_path)
    song_end_utc = get_utc_time()

    return song_start_utc, song_end_utc


def run_baseline():
    """
        Gather 2 minutes of baseline where participant closes eyes
        Input:
        Output:
            baseline_start_utc, baseline_end_utc
    """

    baseline_start_utc = get_utc_time()
    # 1 beep
    playsound(sound_close_eyes_path)

    # sleep for 2 minutes
    time.sleep(60)

    # 2 beeps
    playsound(sound_open_eyes_path)
    baseline_end_utc = get_utc_time()

    return baseline_start_utc, baseline_end_utc


def log_time_and_response(df, coll_id, start_time, end_time, enjoyment_rating):
    """
        Store data into participant's dataframe 
        Input:
            df (pd.dataframe): dataframe
            coll_id (int): Baseline (0) or Song ID (1-12)
            start_time: utc start of collection ID
            end_time: utc end of collection ID
            enjoyment_rating (int): Score of 1 (enjoyable), 2 (neutral), or 3 (unenjoyable)
                                    -1 given if baseline
        Output:
            row appended to df

    """
    # Create list and append
    data = [coll_id, start_time, end_time, enjoyment_rating]
    df.loc[len(df)] = data
    return 


def run_procedure(df):
    """
        Run procedure (baseline + music playing)
    """

    # Create random order of song samples
    song_order = np.random.permutation(np.arange(1, 13))
    print(song_order)

    # Baseline (2 minutes) + 5 seconds of silence before starting
    print('Starting baseline')
    baseline_id = 0
    baseline_start_utc, baseline_end_utc = run_baseline()
    time.sleep(5)

    # Append baseline info
    log_time_and_response(df, baseline_id, baseline_start_utc, baseline_end_utc, enjoyment_rating=int(-1))

    # Loop through all songs & play and store them
    for i, song_id in enumerate(song_order):
        print(f'\nSong {i+1} of 12')

        # 1 beep
        playsound(sound_close_eyes_path)

        # 10 seconds of silence
        time.sleep(10)

        # play song
        song_start_utc, song_end_utc = play_song(song_id)

        # 10 seconds of silence
        time.sleep(10)

        # 2 beeps
        playsound(sound_open_eyes_path)

        # Promp to answer enjoyment
        enjoyment_rating = rate_enjoyment()

        # Sleep for 3 seconds then loop to next song
        time.sleep(3)

        # Store info into dataframe
        log_time_and_response(df, song_id, song_start_utc, song_end_utc, enjoyment_rating)

    # End of collection
    print('\nThanks for ur service, love u mwah <3')


def run_collection():
    """
        Run collection
    """

    subject_name = input('Enter subject name: ')
    df = pd.DataFrame(columns=['EventID', 'StartTime', 'EndTime', 'Enjoyment'])

    # Run procedure
    run_procedure(df)

    # Save dataframe to csv
    csv_path = os.path.join(collected_data_dir, f'sub-{subject_name}.csv')
    df.to_csv(csv_path)
    return


run_collection()

