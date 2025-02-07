# Copyright (c) OpenMMLab. All rights reserved.
import glob
import os
import os.path as osp
import time
import shutil
import ssl
from typing import Dict, List, Optional, Tuple

from mmengine import mkdir_or_exist

from mmocr.registry import DATA_OBTAINERS
from mmocr.utils import check_integrity, is_archive

ssl._create_default_https_context = ssl._create_unverified_context


@DATA_OBTAINERS.register_module()
class NaiveDataObtainer:
    """A naive pipeline for obtaining dataset.

    download -> extract -> move

    Args:
        files (list[dict]): A list of file information.
        cache_path (str): The path to cache the downloaded files.
        data_root (str): The root path of the dataset. It is usually set auto-
            matically and users do not need to set it manually in config file
            in most cases.
        task (str): The task of the dataset. It is usually set automatically
            and users do not need to set it manually in config file
            in most cases.
    """

    def __init__(self, files: List[Dict], cache_path: str, data_root: str,
                 task: str) -> None:
        self.files = files
        self.cache_path = cache_path
        self.data_root = data_root
        self.task = task
        mkdir_or_exist(self.data_root)
        mkdir_or_exist(osp.join(self.data_root, f'{task}_imgs'))
        mkdir_or_exist(osp.join(self.data_root, 'annotations'))
        mkdir_or_exist(self.cache_path)

    def __call__(self):
        for file in self.files:
            save_name = file.get('save_name', None)
            url = file.get('url', None)
            md5 = file.get('md5', None)
            download_path = osp.join(
                self.cache_path,
                osp.basename(url) if save_name is None else save_name)
            # Download required files
            if not check_integrity(download_path, md5):
                self.download(url=url, dst_path=download_path)
            # Extract downloaded zip files to data root
            self.extract(src_path=download_path, dst_path=self.data_root)
            # Move & Rename dataset files
            if 'mapping' in file:
                self.move(mapping=file['mapping'])
        self.clean()

    def download(self, url: Optional[str], dst_path: str) -> None:
        """Download file from given url with progress bar.

        Args:
            url (str): The url to download the file.
            dst_path (str): The destination path to save the file.
        """

        if url is None and not osp.exists(dst_path):
            raise FileNotFoundError(
                'Direct url is not available for this dataset.'
                ' Please manually download the required files'
                ' following the guides.')

        if url.startswith('magnet'):
            raise NotImplementedError('Please use any BitTorrent client to '
                                      'download the following magnet link to '
                                      f'{osp.abspath(dst_path)} and '
                                      f'try again.\nLink: {url}')
            
        
        def modify_url(url):
            import re

            pattern = (
                r"^https?:\/\/(?:\w+\.)?(?:github\.com|gist\.githubusercontent\.com)"
            )

            if re.match(pattern, url):
                return "https://gh.jsesnr.top/" + url

            else:
                return "https://sp.jsesnr.top/" + url.replace('https://','https/').replace('http://','http/')
        
        url = modify_url(url)

        print('Downloading...')
        print(f'URL: {url}')
        print(f'Destination: {osp.abspath(dst_path)}')
        print('If you stuck here for a long time, please check your network, '
              'or manually download the file to the destination path and '
              'run the script again.')
        for retry in range(1,21):
            if os.system(f"wget {url} -q --show-progress --progress=bar:force -N -c --no-check-certificate -O {dst_path}") == 0:
                break
            else:
                print(f"Retry {retry}/20 times.\033[1A",end="\r")
                time.sleep(1)

        print('')

    def extract(self,
                src_path: str,
                dst_path: str,
                delete: bool = False) -> None:
        """Extract zip/tar.gz files.

        Args:
            src_path (str): Path to the zip file.
            dst_path (str): Path to the destination folder.
            delete (bool, optional): Whether to delete the zip file. Defaults
                to False.
        """
        if not is_archive(src_path):
            # Copy the file to the destination folder if it is not a zip
            if osp.isfile(src_path):
                shutil.copy(src_path, dst_path)
            else:
                shutil.copytree(src_path, dst_path)
            return

        zip_name = osp.basename(src_path).split('.')[0]
        if dst_path is None:
            dst_path = osp.join(osp.dirname(src_path), zip_name)
        else:
            dst_path = osp.join(dst_path, zip_name)

        extracted = False
        if osp.exists(dst_path):
            name = set(os.listdir(dst_path))
            if '.finish' in name:
                extracted = True
            elif '.finish' not in name and len(name) > 0:
                while True:
                    c = input(f'{dst_path} already exists when extracting '
                              '{zip_name}, unzip again? (y/N) ') or 'N'
                    if c.lower() in ['y', 'n']:
                        extracted = c == 'n'
                        break
        if extracted:
            open(osp.join(dst_path, '.finish'), 'w').close()
            print(f'{zip_name} has been extracted. Skip')
            return
        mkdir_or_exist(dst_path)
        print(f'Extracting: {osp.basename(src_path)}')
        if src_path.endswith('.zip'):
            try:
                import zipfile
            except ImportError:
                raise ImportError(
                    'Please install zipfile by running "pip install zipfile".')
            with zipfile.ZipFile(src_path, 'r') as zip_ref:
                zip_ref.extractall(dst_path)
        elif src_path.endswith('.tar.gz') or src_path.endswith('.tar'):
            if src_path.endswith('.tar.gz'):
                mode = 'r:gz'
            elif src_path.endswith('.tar'):
                mode = 'r:'
            try:
                import tarfile
            except ImportError:
                raise ImportError(
                    'Please install tarfile by running "pip install tarfile".')
            with tarfile.open(src_path, mode) as tar_ref:
                tar_ref.extractall(dst_path)

        open(osp.join(dst_path, '.finish'), 'w').close()
        if delete:
            os.remove(src_path)

    def move(self, mapping: List[Tuple[str, str]]) -> None:
        """Rename and move dataset files one by one.

        Args:
            mapping (List[Tuple[str, str]]): A list of tuples, each
            tuple contains the source file name and the destination file name.
        """
        for src, dst in mapping:
            src = osp.join(self.data_root, src)
            dst = osp.join(self.data_root, dst)

            if '*' in src:
                mkdir_or_exist(dst)
                for f in glob.glob(src):
                    if not osp.exists(
                            osp.join(dst, osp.relpath(f, self.data_root))):
                        shutil.move(f, dst)

            elif osp.exists(src) and not osp.exists(dst):
                mkdir_or_exist(osp.dirname(dst))
                shutil.move(src, dst)

    def clean(self) -> None:
        """Remove empty dirs."""
        for root, dirs, files in os.walk(self.data_root, topdown=False):
            if not files and not dirs:
                os.rmdir(root)
