from skyetel import Skyetel
from credentials import *


def main():
    skyetel_ob = Skyetel(x_auth_sid, x_auth_secret)
    print("Account Balance: {}".format(skyetel_ob.get_billing_balance()))
    print("Audio Recording List: {}".format(skyetel_ob.get_audio_recordings_list()))
    print("Audio Recording URL: {}".format(
        skyetel_ob.get_audio_recording_url(skyetel_ob.get_audio_recordings_list()[0]['id'])))
    print("Audio Transcription List: {}".format(skyetel_ob.get_audio_transcriptions_list()))
    print("Audio Transcription URL: {}".format(
        skyetel_ob.get_audio_transcription_url(skyetel_ob.get_audio_transcriptions_list()[0]['id'])))
    print("Audio Transcription Text: {}".format(
        skyetel_ob.get_audio_transcription_text(skyetel_ob.get_audio_transcriptions_list()[0]['id'])))
    print("Organizaion Statement (Current): {}".format(skyetel_ob.get_organization_statement()))
    print("Organizaion Statement (April 2021): {}".format(skyetel_ob.get_organization_statement(2021, 3)))
    print("Endpoints List: {}".format(skyetel_ob.get_endpoints_list()))


if __name__ == '__main__':
    main()
