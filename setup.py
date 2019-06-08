from setuptools import setup

setup(
    name='mprisevent',
    version='0.0.0',
    author='Alistair Buxton',
    author_email='a.j.buxton@gmail.com',
    packages=['mprisevent'],
    entry_points={
        'console_scripts': [
            'mprisevent = mprisevent.mprisevent:main',
        ]
    },
    install_requires=['mpris2', 'PyGObject', 'dbus-python', 'requests'],
)
