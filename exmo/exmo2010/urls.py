# -*- coding: utf-8 -*-
# This file is part of EXMO2010 software.
# Copyright 2010, 2011, 2013 Al Nikolov
# Copyright 2010, 2011 non-profit partnership Institute of Information Freedom Development
# Copyright 2012, 2013 Foundation "Institute for Information Freedom Development"
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
import types

from django.conf.urls import patterns, url, include
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.utils.translation import ugettext as _

import reversion

from exmo2010.forms import CertificateOrderForm
from exmo2010.views import AboutView, CertificateOrderView, HelpView, OpenDataView
from monitorings.views import MonitoringManagerView
from organizations.views import OrganizationManagerView
from parameters.views import ParameterManagerView
from scores.views import ScoreAddView, ScoreEditView, ScoreDeleteView, ScoreDetailView
from tasks.views import TaskManagerView


def named_urls(module, *urlpatterns):
    '''
    Wrapper around django.conf.urls.patterns which can guess url name from view and
    automatically converts GenericView classes to views
    Positional args are urlpatters:
        (pattern, view, [, optional_name [, optional_kwargs]])
    If the name is omitted, it will be the same as view class or view function name
    '''
    result_patterns = []
    for urlpattern in urlpatterns:
        if isinstance(urlpattern, (RegexURLResolver, RegexURLPattern)):
            result_patterns.append(urlpattern)
            continue

        kwargs = {}
        try:
            regex, view, name, kwargs = urlpattern
        except ValueError:
            try:
                regex, view, name = urlpattern
            except ValueError:
                regex, view = urlpattern

                if isinstance(view, types.TypeType):
                    name = view.__name__
                elif isinstance(view, (str, unicode)):
                    name = view.split('.')[-1]
                else:
                    name = None

        if isinstance(view, types.TypeType):
            view = view.as_view()

        result_patterns.append(url(regex, view, kwargs=kwargs, name=name))

    return patterns(module, *result_patterns)


scores_patterns = named_urls('scores.views',
    (r'^(?P<score_pk>\d+)/$', 'score_view'),
    (r'^(?P<task_pk>\d+)_(?P<parameter_pk>\d+)/$', ScoreAddView, 'score_add'),
    (r'^(?P<score_pk>\d+)/edit/$', reversion.create_revision()(ScoreEditView.as_view()), 'score_edit'),
    (r'^(?P<score_pk>\d+)/delete/$', reversion.create_revision()(ScoreDeleteView.as_view()), 'score_delete'),
    (r'^(?P<score_pk>\d+)/detail/$', ScoreDetailView, 'score_detail'),
    (r'^rating_update$', 'ratingUpdate'),
)

scores_patterns += named_urls('',
    (r'^(?P<score_pk>\d+)/claim/create/$', 'claims.views.claim_create'),
    (r'^(?P<score_pk>\d+)/clarification/create/$', 'clarifications.views.clarification_create'),
)

monitoring_patterns = named_urls('monitorings.views',
    (r'^$', 'monitoring_list'),
    (r'^add/$', 'monitoring_add'),
    (r'^(?P<monitoring_pk>\d+)/by_criteria_mass_export/$', 'monitoring_by_criteria_mass_export'),
    (r'^(?P<monitoring_pk>\d+)/comment_report/$', 'monitoring_comment_report'),
    (r'^(?P<monitoring_pk>\d+)/experts/$', 'monitoring_by_experts'),
    (r'^(?P<monitoring_pk>\d+)/organization_export/$', 'monitoring_organization_export'),
    (r'^(?P<monitoring_pk>\d+)/organization_import/$', 'monitoring_organization_import'),
    (r'^(?P<monitoring_pk>\d+)/parameter_export/$', 'monitoring_parameter_export'),
    (r'^(?P<monitoring_pk>\d+)/parameter_filter/$', 'monitoring_parameter_filter'),
    (r'^(?P<monitoring_pk>\d+)/parameter_found_report/$', 'monitoring_parameter_found_report'),
    (r'^(?P<monitoring_pk>\d+)/parameter_import/$', 'monitoring_parameter_import'),
    (r'^(?P<monitoring_pk>\d+)/rating/$', 'monitoring_rating'),
    (r'^(?P<monitoring_pk>\d+)/set_npa_params/$', 'set_npa_params'),
    (r'^(?P<monitoring_pk>\d+)_update/$', MonitoringManagerView, 'monitoring_update', {'method': 'update'}),
    (r'^(?P<monitoring_pk>\d+)_delete/$', MonitoringManagerView, 'monitoring_delete', {'method': 'delete'}),
    (r'^(?P<monitoring_pk>\d+)/export/$', 'monitoring_export'),
)

monitoring_patterns += named_urls('tasks.views',
    (r'^(?P<monitoring_pk>\d+)/mass_assign_tasks/$', 'task_mass_assign_tasks'),
    (r'^(?P<monitoring_pk>\d+)/organization/(?P<org_pk>\d+)/task/add/$', 'task_add', 'org_task_add'),   # TODO: replace with task_add
    (r'^(?P<monitoring_pk>\d+)/organization/(?P<org_pk>\d+)/tasks/$', 'tasks_by_monitoring_and_organization'),  # TODO: replace with tasks_by_monitoring
    (r'^(?P<monitoring_pk>\d+)/task/add/$', 'task_add'),
    (r'^(?P<monitoring_pk>\d+)/tasks/$', 'tasks_by_monitoring'),
)

monitoring_patterns += named_urls('organizations.views',
    (r'^(?P<monitoring_pk>\d+)/organization/(?P<org_pk>\d+)_delete/$',
        OrganizationManagerView, 'organization_delete', {'method': 'delete'}),
    (r'^(?P<monitoring_pk>\d+)/organization/(?P<org_pk>\d+)_update/$',
        OrganizationManagerView, 'organization_update', {'method': 'update'}),
    (r'^(?P<monitoring_pk>\d+)/organizations/$', 'organization_list'),
)

monitoring_patterns += named_urls('questionnaire.views',
    (r'^(?P<monitoring_pk>\d+)/add_questionnaire/$', 'add_questionnaire'),
    (r'^(?P<monitoring_pk>\d+)/answers_export/$', 'answers_export', 'monitoring_answers_export'),
)

monitoring_patterns += named_urls('',
    (r'^(?P<monitoring_pk>\d+)/claims/$', 'claims.views.claim_report'),
    (r'^(?P<monitoring_pk>\d+)/clarifications/$', 'clarifications.views.clarification_report'),
)


tasks_patterns = named_urls('tasks.views',
    (r'^task/(?P<task_pk>\d+)_update/$',
        reversion.create_revision()(TaskManagerView.as_view()), 'task_update', {'method': 'update'}),
    (r'^task/(?P<task_pk>\d+)_delete/$',
        reversion.create_revision()(TaskManagerView.as_view()), 'task_delete', {'method': 'delete'}),
    (r'^taskexport/(?P<task_pk>\d+)/$', 'task_export'),
    (r'^taskimport/(?P<task_pk>\d+)/$', 'task_import'),
)

tasks_patterns += named_urls('parameters.views',
    (r'^task/(?P<task_pk>\d+)/parameter/(?P<parameter_pk>\d+)_update/$',
        ParameterManagerView, 'parameter_update', {'method': 'update'}),
    (r'^task/(?P<task_pk>\d+)/parameter/(?P<parameter_pk>\d+)_delete/$',
        ParameterManagerView, 'parameter_delete', {'method': 'delete'}),
    (r'^task/(?P<task_pk>\d+)/parameter/(?P<parameter_pk>\d+)_exclude/$',
        ParameterManagerView, 'parameter_exclude', {'method': 'exclude'}),
    (r'^task/(?P<task_pk>\d+)/parameter/add/$', 'parameter_add',),
)


urlpatterns = named_urls('',
    (r'^accounts/', include('exmo2010.custom_registration.backends.custom.urls')),

    (r'^monitoring/', include(monitoring_patterns)),

    (r'^score/', include(scores_patterns)),
    (r'^scores/(?P<task_pk>\d+)/(?P<print_report_type>print|printfull)?$', 'scores.views.score_list_by_task'),

    (r'^tasks/', include(tasks_patterns)),
    (r'^task/(?P<task_pk>\d+)/history/$', 'tasks.views.task_history'),

    # Отчеты
    (r'^reports/comments/$', 'custom_comments.views.comment_list'),
    (r'^reports/clarifications/$', 'clarifications.views.clarification_list'),
    (r'^reports/claims/$', 'claims.views.claim_list'),
    (r'^reports/monitoring/$', 'monitorings.views.monitoring_report'),
    (r'^reports/monitoring/(?P<report_type>inprogress|finished)/$',
        'monitorings.views.monitoring_report', 'monitoring_report_type'),
    (r'^reports/monitoring/(?P<report_type>inprogress|finished)/(?P<monitoring_pk>\d+)/$',
        'monitorings.views.monitoring_report', 'monitoring_report_finished'),

    (r'^certificate_order/$', CertificateOrderView.as_view([CertificateOrderForm, CertificateOrderForm]),
     'certificate_order'),
    (r'^claim/delete/$', 'claims.views.claim_delete'),
    (r'^toggle_comment/$', 'scores.views.toggle_comment'),
    (r'^ratings/$', 'monitorings.views.ratings'),
    (r'^help/$', HelpView, 'help'),
    (r'^about/$', AboutView, 'about'),

    (r'^opendata/$', OpenDataView, 'opendata'),
    (r'^feedback/$', 'exmo2010.views.feedback'),
    # AJAX-вьюха для получения списка критериев, отключенных у параметра
    (r'^get_pc/$', 'parameters.views.get_pc'),
    # AJAX-вьюха для получения кода div'а для одного вопроса (c полями).
    (r'^get_qq/$', 'questionnaire.views.get_qq'),
    # AJAX-вьюха для получения кода div'а для одного вопроса (без полей).
    (r'^get_qqt/$', 'questionnaire.views.get_qqt'),
)


def crumbs_tree(is_expert=False):
    common_tree = {
        'about': _('About'),
        'help':  _('Help'),
        'feedback': _('Feedback'),
        'opendata': _('Open data'),
        'settings': _('Settings'),
        'monitoring_report':          _('Statistics'),
        'monitoring_report_type':     _('Statistics'),
        'monitoring_report_finished': _('Statistics'),

        'auth_login': _('Login'),
        'auth_password_reset':         _('Password reset (step 1 from 3)'),
        'auth_password_reset_done':    _('Password reset (step 2 from 3)'),
        'auth_password_reset_confirm': _('Password reset (step 3 from 3)'),
        'registration_register':   _('Registration (step 1 of 2)'),
        'registration_complete':   _('Registration (step 2 of 2)'),
        'registration_disallowed': _('Registration disallowed'),
        'registration_activation_complete': _('Activation complete'),
    }

    expert_tree = {
        'comment_list': _('Comments'),
        'claim_list':   _('Claims'),
        'clarification_list': _('Clarifications'),

        'ratings': (_('Ratings'), {
            'monitoring_rating': _('Rating')
        }),

        'monitoring_list': (_('Monitoring cycles'), {
            'monitoring_add':    _('Add monitoring cycle'),
            'monitoring_delete': _('Delete monitoring cycle'),
            'monitoring_update': _('Edit monitoring cycle'),

            'add_questionnaire': _('Add questionnaire'),

            'claim_report':         _('Monitoring cycle'),
            'clarification_report': _('Monitoring cycle'),

            'monitoring_by_experts':       _('Monitoring cycle'),
            'monitoring_parameter_filter': _('Monitoring cycle'),

            'monitoring_comment_report':         _('Monitoring cycle'),
            'monitoring_parameter_found_report': _('Monitoring cycle'),

            'monitoring_parameter_import':    _('Import parameter'),
            'monitoring_organization_import': _('Import organization'),

            'organization_list': _('Monitoring cycle'),

            'task_mass_assign_tasks': _('Monitoring cycle'),

            'tasks_by_monitoring': (_('Monitoring cycle'), {
                'task_add':     _('Add task'),
                'org_task_add': _('Add task'),  # TODO: replace with task_add

                'tasks_by_monitoring_and_organization': _('Organization'),  # TODO: replace with tasks_by_monitoring

                'organization_update':    _('Edit organization'),
                'organization_delete':    _('Delte organization'),

                'score_list_by_task': (_('Organization'), {
                    'clarification_create': _('Create clarification'),
                    'claim_create':         _('Create claim'),
                    # Task
                    'task_update':  _('Edit task'),
                    'task_delete':  _('Delte task'),
                    'task_import':  _('Import task'),
                    'task_history': _('Organization'),
                    # Score
                    'score_add':    _('Parameter'),
                    'score_view':   _('Parameter'),
                    'score_edit':   _('Parameter'),
                    'score_delete': _('Delete score'),
                    # Parameter
                    'parameter_add':    _('Add parameter'),
                    'parameter_update': _('Edit parameter'),
                    'parameter_delete': _('Delte parameter'),
                })
            })
        })
    }

    nonexpert_tree = {
        'ratings': (_('Ratings'), {
            'monitoring_rating': (_('Rating'), {
                'score_list_by_task': (_('Organization'), {
                    'score_view': _('Parameter'),
                })
            }),
        }),
        'monitoring_list': _('Monitoring cycles'),
        'certificate_order': _('Openness certificate'),
    }

    common_tree.update(expert_tree if is_expert else nonexpert_tree)

    return {'index': ('', common_tree)}
