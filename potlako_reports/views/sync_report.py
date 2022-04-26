from django.apps import apps as django_apps
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin



class SyncReportView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'sync_report.html'
    navbar_selected_item = 'Sync Report'
    navbar_name = 'potlako_reports'

    subject_consent_model = 'potlako_subject.subjectconsent'

    packages = ('edc_appointment', 'potlako_subject'),

    

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)


    def calculate_statistics(self):

        statistics = dict()

        host_machines = set(self.subject_consent_cls.objects.values_list(
            'hostname_created', flat=True))

        models = {}

        for package in self.packages:
            temp = django_apps.all_models.get(package, None)

            if temp:
                models.update(temp)

        for host_machine in host_machines:

            host_machine_statistics = dict()

            for model_cls in models.values():

                if 'historical' in model_cls._meta.verbose_name:
                    continue
                try:
                    count = model_cls.objects.filter(
                        hostname_created=host_machine).count()
                    host_machine_statistics.update(
                        {model_cls._meta.verbose_name: count})
                except:
                    continue

            statistics.update({host_machine: host_machine_statistics})

        return statistics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        statistics = self.calculate_statistics()

        context.update(statistics=statistics)
        return context
    




    