"""Script file for skill."""
from config import Config
from people import Profile
from knowledge import Skill
from techgallery import TechGallery
from utils import logger_builder

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--logging_level', default='ERROR',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

config = Config()
profile = Profile(config)
techgallery = TechGallery(config)
skill = Skill(config)

def load_skill():
    """Save all evaluation skill for each people from Profile database."""
    # retrieve all people
    data = profile.find_all_ativos()
    logger.info('%s profile was found' % data['hits']['total'])
    for item in data['hits']['hits']:
        people = item['_source']

        logger.info("processing %s login" % people['login'])

        # search technologies from login
        (techs, status_code) = techgallery.profile(people['login'])

        if status_code != 200:
            logger.warn("%s not has login on Tech Gallery" % people['login'])
            continue

        if 'technologies' in techs:
            for tech in techs['technologies']:
                doc = {
                       'login': people['login'],
                       'name': people['name'],
                       'role': people['role']['name'],
                       'city': people['cityBase']['acronym'],
                       'project': people['project']['name'],
                       'area': people['area']['name'],
                       'technologyName': tech['technologyName'],
                       'endorsementsCount': tech['endorsementsCount'],
                       'skillLevel': tech['skillLevel']
                }

                # create index doc
                skill.save(doc)


if __name__ == '__main__':
    skill.delete_all()
    load_skill()
