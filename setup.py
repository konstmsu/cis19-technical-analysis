from setuptools import setup, find_packages

setup(name='cis19-technical-analysis',
      version='0.1',
      description='CodeIT Suisse 2019 Challenge - Technical Analysis',
      author='Konstantin Spirin',
      author_email='konstmsu@gmail.com',
      packages=find_packages(),
      install_requires=['markdown', 'gunicorn'],
      setup_requires=[
          "flake8"
      ])
