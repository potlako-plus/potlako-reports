from itertools import count
import statistics
from django.apps import apps as django_apps
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin




class SyncReportView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'sync_report.html'
    navbar_selected_item = 'Sync Report'
    navbar_name = 'potlako_reports'

    subject_consent_model = 'potlako_subject.subjectconsent'
    appointment_model = 'edc_appointment.appointment'

    modules = ('edc_appointment', 'potlako_subject'),

    

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def appointment_cls(self):
        return django_apps.get_model(self.appointment_model)

    @property
    def host_machines(self):
        host_machines = set(self.subject_consent_cls.objects.values_list(
            'hostname_created', flat=True))
        return host_machines

    @property
    def host_machines_formatted_names(self):
        host_machines = []
        for name in self.host_machines:
            if 'potlako_plus' in name:
                host_machines.append(name[-2:])
        return host_machines

    @property
    def crf_models(self):

        models = list()

        for module in self.modules:
            for model in django_apps.get_models():
                if not model.__module__.startswith(module) \
                        or model._meta.verbose_name.startswith('historical'):
                    continue
                models.append(model)

        return models

    @property
    def crf_verbose_names(self):
        verbose_names = []

        for model_cls in self.crf_models:
            verbose_names.append(model_cls._meta.verbose_name.title())
        return verbose_names


    @property
    def appointment_statistics(self):

        statistics = []

        for host_machine in self.host_machines:

            appointments = self.appointment_cls.objects.filter(
                hostname_created=host_machine)

            statistics.append(
                {
                    'host_machine': host_machine,
                    'appointments': appointments.count(),
                    'last_modified': appointments.latest('modified').modified.date().isoformat()    
                }
            )
        
        return statistics

    @property
    def crf_statistics(self):
        statistics = []
        
        for crf in self.crf_models:
            data = [crf._meta.verbose_name,]
            for host_machine in self.host_machines:
                crf_counter = crf.objects.filter(hostname_created=host_machine).count()
                data.append(crf_counter)
            statistics.append(data)
                

                
        return statistics

        
            


    @property
    def general_statistics(self):

        statistics = dict()

        models = {}

        for package in self.modules:
            temp = django_apps.all_models.get(package, None)

            if temp:
                models.update(temp)

        for host_machine in self.host_machines:

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

        context.update(
            crf_verbose_names=self.crf_verbose_names,
            crf_statistics = self.crf_statistics,
            host_machines = self.host_machines,
            host_machines_formatted_names=self.host_machines_formatted_names,
            general_statistics=self.general_statistics,
            appointment_statistics = self.appointment_statistics,
            crf_models=self.crf_models)
        return context
    




    