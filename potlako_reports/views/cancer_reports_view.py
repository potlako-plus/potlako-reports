from datetime import date

from django.apps import apps as django_apps
from django.views.generic.base import TemplateView

from dateutil.relativedelta import relativedelta
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class CancerView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'cancer_reports.html'
    navbar_selected_item = 'Cancer Reports'
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
        six_months = date.today() + relativedelta(months=-6)
        twelve_months = date.today() + relativedelta(months=-12)

        cancer_dx_tx_endpoint_subjects = self.cancer_dx_tx_endpoint_cls.objects.all()
        final_cancer_diagnosis_6 = self.cancer_dx_tx_endpoint_cls.objects.filter(diagnosis_date__lte=six_months).count()
        final_cancer_diagnosis_12 = self.cancer_dx_tx_endpoint_cls.objects.filter(diagnosis_date__lte=twelve_months).count()
        confirmed_cancer_diagnosis_6 = self.cancer_dx_tx_cls.objects.filter(diagnosis_date__lte=six_months).count()
        confirmed_cancer_diagnosis_12 = self.cancer_dx_tx_cls.objects.filter(diagnosis_date__lte=twelve_months).count()

        context.update(
            cancer_subjects=cancer_dx_tx_endpoint_subjects,
            final_cancer_diagnosis_6=final_cancer_diagnosis_6,
            final_cancer_diagnosis_12=final_cancer_diagnosis_12,
            confirmed_cancer_diagnosis_6=confirmed_cancer_diagnosis_6,
            confirmed_cancer_diagnosis_12=confirmed_cancer_diagnosis_12
        )

        return context
