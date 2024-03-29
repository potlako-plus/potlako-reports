from django.apps import apps as django_apps
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from edc_constants.constants import MALE, FEMALE


class HomeView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'home.html'
    navbar_selected_item = 'Enrollments Reports'
    navbar_name = 'potlako_reports'

    subject_screening_model = 'potlako_subject.subjectscreening'
    subject_consent_model = 'potlako_subject.subjectconsent'
    cancer_dx_tx = 'potlako_subject.cancerdxandtxendpoint'
    cancer_dx_tx_endpoint = 'potlako_subject.cancerdxandtxendpoint'
    cancer_dx_tx = 'potlako_subject.cancerdxandtx'
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

    @property
    def cancer_dx_tx_endpoint_cls(self):
        return django_apps.get_model(self.cancer_dx_tx_endpoint)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def cancer_dx_tx_cls(self):
        return django_apps.get_model(self.cancer_dx_tx)

    @property
    def enrollment_timeseries_statistics(self):
        """Time series data from the first consent

        Returns:
            list: Data calculate from 2020, up-to-dakte
        """
        current_year = datetime.now()
        months = []
        initial_date = self.subject_consent_cls.objects.latest(
            '-report_datetime').report_datetime.date()

        while True:

            if initial_date.year == current_year.year and initial_date.month == current_year.month:
                break

            months.append(initial_date)
            initial_date += relativedelta(months=1)

        enrollment_data = list()

        for date in months:
            consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month).count()

            date_year = date.year
            date_month = date.month

            enrollment_data.append(
                (f"{date_year}-{date_month}",  consents_count),
            )

        return enrollment_data

    @property
    def enrollment_timeseries_statistics_by_gender(self):
        """Time series data from the first consent

        Returns:
            list: Data calculate from 2020, up-to-date
        """
        current_year = datetime.now()
        months = []
        initial_date = self.subject_consent_cls.objects.latest(
            '-report_datetime').report_datetime.date()

        while True:

            if initial_date.year == current_year.year and initial_date.month == current_year.month:
                break

            months.append(initial_date)
            initial_date += relativedelta(months=1)

        enrollment_dates = list()
        gender_statistics = list()

        for date in months:
            female_consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month, gender=FEMALE).count()

            male_consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month, gender=MALE).count()

            date_year = date.year
            date_month = date.month

            enrollment_dates.append(
                f"{date_year}-{date_month}"
            )
            gender_statistics.append(
                (female_consents_count, male_consents_count)
            )

        return (enrollment_dates, gender_statistics)

    @property
    def get_gender_count(self):
        female_ids = self.subject_consent_cls.objects.filter(
            gender=FEMALE).distinct().count()
        male_ids = self.subject_consent_cls.objects.filter(
            gender=MALE).distinct().count()

        gender_statistics = [female_ids, male_ids]
        return gender_statistics

    gender_labels = ['Females', 'Males']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screened_subjects = self.subject_screening_cls.objects.all().count()
        consented_subjects = self.subject_consent_cls.objects.all().count()
        enrolled_subjects = self.subject_consent_cls.objects.all().count()
        not_enrolled_subjects = self.subject_screening_cls.objects.filter(
            is_eligible=False).count()

        six_months = date.today() + relativedelta(months=-6)
        twelve_months = date.today() + relativedelta(months=-12)

        final_cancer_diagnosis_6 = self.cancer_dx_tx_endpoint_cls.objects.filter(
            diagnosis_date__lte=six_months).count()
        final_cancer_diagnosis_12 = self.cancer_dx_tx_endpoint_cls.objects.filter(
            diagnosis_date__lte=twelve_months).count()
        confirmed_cancer_diagnosis_6 = self.cancer_dx_tx_endpoint_cls.objects.filter(
            diagnosis_date__lte=six_months).count()
        confirmed_cancer_diagnosis_12 = self.cancer_dx_tx_endpoint_cls.objects.filter(
            diagnosis_date__lte=twelve_months).count()
        enrollments = [
            ['Screening', screened_subjects],
            ['Consented', consented_subjects],
            ['Not Enrolled', not_enrolled_subjects],
            ['Enrolled', enrolled_subjects],
        ]

        cancers = [
            ['Confirmed Cancer Diagnosis At 6 months', confirmed_cancer_diagnosis_6],
            ['Confirmed Cancer Diagnosis At 12 months',
                confirmed_cancer_diagnosis_12],
            ['Final Cancer Diagnosis At 6 months', final_cancer_diagnosis_6],
            ['Final Cancer Diagnosis At 12 months', final_cancer_diagnosis_12]
        ]

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

        worklists = [
            ['Intervention Arm', intervention_enrolled],
            ['Standard Care Arm', enhanced_care_enrolled],
            ['Appointment Worklist', worklist_count],
            ['Investigations Worklist', investigation_worklist]]

        context.update(
            screened_subjects=screened_subjects,
            consented_subjects=consented_subjects,
            not_enrolled_subjects=not_enrolled_subjects,
            enrolled_subjects=enrolled_subjects,

            final_cancer_diagnosis_6=final_cancer_diagnosis_6,
            final_cancer_diagnosis_12=final_cancer_diagnosis_12,
            confirmed_cancer_diagnosis_6=confirmed_cancer_diagnosis_6,
            confirmed_cancer_diagnosis_12=confirmed_cancer_diagnosis_12,

            enrollments=enrollments,
            cancers=cancers,
            worklists=worklists,

            worklist_count=worklist_count,
            investigation_worklist=investigation_worklist,
            intervention_enrolled=intervention_enrolled,
            enhanced_care_enrolled=enhanced_care_enrolled,
            enrollment_timeseries_statistics=self.enrollment_timeseries_statistics,
            enrollment_timeseries_statistics_by_gender=self.enrollment_timeseries_statistics_by_gender,
            gender_labels=self.gender_labels,
            gender_stats=self.get_gender_count,


        )

        return context
