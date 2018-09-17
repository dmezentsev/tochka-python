import configparser
import os


def get_db_url(config_path):
    dirname = os.path.dirname(__file__)
    cp = configparser.ConfigParser()
    cp.read('{}/__config__/{}'.format(dirname, config_path))
    db_config = cp['default']
    return '{protocol}://{user}:{password}@{host}:{port}/{dbname}'.format(
        protocol=db_config.get('protocol', 'postgresql'),
        user=db_config.get('user', 'postgres'),
        password=db_config.get('password', ''),
        host=db_config.get('host', 'localhost'),
        port=int(db_config.get('port', 5432)),
        dbname=db_config.get('dbname', 'postgres')
    )
