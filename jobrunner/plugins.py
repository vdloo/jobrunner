from glob import glob

from jobrunner.settings import PROJECT_DIR


def load_all_plugins():
    """
    Load all registered jobs from the flows directory
    :return None:
    """
    for module in glob(PROJECT_DIR + '/flows/*/*/*.py'):
        plugin = module.split(
            '/flows/'
        )[1].replace('/', '.').replace('.py', '')
        __import__('flows.' + plugin)
