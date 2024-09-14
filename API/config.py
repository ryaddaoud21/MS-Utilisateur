import os
class Config:


    DEBUG = True

    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@mysql-db/users_db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration de RabbitMQ
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
    RABBITMQ_QUEUE_AUTH = os.getenv('RABBITMQ_QUEUE_AUTH', 'auth_requests')
    RABBITMQ_QUEUE_RESPONSES = os.getenv('RABBITMQ_QUEUE_RESPONSES', 'auth_responses')