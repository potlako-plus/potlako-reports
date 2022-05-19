from django.apps import apps as django_apps
from django.conf import settings
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
    
    non_crf_models = [
         'edc_appointment.appointment',
          'potlako_prn.deathreport',
          'potlako_prn.subjectoffstudy',
          'potlako_subject.subjectconsent',
          'potlako_subject.subjectlocator',
          'potlako_subject.subjectscreening',
          'potlako_subject.subjectvisit',
          'potlako_subject.verbalconsent',
          
    ]
    
    # crf models of interest
    
    crf_models = [
        'potlako_subject.patientcallinitial',
        'potlako_subject.symptomandcareseekingassessment',
        'potlako_subject.transport',
        'potlako_subject.investigationsordered',
        'potlako_subject.investigationsresulted',
        'potlako_subject.medicaldiagnosis',
        'potlako_subject.patientcallfollowup',
        'potlako_subject.missedvisit',
        'potlako_subject.homevisit',
        'potlako_subject.cancerdxandtx'
    ]
    
    
    
    
    
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
        
        for model_name in self.non_crf_models:
            model_class_statistics = []
            model_class = django_apps.get_model(model_name)
            
            verbose_name = model_class._meta.verbose_name.title()
            
            model_class_statistics.append(verbose_name)
                
            for host_machine in self.host_machines:
                counter = model_class.objects.filter(hostname_created__iexact=host_machine).count()
                model_class_statistics.append(counter)
                
            statistics.append(model_class_statistics)
        
            
        return statistics
    
    @property
    def non_crf_statistics_totals(self):
        statistics = []
        for stat in self.non_crf_statistics:
            statistics.append([stat[0], sum(stat[1:])])
        # breakpoint()
        return statistics
    
    @property
    def hostmachine_non_crf_statistics(self):
        statistics = []
        
        for index, host in enumerate(self.host_formatted_names):
            temp = [host, ]
            total = 0
            for crf_stat in self.non_crf_statistics:
                total += crf_stat[index+1]
            temp.append(total)
            statistics.append(temp)
        return statistics
    
    @property
    def hostmachine_crf_statistics(self):
        statistics = []
        
        for index, host in enumerate(self.host_formatted_names):
            temp = [host, ]
            total = 0
            for crf_stat in self.crf_statistics:
                total += crf_stat[index+1]
            temp.append(total)
            statistics.append(temp)
        return statistics
    
    
    
    @property
    def crf_statistics(self):
        statistics = []

        
        for model_class_name in self.crf_models:
            
            model_class = django_apps.get_model(model_class_name)
            
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
            host_machines = self.host_formatted_names,
            crf_statistics = self.crf_statistics,
            non_crf_statistics_totals = self.non_crf_statistics_totals,
            hostmachine_non_crf_statistics = self.hostmachine_non_crf_statistics,
            hostmachine_crf_statistics = self.hostmachine_crf_statistics,
            device_id = settings.DEVICE_ID
        )
        
        return context


    
    




    