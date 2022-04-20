
from django.apps import apps as django_apps
from django.views.generic.base import TemplateView
from pip._internal import self_outdated_check

from dateutil.relativedelta import relativedelta
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class SyncReportView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'sync_report.html'
    navbar_selected_item = 'Sync Report'
    navbar_name = 'potlako_reports'
