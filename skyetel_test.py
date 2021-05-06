from skyetel import *
from credentials import *


def main():
    skyetel_ob = Skyetel(x_auth_sid, x_auth_secret)
    print("Account Balance: {}".format(skyetel_ob.get_billing_balance()))
    audiorec = skyetel_ob.get_audio_recordings_list()
    print("Audio Recording List: {}".format(audiorec))
    print("Audio Recording URL: {}".format(skyetel_ob.get_audio_recording_url(audiorec[0].id)))
    audiotran = skyetel_ob.get_audio_transcriptions_list()
    print("Audio Transcription List: {}".format(audiotran))
    print("Audio Transcription URL: {}".format(skyetel_ob.get_audio_transcription_url(audiotran[0].id)))
    print("Audio Transcription Text: {}".format(skyetel_ob.get_audio_transcription_text(audiotran[0].id)))
    print("Organizaion Statement (Current): {}".format(skyetel_ob.get_organization_statement()))
    print("Organizaion Statement (April 2021): {}".format(skyetel_ob.get_organization_statement(2021, 3)))
    print("Endpoints List: {}".format(skyetel_ob.get_endpoints_list()))
    phonenum = skyetel_ob.get_phonenumbers(items_per_page=20)
    print("Phone Numbers List: {}".format(phonenum))
    print("E911 Address: {}".format(skyetel_ob.get_phonenumber_e911(phonenum[2].id)))


if __name__ == '__main__':
    main()
