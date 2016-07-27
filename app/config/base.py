"""
    Base Configuration File
"""
""" Put Generic Configurations here """
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'someSecretKey'

""" Put Development Specific Configurations here """
class DevelopmentConfig(Config):
    DEBUG = False

""" Put Staging Specific Configurations here """
class StagingConfig(Config):
    TESTING = True

""" Put Production Specific Configurations here """
class ProductionConfig(Config):
    pass
