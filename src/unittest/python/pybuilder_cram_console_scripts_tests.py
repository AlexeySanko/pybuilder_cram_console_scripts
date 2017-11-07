#   -*- coding: utf-8 -*-
#
#   Copyright 2016 Alexey Sanko
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
Tests for pybuilder_cram_console_scripts module

"""

import os
import shutil
import tempfile
from unittest import TestCase

from mock import Mock, patch
from pybuilder.core import Project
from pybuilder.errors import BuildFailedException

from pybuilder_cram_console_scripts import (
    initialize_cram_console_scripts,
    generate_cram_console_scripts
)

TEST_CONSOLE_SCRIPTS = [
    "some_console1 = some_module1:some_function1",
    "some_console2 = some_package.some_module2:some_function2"]


class CramCSPluginInitializationTests(TestCase):
    """ Test initialize_cram_console_scripts    """
    def setUp(self):
        self.project = Project("basedir")

    def test_should_set_default_properties(self):   # pylint: disable=invalid-name
        """ We need to init cram_generate_console_scripts"""
        initialize_cram_console_scripts(self.project)
        self.assertEquals(
            self.project.get_property('cram_generate_console_scripts'),
            True)

    def test_should_leave_user_specified_properties(self):  # pylint: disable=invalid-name
        """ We need to keep user-defined cram_generate_console_scripts"""
        self.project.set_property('cram_generate_console_scripts', False)
        initialize_cram_console_scripts(self.project)
        self.assertEquals(
            self.project.get_property('cram_generate_console_scripts'),
            False)


class CramCSPluginGeneratorTests(TestCase):
    """ Test generate_cram_console_scripts    """
    def setUp(self):
        self.project = Project("basedir")

    def test_should_raise_if_not_cram_run_test_from_target(self):   # pylint: disable=invalid-name
        """ Raise if cram_run_test_from_target was set to False"""
        self.project.set_property('cram_run_test_from_target', False)
        self.assertRaises(BuildFailedException, generate_cram_console_scripts,
                          self.project, Mock())

    def test_should_raise_if_distutils_werent_set(self):   # pylint: disable=invalid-name
        """
        Raise if distutils_console_scripts and
        distutils_entry_points weren't set
        """
        self.project.set_property('cram_run_test_from_target', True)
        self.assertRaises(BuildFailedException, generate_cram_console_scripts,
                          self.project, Mock())

    def test_should_raise_if_distutils_entry_points_without_console(self):  # pylint: disable=invalid-name
        """
        Raise if distutils_entry_points is set,
        but doesn't contain console_scripts
        """
        self.project.set_property(
            'distutils_entry_points', {'param1': 'value1'})
        self.project.set_property('cram_run_test_from_target', True)
        self.assertRaises(BuildFailedException, generate_cram_console_scripts,
                          self.project, Mock())

    @patch("pybuilder_cram_console_scripts.ScriptMaker.make_multiple")
    def test_should_parse_distutils_console_scripts(    # pylint: disable=invalid-name
            self, mock_make_multiple):
        """
        Test that plugin works with distutils_console_scripts property
        """
        self.project.set_property('cram_run_test_from_target', True)
        self.project.set_property('dir_dist', 'target/dist/some_pkg')
        self.project.set_property('dir_dist_scripts', 'my_scripts')
        self.project.set_property('cram_generate_console_scripts_dir', 'gen')
        self.project.set_property(
            'distutils_console_scripts', TEST_CONSOLE_SCRIPTS)
        logger_mock = Mock()
        generate_cram_console_scripts(self.project, logger_mock)
        mock_make_multiple.assert_called_once_with(TEST_CONSOLE_SCRIPTS)
        self.assertEqual(logger_mock.debug.call_count, 2)

    @patch("pybuilder_cram_console_scripts.ScriptMaker.make_multiple")
    def test_should_parse_distutils_entry_points(   # pylint: disable=invalid-name
            self, mock_make_multiple):
        """
        Test that plugin works with distutils_console_scripts property
        """
        self.project.set_property('cram_run_test_from_target', True)
        self.project.set_property('dir_dist', 'target/dist/some_pkg')
        self.project.set_property('dir_dist_scripts', 'my_scripts')
        self.project.set_property('cram_generate_console_scripts_dir', 'gen')
        self.project.set_property(
            'distutils_entry_points',
            {'console_scripts': TEST_CONSOLE_SCRIPTS})
        logger_mock = Mock()
        generate_cram_console_scripts(self.project, logger_mock)
        mock_make_multiple.assert_called_once_with(TEST_CONSOLE_SCRIPTS)
        self.assertEqual(logger_mock.debug.call_count, 2)


class CramCSPluginGeneratorWithTmpTests(TestCase):
    """ Test that generate_cram_console_scripts generates files on disk"""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.project = Project(self.tmp_dir)

    def test_should_generate_console_scripts(self):     # pylint: disable=invalid-name
        """
        Test that plugin generates console scripts
        """
        self.project.set_property('cram_run_test_from_target', True)
        self.project.set_property('dir_dist', 'target')
        self.project.set_property('dir_dist_scripts', 'my_scripts')
        self.project.set_property('cram_generate_console_scripts_dir', 'gen')
        trgt_dir = os.path.join(self.tmp_dir, 'target', 'my_scripts', 'gen')
        os.makedirs(trgt_dir)
        self.project.set_property(
            'distutils_console_scripts', TEST_CONSOLE_SCRIPTS)
        logger_mock = Mock()
        generate_cram_console_scripts(self.project, logger_mock)
        self.assertTrue(os.path.isfile(os.path.join(trgt_dir, 'some_console1')))
        self.assertTrue(os.path.isfile(os.path.join(trgt_dir, 'some_console2')))
        self.assertEqual(logger_mock.debug.call_count, 2)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
