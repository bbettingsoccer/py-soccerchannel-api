import os
from dotenv import load_dotenv, dotenv_values, find_dotenv


def env_check():
    env_file = None

    if os.environ['ENV_NAME'] == 'DEV':
        print("ENV DEV")
        env_file = find_dotenv("./env/.env.dev")
        load_dotenv(env_file)

    elif os.environ['ENV_NAME'] == 'PRO':
        env_file = find_dotenv("./env/.env.pro")
        load_dotenv(env_file)
    load_dotenv(env_file)
