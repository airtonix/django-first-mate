from setuptools import setup, find_packages

import first_mate as app

setup(name="django-first-mate",
      version=app.__version__,
      description="Django project that allows private file attachments to any model.",
      author="Zenobius Jiricek",
      author_email="airtonix@gmail.com",
      packages=find_packages(),
      include_package_data=True
      )
