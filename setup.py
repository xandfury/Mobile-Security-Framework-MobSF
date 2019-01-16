import tempfile
import logging as logger
import sys
import requests
import io
import os
import zipfile
from setuptools import setup, find_packages
from MobSF import settings
logger.basicConfig(stream=sys.stdout, level=logger.DEBUG)


_cur_dir = os.path.abspath(os.path.dirname(__file__))
MOBSF_TOOLS_LINK = "https://github.com/xandfury/mobsf_tools/archive/master.zip"
_tmp_folder = tempfile.mkdtemp(prefix='__mobsf__')


def check_mobsf_tools():
    # If the tools directory is empty - download and copy tools from remote repo.
    _tools_dir = os.path.join(_cur_dir, 'StaticAnalyzer', 'tools')
    if os.path.isdir(_tools_dir):
        # tools directory exists now check whether is empty or not
        if len(os.listdir(_tools_dir)):
            # tools directory exists and it is not empty.. A better way would be check hash
            return
    print("Downloading MobSF tools and packages")
    # clone and copy all the contents of the tools repo
    r = requests.get(MOBSF_TOOLS_LINK)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(_tmp_folder)
    print("Tools downloaded at : {}".format(_tmp_folder))


setup(
    name='MobSF',
    version=settings.MOBSF_VER,
    packages=find_packages(exclude=['*.pyc']),
    python_requires='>=3.5',
    scripts=['bin/mobsf'],
    url="https://opensecurity.in",
    license='GPL 3',
    author="Open Security",
    author_email="ajin25@gmail.com",
    classifiers=[
        "Development Status :: 6 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python",
        "Topic :: Security",
        "Topic :: Internet",
        "Topic :: Software Development :: Testing"
    ],
    package_data={
        "": ["*.txt", "*.rst"],
    },
    keywords="Android Security Penetration Testing",
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description="""Mobile Security Framework is an automated, all-in-one mobile application (Android/iOS/Windows) 
    pen-testing framework capable of performing static analysis, dynamic analysis, malware analysis and web API 
    testing.""",
    install_requires=open('requirements.txt').read().splitlines(),
)

os.rmdir(_tmp_folder)
