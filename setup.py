from distutils.core import setup

setup(name='ws',
    version='0.1',
    description='',
    author='Jon Hill',
    author_email='jon@jonhill.ca',
    url='',
    packages = ['ws'],
    license='MIT',

    install_requires=[
        'zmq'
    ],

    entry_points={
        'console_scripts': [
            'ws = ws:main'
        ]
    }
)
