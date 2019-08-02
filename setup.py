from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='django-accountkit',
      version='0.2.3',
      description='Facebook accountkit support for Django',
	  long_description=long_description,
	  long_description_content_type='text/markdown',
      author='Shahzeb Qureshi',
      author_email='shahzeb_iam@outlook.com',
	  url='https://github.com/antiproblemist/django-accountkit',
      packages=['accountkitlogin', 'accountkitlogin.templatetags'],
	  include_package_data = True,
      package_data={
		'': ['LICENSE', 'README.md'],
      },
	  license='MIT',
	  classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
		  'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 2.7',
		  'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
          'Topic :: Software Development',
          ],
      install_requires=[
		"Django >= 1.11",
		"requests >= 2.18.4",
		],
     )