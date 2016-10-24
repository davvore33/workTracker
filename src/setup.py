from distutils.core import setup

setup(
    name='workTracker',
    version='0.0',
    packages=[''],
    package_dir={'': 'src'},
    url='https://github.com/davvore33/workTracker',
    license='GPLv3',
    author='Matteo Triggiani',
    author_email='davvore33@gmail.com',
    description='those scripts allows you to get events from a google calendar ', requires=['PyQt5', 'httplib2',
                                                                                            'apiclient', 'oauth2client',
                                                                                            'DateTime']
)
