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
import csv
import re
import string

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, QueryDict
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
import reversion

from accounts.forms import SettingsInvCodeForm
from core.utils import UnicodeReader, UnicodeWriter
from exmo2010.models import Monitoring, Organization, Parameter, Score, Task, TaskHistory
from core.helpers import table
from tasks.forms import TaskForm


def task_export(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if not request.user.has_perm('exmo2010.view_task', task):
        return HttpResponseForbidden(_('Forbidden'))
    parameters = Parameter.objects.filter(monitoring=task.organization.monitoring).exclude(exclude=task.organization)
    scores = Score.objects.filter(task=task_pk, revision=Score.REVISION_DEFAULT)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=task-%s.csv' % task_pk
    response.encoding = 'UTF-16'
    writer = UnicodeWriter(response)
    writer.writerow([
        '#Code',
        'Name',
        'Found',
        'Complete',
        'CompleteComment',
        'Topical',
        'TopicalComment',
        'Accessible',
        'AccessibleComment',
        'Hypertext',
        'HypertextComment',
        'Document',
        'DocumentComment',
        'Image',
        'ImageComment',
        'Comment'
    ])
    category = None
    subcategory = None
    for p in parameters:
        out = (
            p.code,
            p.name,
        )
        try:
            s = scores.get(parameter=p)
        except:
            out += (
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                ''
            )
        else:
            out += (s.found,)
            if p.complete:
                out += (
                    s.complete,
                    s.completeComment
                )
            else:
                out += ('', '')
            if p.topical:
                out += (
                    s.topical,
                    s.topicalComment
                )
            else:
                out += ('', '')
            if p.accessible:
                out += (
                    s.accessible,
                    s.accessibleComment
                )
            else:
                out += ('', '')
            if p.hypertext:
                out += (
                    s.hypertext,
                    s.hypertextComment
                )
            else:
                out += ('', '')
            if p.document:
                out += (
                    s.document,
                    s.documentComment
                )
            else:
                out += ('', '')
            if p.image:
                out += (
                    s.image,
                    s.imageComment
                )
            else:
                out += ('','')
            out += (s.comment,)
        writer.writerow(out)
    return response


@reversion.create_revision()
@login_required
def task_import(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if not request.user.has_perm('exmo2010.fill_task', task):
        return HttpResponseForbidden(_('Forbidden'))
    if not request.FILES.has_key('taskfile'):
        return HttpResponseRedirect(reverse('exmo2010:score_list_by_task', args=[task_pk]))
    reader = UnicodeReader(request.FILES['taskfile'])
    errLog = []
    rowOKCount = 0
    rowALLCount = 0
    try:
        for row in reader:
            rowALLCount += 1
            if row[0].startswith('#'):
                errLog.append(_("row %d. Starts with '#'. Skipped") % reader.line_num)
                continue
            try:
                code = re.match('^(\d+)$', row[0])
                if not code:
                    errLog.append(_("row %(row)d (csv). Not a code: %(raw)s") % {'row': reader.line_num, 'raw': row[0]})
                    continue
                if not any(row[2:16]):
                    errLog.append(_("row %(row)d (csv). Empty score: %(raw)s") % {'row': reader.line_num, 'raw': row[0]})
                    continue
                parameter = Parameter.objects.get(code=code.group(1), monitoring=task.organization.monitoring)
                try:
                    score = Score.objects.get(task=task, parameter=parameter)
                except Score.DoesNotExist:
                    score = Score()
                score.task = task
                score.parameter = parameter
                for i, key in enumerate(['found', 'complete', 'completeComment', 'topical', 'topicalComment',
                                         'accessible', 'accessibleComment', 'hypertext', 'hypertextComment',
                                         'document', 'documentComment', 'image', 'imageComment', 'comment']):
                    value = row[i+2]
                    setattr(score, key, value if value else None)
                score.full_clean()
                score.save()
            except ValidationError, e:
                errLog.append(_("row %(row)d (validation). %(raw)s") % {
                    'row': reader.line_num,
                    'raw': '; '.join(['%s: %s' % (i[0], ', '.join(i[1])) for i in e.message_dict.items()])})
            except Parameter.DoesNotExist:
                errLog.append(_("row %(row)d. %(raw)s") % {
                    'row': reader.line_num,
                    'raw': _('Parameter matching query does not exist')})
            except Exception, e:
                errLog.append(_("row %(row)d. %(raw)s") % {
                    'row': reader.line_num,
                    'raw': filter(lambda x: x in string.printable, e.__str__())})
            else:
                rowOKCount += 1
    except csv.Error, e:
        errLog.append(_("row %(row)d (csv). %(raw)s") % {'row': reader.line_num, 'raw': e})
    except UnicodeError:
        errLog.append(_("File, you are loading is not valid CSV."))
    except Exception, e:
        errLog.append(_("Import error: %s." % e))
    title = _('Import CSV for task %s') % task

    return TemplateResponse(request, 'task_import_log.html', {
        'task': task,
        'file': request.FILES['taskfile'],
        'errLog': errLog,
        'rowOKCount': rowOKCount,
        'rowALLCount': rowALLCount,
        'title': title,
    })


# TODO: replace with tasks_by_monitoring
def tasks_by_monitoring_and_organization(request, monitoring_pk, org_pk):
    """
    We have 3 generic group: experts, customers, organizations.
    Superusers: all tasks
    Experts: only own tasks
    Customers: all approved tasks
    organizations: all approved tasks of organizations that belongs to user
    Also for every ogranization we can have group.

    """
    monitoring = get_object_or_404(Monitoring, pk = monitoring_pk)
    organization = get_object_or_404(Organization, pk = org_pk)
    user = request.user
    profile = None
    if user.is_active: profile = user.profile
    if not user.has_perm('exmo2010.view_monitoring', monitoring):
        return HttpResponseForbidden(_('Forbidden'))
    title = _('Task list for %s') % organization.name
    queryset = Task.objects.filter(organization = organization)
    # Or, filtered by user
    if user.has_perm('exmo2010.admin_monitoring', monitoring):
      headers = (
                (_('organization'), 'organization__name', 'organization__name', None, None),
                (_('expert'), 'user__username', 'user__username', None, None),
                (_('status'), 'status', 'status', int, Task.TASK_STATUS),
                (_('complete, %'), None, None, None, None),
                (_('openness, %'), None, None, None, None),
      )
    elif profile and profile.is_expert:
    # Or, without Expert
      headers = (
                (_('organization'), 'organization__name', 'organization__name', None, None),
                (_('status'), 'status', 'status', int, Task.TASK_STATUS),
                (_('complete, %'), None, None, None, None),
                (_('openness, %'), None, None, None, None)
      )
    else:
      queryset = Task.approved_tasks.all()
      queryset = queryset.filter(organization = organization)
      headers = (
                (_('organization'), 'organization__name', 'organization__name', None, None),
                (_('openness, %'), None, None, None, None)
              )
    task_list = []
    for task in queryset:
        if user.has_perm('exmo2010.view_task', task): task_list.append(task.pk)
    queryset = Task.objects.filter(pk__in = task_list)

    return table(request, headers, queryset=queryset, paginate_by=15,
                 extra_context={
                     'monitoring': monitoring,
                     'organization': organization,
                     'title': title,
                 },
                 template_name="task_list.html",)


@reversion.create_revision()
@login_required
def task_add(request, monitoring_pk, org_pk=None):
    monitoring = get_object_or_404(Monitoring, pk = monitoring_pk)
    if org_pk:
        organization = get_object_or_404(Organization, pk = org_pk)
        redirect = '%s?%s' % (reverse('exmo2010:tasks_by_monitoring_and_organization', args=[monitoring.pk, organization.pk]), request.GET.urlencode())
        title = _('Add new task for %s') % organization.name
    else:
        organization = None
        redirect = '%s?%s' % (reverse('exmo2010:tasks_by_monitoring', args=[monitoring.pk]), request.GET.urlencode())
        title = _('Add new task for %s') % monitoring

    redirect = redirect.replace("%","%%")
    if request.user.has_perm('exmo2010.admin_monitoring', monitoring):
        if request.method == 'GET':
            form = TaskForm(initial={'organization': organization}, monitoring=monitoring)
        elif request.method == 'POST':
            form = TaskForm(request.POST, monitoring=monitoring)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(redirect)

        return TemplateResponse(request, 'exmo2010/task_form.html', {
            'monitoring': monitoring,
            'organization': organization,
            'title': title,
            'form': form
        })
    else:
        return HttpResponseForbidden(_('Forbidden'))


class TaskManagerView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = Task
    context_object_name = "object"
    form_class = TaskForm
    template_name = "task_status.html"
    extra_context = {}
    pk_url_kwarg = 'task_pk'

    def get_redirect(self, request, monitoring, organization, org_pk=None):
        organization_from_get = request.GET.get('organization', '')
        if org_pk or organization_from_get:
            q = request.GET.copy()
            if organization_from_get:
                q.pop('organization')
            redirect = '%s?%s' % (reverse('exmo2010:tasks_by_monitoring_and_organization',
                                  args=[monitoring.pk, organization.pk]), q.urlencode())
        else:
            redirect = '%s?%s' % (reverse('exmo2010:tasks_by_monitoring',
                                          args=[monitoring.pk]), request.GET.urlencode())
        redirect = redirect.replace("%", "%%")
        return redirect

    def get_context_data(self, **kwargs):
        context = super(TaskManagerView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        organization = self.object.organization
        monitoring = organization.monitoring
        org_pk = self.kwargs.get('org_pk')
        self.success_url = self.get_redirect(request, monitoring, organization, org_pk)

        valid_methods = ['delete', 'approve', 'close',
                         'open', 'update', 'get', ]
        if self.kwargs["method"] not in valid_methods:
            HttpResponseForbidden(_('Forbidden'))

        if self.kwargs["method"] == 'delete':
            title = _('Delete task %s') % self.object
            if not request.user.has_perm('exmo2010.admin_monitoring', monitoring):
                return HttpResponseForbidden(_('Forbidden'))
            else:
                self.template_name = "exmo2010/task_confirm_delete.html"
                self.extra_context = {
                    'monitoring': monitoring,
                    'organization': organization,
                    'title': title,
                    'deleted_objects': Score.objects.filter(task=self.object)
                }

        if self.kwargs["method"] == 'close':
            title = _('Close task %s') % self.object
            if not request.user.has_perm('exmo2010.close_task', self.object):
                return HttpResponseForbidden(_('Forbidden'))
            else:
                if self.object.open:
                    try:
                        reversion.set_comment(_('Task ready'))
                        self.object.ready = True
                    except ValidationError, e:
                        return HttpResponse('%s' % e.message_dict.get('__all__')[0])
                else:
                    return HttpResponse(_('Already closed'))

        if self.kwargs["method"] == 'approve':
            title = _('Approve task for %s') % self.object
            if not request.user.has_perm('exmo2010.approve_task', self.object):
                return HttpResponseForbidden(_('Forbidden'))
            else:
                if not self.object.approved:
                    try:
                        reversion.set_comment(_('Task approved'))
                        self.object.approved = True
                    except ValidationError, e:
                        return HttpResponse('%s' % e.message_dict.get('__all__')[0])
                else:
                    return HttpResponse(_('Already approved'))
        if self.kwargs["method"] == 'open':
            title = _('Open task %s') % self.object
            if not request.user.has_perm('exmo2010.open_task', self.object):
                return HttpResponseForbidden(_('Forbidden'))
            else:
                if not self.object.open:
                    try:
                        reversion.set_comment(_('Task openned'))
                        self.object.open = True
                    except ValidationError, e:
                        return HttpResponse('%s' % e.message_dict.get('__all__')[0])
                else:
                    return HttpResponse(_('Already open'))
        if self.kwargs["method"] == 'update':
            title = _('Edit task %s') % self.object
            self.template_name = "exmo2010/task_form.html"
            if not request.user.has_perm('exmo2010.admin_monitoring', monitoring):
                return HttpResponseForbidden(_('Forbidden'))
            else:
                reversion.set_comment(_('Task updated'))
                self.extra_context = {
                    'monitoring': monitoring,
                    'organization': organization,
                    'title': title,
                }

        self.extra_context['title'] = title
        return super(TaskManagerView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        organization = self.object.organization
        monitoring = organization.monitoring
        org_pk = self.kwargs.get('org_pk')
        self.success_url = self.get_redirect(request, monitoring, organization, org_pk)
        if self.kwargs["method"] == 'delete':
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        elif self.kwargs["method"] == 'update':
            return super(TaskManagerView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskManagerView, self).dispatch(*args, **kwargs)


def task_history(request, task_pk):
    task = Task.objects.get(pk=task_pk)
    history = TaskHistory.objects.filter(task=task_pk)

    return TemplateResponse(request, 'task_history.html', {
        'task': task,
        'history': history,
        'title': task.organization.name,
    })


def tasks_by_monitoring(request, monitoring_pk):
    monitoring = get_object_or_404(Monitoring, pk=monitoring_pk)
    profile = None
    if request.user.is_active:
        profile = request.user.profile
    if not request.user.has_perm('exmo2010.view_monitoring', monitoring):
        return HttpResponseForbidden(_('Forbidden'))
    title = _('Task list for %(monitoring)s') % {'monitoring': monitoring}
    task_list = []
    queryset = Task.objects.filter(organization__monitoring=monitoring).\
    select_related()
    for task in queryset:
        if request.user.has_perm('exmo2010.view_task', task):
            task_list.append(task.pk)
    if not task_list and not \
    request.user.has_perm('exmo2010.admin_monitoring', monitoring):
        return HttpResponseForbidden(_('Forbidden'))
    queryset = Task.objects.filter(pk__in=task_list).extra(
        select={'complete_sql': Task.complete_sql_extra()}).select_related()
    if request.user.has_perm('exmo2010.admin_monitoring', monitoring):
        users = User.objects.filter(task__organization__monitoring = monitoring).distinct()
        UserChoice = [(u.username, u.profile.legal_name) for u in users]
        headers = (
            (_('organization'), 'organization__name', 'organization__name',
             None, None),
            (_('expert'), 'user__username', 'user__username', None, UserChoice),
            (_('status'), 'status', 'status', int, Task.TASK_STATUS),
            (_('complete, %'), None, None, None, None),
            )
    elif profile and profile.is_expertB and not profile.is_expertA:
        filter1 = request.GET.get('filter1')
        if filter1:
            try:
                int(filter1)
            except ValueError:
                q = QueryDict('')
                request.GET = q
        headers = (
            (_('organization'), 'organization__name', 'organization__name',
             None, None),
             (_('status'), 'status', 'status', int, Task.TASK_STATUS),
             (_('complete, %'), None, None, None, None),
            )
    elif profile and profile.is_expert:
        headers = (
            (_('organization'), 'organization__name', 'organization__name',
             None, None),
             (_('status'), 'status', 'status', int, Task.TASK_STATUS),
             (_('complete, %'), None, None, None, None),
            )
    else:
        headers = (
            (_('organization'), 'organization__name', 'organization__name',
             None, None),
            )

    return table(
        request,
        headers,
        queryset = queryset,
        paginate_by = 50,
        extra_context = {
            'monitoring': monitoring,
            'title': title,
            'invcodeform': SettingsInvCodeForm(),
        },
        template_name="task_list.html",
    )


@login_required
def task_mass_assign_tasks(request, monitoring_pk):
    monitoring = get_object_or_404(Monitoring, pk = monitoring_pk)
    if not request.user.has_perm('exmo2010.admin_monitoring', monitoring):
        return HttpResponseForbidden(_('Forbidden'))
    organizations = Organization.objects.filter(monitoring = monitoring)
    title = _('Mass assign tasks')
    groups = []
    for group_name in ['expertsA','expertsB','expertsB_manager']:
        group, created = Group.objects.get_or_create(name = group_name)
        groups.append(group)
    users = User.objects.filter(is_active = True).filter(groups__in = groups)
    log = []
    if request.method == 'POST' and request.POST.has_key('organizations') and request.POST.has_key('users'):
        for organization_id in request.POST.getlist('organizations'):
            for user_id in request.POST.getlist('users'):
                try:
                    user = User.objects.get(pk = (user_id))
                    organization = Organization.objects.get(pk = int(organization_id))
                    task = Task(
                        user = user,
                        organization = organization,
                        status = Task.TASK_OPEN,
                    )
                    task.full_clean()
                    task.save()
                except ValidationError, e:
                    log.append('; '.join(['%s: %s' % (i[0], ', '.join(i[1])) for i in e.message_dict.items()]))
                except Exception, e:
                    log.append(e)
                else:
                    log.append('%s: %s' % (user.userprofile.legal_name, organization.name))

    return TemplateResponse(request, 'mass_assign_tasks.html', {
        'organizations': organizations,
        'users': users,
        'monitoring': monitoring,
        'log': log,
        'title': title,
    })
