"""Script file for skill."""
import logging
from config import Config
from people import Profile
from knowledge import Skill
from techgallery import TechGallery

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

config = Config()
profile = Profile(config)
techgallery = TechGallery(config)
skill = Skill(config)


def load_skill():
    """Save all evaluation skill for each people from Profile database."""
    # retrieve all people
    data = profile.find_all()
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
    load_skill()
