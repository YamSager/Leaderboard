from setuptools import setup

setup(
    name='Leaderboard',
    packages=['Leaderboard'],
    setup_requires=['pbr'],
    pbr=True,
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
