
from django.apps import apps as django_apps
from django.views.generic.base import TemplateView

from dateutil.relativedelta import relativedelta
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class WorkListView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'worklist_reports.html'
    navbar_selected_item = 'Worklist Reports'
    navbar_name = 'potlako_reports'

    cancer_dx_tx_endpoint = 'potlako_subject.cancerdxandtxendpoint'
    cancer_dx_tx = 'potlako_subject.cancerdxandtx'

    @property
    def cancer_dx_tx_endpoint_cls(self):
        return django_apps.get_model(self.cancer_dx_tx_endpoint)

    @property
    def cancer_dx_tx_cls(self):
        return django_apps.get_model(self.cancer_dx_tx)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
