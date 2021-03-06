# -*- coding: utf-8 -*-
# This file is part of EXMO2010 software.
# Copyright 2013 Al Nikolov
# Copyright 2013 Foundation "Institute for Information Freedom Development"
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.urlresolvers import reverse
from model_mommy import mommy

from core.test_utils import BaseSeleniumTestCase
from exmo2010.models import User, Monitoring, Organization, Task, Parameter, Score, MONITORING_INTERACTION


class AutoScoreCommentTestCase(BaseSeleniumTestCase):
    ''' Tests automatic comments insertion when editing scores on score page '''

    def setUp(self):
        # GIVEN expertB account
        expertB = User.objects.create_user('expertB', 'expertB@svobodainfo.org', 'password')
        expertB.profile.is_expertB = True

        # AND INTERACTION monitoring with organization, and task
        monitoring = mommy.make(Monitoring, status=MONITORING_INTERACTION)
        organization = mommy.make(Organization, monitoring=monitoring)
        task = mommy.make(
            Task,
            organization=organization,
            user=expertB,
            status=Task.TASK_APPROVED,
        )

        # AND parameter with only 'accessible' attribute
        parameter = mommy.make(
            Parameter,
            monitoring=monitoring,
            complete = False,
            accessible = True,
            topical = False,
            hypertext = False,
            document = False,
            image = False,
            npa = False
        )

        # AND score with zero initial values for parameter attributes
        score = mommy.make(Score, task=task, parameter=parameter, found=0, accessible=0)

        # AND i am logged in as expertB
        self.login('expertB', 'password')
        # AND i am on score page
        self.get(reverse('exmo2010:score_view', args=(score.pk,)))
        # AND i opened change score tab
        self.find('a[href="#change_score"]').click()

    def test_all_maximum_scores(self):
        # WHEN i set all values to (maximum)
        self.find('#id_found_2').click()
        self.find('#id_accessible_3').click()

        with self.frame('iframe'):
            # THEN 3 comment lines should be added automatically
            self.assertEqual(len(self.findall('input.autoscore')), 3)

            # AND intro line should say that value changed to maximum (have 'max' class)
            cls = self.find('#autoscore-intro').get_attribute('class')
            self.assertTrue('max' in cls)

            # AND all other lines should say that values changed
            text = self.find('#found_brick').get_attribute('value')
            self.assertTrue(text.endswith(u'0 → 1'))
            text = self.find('#accessible_brick').get_attribute('value')
            self.assertTrue(text.endswith(u'0 → 3'))

    def test_two_scores(self):
        # WHEN i set 'found' value to 1 (maximum)
        self.find('#id_found_2').click()

        # AND i set 'accessible' value to 2 (NOT maximum)
        self.find('#id_accessible_2').click()

        with self.frame('iframe'):
            # THEN 3 comment lines should be added automatically
            self.assertEqual(len(self.findall('input.autoscore')), 3)

            # AND intro line should say that value changed, not to maximum (no 'max' class)
            cls = self.find('#autoscore-intro').get_attribute('class')
            self.assertFalse('max' in cls)

            # AND second line should say that 'found' changed from 0 to 1
            text = self.find('#found_brick').get_attribute('value')
            self.assertTrue(text.endswith(u'0 → 1'))

            # AND third line should say that 'accessible' changed from 0 to 2
            text = self.find('#accessible_brick').get_attribute('value')
            self.assertTrue(text.endswith(u'0 → 2'))

    def test_autoremove_autoscore_comments(self):
        # WHEN i set 'found' value to 1
        self.find('#id_found_2').click()

        with self.frame('iframe'):
            # THEN 2 comment lines should be added automatically
            self.assertEqual(len(self.findall('input.autoscore')), 2)

        # WHEN i set 'found' value back to 0
        self.find('#id_found_1').click()

        with self.frame('iframe'):
            # THEN all comment lines should be removed automatically
            self.assertEqual(len(self.findall('input.autoscore')), 0)

    def test_disable_submit(self):
        # WHEN nothing is typed in comment area explicitly
        # AND i set 'found' value to 1
        self.find('#id_found_2').click()

        # THEN submit button should stay disabled
        self.wait_enabled('#submit_score_and_comment', False)

        with self.frame('iframe'):
            # WHEN i type something in the comment area
            self.find('body').send_keys('hi')

        # THEN submit button should be enabled
        self.wait_enabled('#submit_score_and_comment')

        with self.frame('iframe'):
            # WHEN i erase text in the comment area
            self.find('body').send_keys('\b\b')

        # THEN submit button should turn disabled
        self.wait_enabled('#submit_score_and_comment', False)
