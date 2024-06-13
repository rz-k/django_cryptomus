from setuptools import setup, find_packages


setup(
    name='django-rest-cryptomus',
    version='0.2.7',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app for integrating with Cryptomus payment gateway.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rz-k/django_cryptomus',
    author='reza karampour',
    author_email='adamak.tng@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=4.0',
    ],
)
