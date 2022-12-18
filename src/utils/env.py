import os
from dotenv import load_dotenv
load_dotenv()


class vars:
    AWS_ACCCESSKEY = os.getenv('AWS_ACCCESSKEY')
    AWS_SECRETKEY = os.getenv('AWS_SECRETKEY')
    AWS_REGION = os.getenv('AWS_REGION')
    TOKEN = os.getenv("TOKEN")
    NISIT_KU_URL = os.getenv("NISIT_KU_URL")
    PIRUN_URL = os.getenv("PIRUN_URL")
