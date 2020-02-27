import logging
from archive.common import configuration
from archive import Archive


config = configuration.mix_configs([
    configuration.default_config,
    configuration.get_file_config('config.json'),
    configuration.get_cli_config()
])

logging.basicConfig(format="%(asctime)s:" + logging.BASIC_FORMAT, level=logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("slack").setLevel(logging.WARNING)
logging.getLogger("archive").setLevel(getattr(logging, config['log_level'].upper()))

a = Archive(config)


def fetch():
    a.fetch_all.recurse(begin_anew=config.get('begin_anew'))


def render():
    a.render_all.recurse(begin_anew=config.get('begin_anew'))


if __name__ == "__main__":
    fetch()
    render()
