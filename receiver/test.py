import yaml
import logging.config

with open('./log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')
    logger.debug("Test")