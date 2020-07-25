import os
class ConfigManager:
    def get_ibm_token():
        return os.environ['IBM_WAT_IAM_TOKEN']

    def get_ibm_assistent_id():
        return os.environ['IBM_WAT_ASSISTANT_ID']

    def get_ibm_assistent_url():
        return os.environ['IBM_WAT_URL']

    def get_telegram_token():
        return os.environ['BOT_TOKEN'] 

    def get_t2s_token():
        return os.environ['IBM_WAT_T2S_IAM_TOKEN'] 

    def get_s2t_token():
        return os.environ['IBM_WAT_S2T_IAM_TOKEN']      

    def get_t2s_url():
        return os.environ['IBM_WAT_T2S_URL'] 

    def get_s2t_url():
        return os.environ['IBM_WAT_S2T_URL']              


    