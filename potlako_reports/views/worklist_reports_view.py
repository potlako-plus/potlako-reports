
from django.apps import apps as django_apps
from django.views.generic.base import TemplateView
from pip._internal import self_outdated_check

from dateutil.relativedelta import relativedelta
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class WorkListView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'worklist_reports.html'
    navbar_selected_item = 'Worklist Reports'
    navbar_name = 'potlako_reports'

    clinician_call_enrollment_model = 'potlako_subject.cliniciancallenrollment'
    worklist_model = 'potlako_follow.worklist'
    investigation_worklist_model = 'potlako_follow.investigationfuworklist'

    @property
    def clinician_call_enrollment_cls(self):
        return django_apps.get_model(self.clinician_call_enrollment_model)

    @property
    def worklist_cls(self):
        return django_apps.get_model(self.worklist_model)

    @property
    def investigation_worklist_cls(self):
        return django_apps.get_model(self.investigation_worklist_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        worklist_count = self.worklist_cls.objects.all().count()
        investigation_worklist = self.investigation_worklist_cls.objects.all().count()

        enhanced_care = ['otse_clinic', 'mmankgodi_clinic',
                         'letlhakeng_clinic',
                         'mathangwane clinic', 'ramokgonami_clinic',
                         'sefophe_clinic',
                         'mmadinare_primary_hospital', 'tati_siding_clinic',
                         'bokaa_clinic', 'masunga_primary_hospital',
                         'masunga_clinic',
                         'mathangwane_clinic', 'manga_clinic']
        intervention = ['mmathethe_clinic', 'molapowabojang_clinic',
                        'lentsweletau_clinic', 'oodi_clinic',
                        'metsimotlhabe_clinic',
                        'shoshong_clinic', 'lerala_clinic',
                        'maunatlala_clinic',
                        'nata_clinic', 'mandunyane_clinic',
                        'sheleketla_clinic']

        intervention_enrolled = self.clinician_call_enrollment_cls.objects.\
            filter(facility__in=intervention).count()
        enhanced_care_enrolled = self.clinician_call_enrollment_cls.objects. \
            filter(facility__in=enhanced_care).count()

        context.update(
            worklist_count=worklist_count,
            investigation_worklist=investigation_worklist,
            intervention_enrolled=intervention_enrolled,
            enhanced_care_enrolled=enhanced_care_enrolled
        )

        return context
