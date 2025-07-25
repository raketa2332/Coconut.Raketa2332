import os
from dotenv import load_dotenv

load_dotenv()


class SuperAdminCreds:
    USERNAME = os.getenv("SUPER_ADMIN_LOGIN")
    PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
