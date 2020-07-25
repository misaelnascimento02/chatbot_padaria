from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from io import BytesIO

import logging
from configManager import ConfigManager

logger = logging.getLogger('TelegramBot')

t2sauth = IAMAuthenticator(ConfigManager.get_t2s_token())
s2tauth = IAMAuthenticator(ConfigManager.get_s2t_token())

text2speech = TextToSpeechV1(
    authenticator=t2sauth
)

text2speech.set_service_url(ConfigManager.get_t2s_url())

speech2text = SpeechToTextV1(
    authenticator=s2tauth
)

speech2text.set_service_url(ConfigManager.get_s2t_url())

def convert_voice(audio_file):
    response = speech2text.recognize(
        audio=audio_file,
        content_type='audio/ogg',
        model='pt-BR_NarrowbandModel'
    )
    result = response.get_result()
    logger.info('Detectada frase: ' + result['results'][0]['alternatives'][0]['transcript'])
    return result['results'][0]['alternatives'][0]['transcript']

def convert_text(message):
    response = text2speech.synthesize(
        text=message,
        voice='pt-BR_IsabelaV3Voice',
        accept='audio/ogg'
    )
    logger.info('Convertando texto em voz')
    return BytesIO(response.get_result().content)
