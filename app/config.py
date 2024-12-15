from decouple import config

class Config:
    FILE_LINKS_PATH = config('FILE_LINKS_PATH', default='links_example.csv')
    PERIOD_TRACKING = config('PERIOD_TRACKING', default=3600) # seconds

    class Email:
        SMTP_SERVER = config('SMTP_SERVER')
        SMTP_PORT = config('SMTP_PORT')
        SMTP_PASSWORD = config('SMTP_PASSWORD')
        SENDER_EMAIL = config('SENDER_EMAIL')
        RECEIVER_EMAIL = config('RECEIVER_EMAIL')

cnfg = Config()
