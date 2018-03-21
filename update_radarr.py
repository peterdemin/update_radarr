import os
import tempfile
import logging

import requests


logger = logging.getLogger('update_radarr')


def main():
    logging.basicConfig(level=logging.DEBUG)
    os.chdir('/opt/Radarr')
    untar_from_url(
        fetch_latest_release_url()
    )


def fetch_latest_release_url():
    data = requests.get('https://api.github.com/repos/Radarr/Radarr/releases').json()
    for asset in data[0]['assets']:
        if 'linux' in asset['name']:
            logger.info('Installing %s', asset['name'])
            return asset['browser_download_url']
    raise RuntimeError('Latest linux release not found')


def untar_from_url(url):
    response = requests.get(url, stream=True)
    with tempfile.NamedTemporaryFile() as fp:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                fp.write(chunk)
        fp.close()
        os.system('tar xf {0}'.format(fp.name))


if __name__ == '__main__':
    main()
