import os
import tarfile
import logging
import tempfile
import contextlib

import requests


logger = logging.getLogger('update_radarr')
SERVICE_NAME = 'radarr.service'
INSTALL_PATH = '/opt/Radarr'


def main():
    logging.basicConfig(level=logging.DEBUG)
    service_status()
    logging.info('chdir /opt')
    os.chdir('/opt')
    untar_from_url(
        fetch_latest_release_url()
    )
    service_status()


def fetch_latest_release_url():
    data = requests.get('https://api.github.com/repos/Radarr/Radarr/releases').json()
    for asset in data[0]['assets']:
        if 'linux' in asset['name']:
            logger.info('Installing %s', asset['name'])
            return asset['browser_download_url']
    raise RuntimeError('Latest linux release not found')


def untar_from_url(url):
    response = requests.get(url, stream=True)
    with tempfile.NamedTemporaryFile(mode='w+b') as fp:
        for chunk in response.iter_content(chunk_size=1024 * 4096):
            if chunk:
                fp.write(chunk)
        fp.flush()
        fp.seek(0)
        logging.info('tar xf %s', fp.name)
        with tarfile.open(fileobj=fp, mode='r:gz') as tar:
            logging.info("Validating tar archive")
            for member in tar.getmembers():
                if not os.path.abspath(member.name).startswith(INSTALL_PATH):
                    raise RuntimeError(
                        "Tar archive has file outside of Radarr directory: {0}"
                        .format(member.name)
                    )
            logging.info("Validated. Extracting")
            with paused_service():
                tar.extractall()
                command('chmod go=rx -R {0}'.format(INSTALL_PATH))
                logging.info("Extracted.")


@contextlib.contextmanager
def paused_service():
    command('systemctl stop {0}'.format(SERVICE_NAME))
    yield
    command('systemctl start {0}'.format(SERVICE_NAME))


def service_status():
    command('systemctl status {0}'.format(SERVICE_NAME))


def command(cmd):
    logging.info(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
