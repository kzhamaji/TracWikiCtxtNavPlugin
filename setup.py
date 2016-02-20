from setuptools import setup

extra = {}

try:
    from trac.util.dist  import  get_l10n_cmdclass
    cmdclass = get_l10n_cmdclass()
    if cmdclass:
        extra['cmdclass'] = cmdclass
        extractors = [
#            ('**.py',                'python', None),
            ('**/templates/**.html', 'genshi', None),
        ]
        extra['message_extractors'] = {
            'wikictxtnav': extractors,
        }
except:
    pass

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
            'locale/*/LC_MESSAGES/*.mo',
        ]
    },
    entry_points={
        'trac.plugins': [
            'wikictxtnav.wikicreate = wikictxtnav.wikicreate',
            'wikictxtnav.wikiedit = wikictxtnav.wikiedit',
        ]
    },
    **extra
)
