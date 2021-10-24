class Config:
    SECRET_KEY = 'P0t3()Au6(w0n7G)'


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
