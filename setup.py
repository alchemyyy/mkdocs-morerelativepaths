from setuptools import setup

setup(
    name='mkdocs-plugin-morerelativepaths',
    version='0.1',
    description='Im gay',
    packages=['plugin_morerelativepaths'],
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'morerelativepaths = plugin_morerelativepaths.plugin:MoreRelativePathsPlugin',
        ],
    },
    install_requires=[
        'mkdocs>=1.0',
    ],
)