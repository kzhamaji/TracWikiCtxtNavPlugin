from setuptools import setup

setup(
    name='TracWikiCtxtNavPlugin',
    #description='',
    #keywords='',
    #url='',
    version='0.1',
    #license='',
    #author='',
    #author_email='',
    #long_description="",
    packages=['wikictxtnav'],
    package_data={
        'wikictxtnav': [
            'templates/*.html',
        ]
    },
    entry_points={
        'trac.plugins': [
            'wikictxtnav.wikicreate = wikictxtnav.wikicreate',
            'wikictxtnav.wikiedit = wikictxtnav.wikiedit',
        ]
    }
)
