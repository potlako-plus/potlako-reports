import enum
from itertools import count
import statistics
from tabnanny import verbose
from textwrap import indent
from xml.sax.handler import property_encoding
from django.apps import apps as django_apps
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin




class SyncReportView(TemplateView, NavbarViewMixin, EdcBaseViewMixin):
    template_name = 'sync_report.html'
    navbar_selected_item = 'Sync Report'
    navbar_name = 'potlako_reports'

    # Non crf models of interest
    appointment_model = 'edc_appointment.appointment'
    death_report_model = 'potlako_prn.deathreport'
    subject_offstudy_model = 'potlako_prn.subjectoffstudy'
    subject_consent_model = 'potlako_subject.subjectconsent'
    subject_locator_model = 'potlako_subject.subjectlocator'
    subject_screening_model = 'potlako_subject.subjectscreening'
    subject_visit_model = 'potlako_subject.subjectvisit'
    verbal_consent_model = 'potlako_subject.verbalconsent'
    
    @property
    def appointment_model_cls(self):
        return django_apps.get_model(self.appointment_model)
    
    
    @property
    def verbal_consent_model_cls(self):
        return django_apps.get_model(self.verbal_consent_model)
    
    @property
    def death_report_model_cls(self):
        return django_apps.get_model(self.death_report_model)
    
    @property
    def subject_offstudy_model_cls(self):
        return django_apps.get_model(self.subject_offstudy_model)

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)
    
    @property
    def subject_locator_model_cls(self):
        return django_apps.get_model(self.subject_locator_model)
    
    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)
    
    @property
    def subject_visit_model_cls(self):
        return django_apps.get_model(self.subject_visit_model)

    @property
    def host_machines(self):
        name_pattern = '[a-z_]+[0-9]+'
        host_names  = set(self.subject_consent_model_cls.objects.filter(
            hostname_created__iregex = name_pattern
        ).values_list('hostname_created', flat=True))

        

        return sorted(host_names)
    
    @property
    def host_formatted_names(self):
        return list(map(lambda name: f'Machine {name[-2:]}', self.host_machines))

    @property
    def non_crf_statistics(self):
        statistics = []
        models_classes = [
            self.subject_visit_model_cls, 
            self.subject_screening_model_cls, 
            self.subject_consent_model_cls,
            self.verbal_consent_model_cls,
            self.appointment_model_cls,
            self.subject_offstudy_model_cls,
            self.death_report_model_cls,
            self.subject_locator_model_cls,
        ]
        
        
        for model_class in models_classes:
            model_class_statistics = []
            
            verbose_name = model_class._meta.verbose_name.title()
            
            model_class_statistics.append(verbose_name)
                
            for host_machine in self.host_machines:
                counter = model_class.objects.filter(hostname_created__iexact=host_machine).count()
                model_class_statistics.append(counter)
                
            statistics.append(model_class_statistics)
        
            
        return statistics
    
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        context.update(
            non_crf_statistics=self.non_crf_statistics,
            host_machines = self.host_formatted_names
        )
        
        return context


    
    




    