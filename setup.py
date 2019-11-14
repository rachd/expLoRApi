from setuptools import setup

setup(
    name='explor',
    packages=['explor'],
    include_package_data=True,
    install_requires=[
        'flask',
        'lor_deckcodes'
    ]
)