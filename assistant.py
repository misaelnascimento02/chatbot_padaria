from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from session_manager import SessionManager
from session_manager import SessionManager

import logging
import actions
from configManager import  ConfigManager

logger = logging.getLogger('TelegramBot')


class IBMAssistant:
    def __init__(self, chatId):
        self.chat_id = chatId
               
        authenticator = IAMAuthenticator(
            ConfigManager.get_ibm_token())
        self.assistant_id = ConfigManager.get_ibm_assistent_id()

        self.assistant = AssistantV2(
            version='2020-02-05',
            authenticator=authenticator
        )

        self.assistant.set_service_url(ConfigManager.get_ibm_assistent_url())
        
        self.validate_session()

    def create_session(self):
        response = self.assistant.create_session(self.assistant_id)
        return response.get_result()['session_id']

    def validate_session(self):
        # check if session is valid for current chat_id
        logger.info('Validando sessão de ' + str(self.chat_id))
        if not SessionManager.getInstance().checkSession(self.chat_id):
            self.session_id = self.create_session()
            logger.info('Sessão criada para ' + str(self.chat_id))
        else:
            self.session_id = SessionManager.getInstance().getSession(self.chat_id)
            logger.info('Sessão atualizada para ' + str(self.chat_id))

        SessionManager.getInstance().updateSession(self.chat_id, self.session_id)

    def execute_action(self, response):
        # verifica se a resposta tem acao para ser executada
        if 'actions' in response['output']:
            action = response['output']['actions'][0]
            logger.info('Executando ação ' + action['name'])
            # executa a ação correta e recebe dados em um dicionario
            action['parameters']['cliente_id'] = self.chat_id
            result_data = actions.action_handler(
                action['name'], action['parameters'], action['result_variable'])
            # envia dados de resposta como contexto para o Watson Assistant
            response = self.assistant.message(
                assistant_id=self.assistant_id,
                session_id=self.session_id,
                context=result_data
            ).get_result()
        return response

    def send_message(self, message):
        logger.info('Enviando mensagem para o Assistant: ' + message)
        response = self.assistant.message(
            assistant_id=self.assistant_id,
            session_id=self.session_id,
            input={
                'message_type': 'text',
                'text': message
            }
        )
        result = response.get_result()
        logger.info(result)
        result = self.execute_action(result)
        logger.info('Recebido do assistant: ' +
                    result['output']['generic'][0]['text'])
        return result['output']['generic'][0]['text']
