from __future__ import annotations

import subprocess


def install_requirements():
    subprocess.run('pip install -r requirements.txt', shell=True)


def install_nltk_data_packages():
    subprocess.run(
        'python -m nltk.downloader stopwords punkt wordnet', shell=True,
    )


def install_spacy_data_packages():
    subprocess.run(
        'python -m spacy download --force en_core_web_sm', shell=True,
    )


if __name__ == '__main__':
    print('Initiating SetUp.')
    install_requirements()
    print(' Requirements installed.')
    install_nltk_data_packages()
    install_spacy_data_packages()
    print(' External nltk and spacy packages installed.')
    print('Setup completed successfully!')
