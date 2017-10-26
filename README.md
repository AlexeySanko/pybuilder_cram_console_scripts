PyBuilder Cram Console Scripts Plugin [![Build Status](https://travis-ci.org/AlexeySanko/pybuilder_cram_console_scripts.svg?branch=master)](https://travis-ci.org/AlexeySanko/pybuilder_cram_console_scripts)
=======================

Plugin which extends PyBuilder Cram plugin with console scripts based on distutils plugin properties

Pre-requisites
---------------

Note that plugin needs target directory usage for Cram tests.
Do not change default `True` value for `cram_run_test_from_target` property.

Plugin uses `distutils_console_scripts` or `distutils_entry_points` properties
from `distutils` plugin for generating console scripts

How to use
----------

Add plugin dependency to your `build.py`
```python
use_plugin('python.distutils')
use_plugin('pypi:pybuilder_cram_console_scripts')

@init
def set_properties(project, logger):
    project.set_property('distutils_console_scripts', [
        "some_console1 = some_module1:some_function1",
        "some_console2 = some_package.some_module2:some_function2"])
```

Properties
----------

| Name | Type | Default Value | Description |
| --- | --- | --- | --- |
| cram_generate_console_scripts | bool | True | Generate console scripts into target scripts directory for testing by Cram tests |