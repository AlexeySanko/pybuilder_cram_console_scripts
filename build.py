from pybuilder.core import use_plugin, init, Author

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.frosted")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.unittest")
use_plugin("filter_resources")
# third party plugins
use_plugin('pypi:pybuilder_semver_git_tag')
use_plugin('pypi:pybuilder_pylint_extended')


name = "pybuilder_cram_console_scripts"
authors = [Author('Alexey Sanko', 'alexeycount@gmail.com')]
url = 'https://github.com/AlexeySanko/pybuilder_cram_console_scripts'
description = 'Please visit {0} for more information!'.format(url)
license = 'Apache License, Version 2.0'
summary = 'PyBuilder Cram Console Scripts Plugin'

default_task = ['clean', 'analyze', 'publish']


@init
def filter_settings(project):
    # filter target files
    project.set_property('filter_resources_target', '$dir_dist')
    # provide verions and other properties
    project.get_property("filter_resources_glob").append(
        "%s/version.py" % name)


@init
def set_properties(project):
    # dependencies
    project.build_depends_on('mock')

    # coverage
    project.set_property('coverage_break_build', True)
    project.set_property('coverage_threshold_warn', 100)
    project.set_property('coverage_branch_threshold_warn', 100)

    # flake8
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)

    # frosted
    project.set_property("frosted_break_build", True)
    project.set_property("frosted_include_test_sources", True)

    # semver git tag
    project.set_property('semver_git_tag_changelog', 'CHANGELOG.md')

    # distutils
    project.set_property('distutils_commands', ['bdist_wheel'])
    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'])
