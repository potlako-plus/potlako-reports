from concurrent.futures import ThreadPoolExecutor
import imp
from pyexpat import model
from threading import Thread

from django.apps import apps as django_apps
from django.db.models import QuerySet, Model
from django.views.generic.list import ListView

from dateutil.relativedelta import relativedelta
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from edc_sync.models import IncomingTransaction

# TODO: use conversions
from potlako_subject.models import SubjectConsent


class SyncReportView(NavbarViewMixin, EdcBaseViewMixin, ListView):
    template_name = 'sync_report.html'
    navbar_selected_item = 'Sync Report'
    navbar_name = 'potlako_reports'
    model = IncomingTransaction
    context_object_name = 'incoming_transactions'
    paginate_by = 20
    ordering = ['-created']

    def statistics(self):
        pass

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        errors = queryset.filter(is_error=True).count()
        consumed = queryset.filter(is_consumed=True).count()
        updates = queryset.filter(action='U').count()
        deletes = queryset.filter(action='D').count()
        inserts = queryset.filter(action='I').count()

        context.update(
            errors=errors,
            consumed = consumed,
            updates = updates,
            deletes = deletes,
            inserts = inserts)
        return context