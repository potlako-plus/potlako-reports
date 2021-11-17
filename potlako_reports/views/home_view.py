from django.apps import apps as django_apps
from django.views.generic.base import TemplateView
from pip._internal import self_outdated_check

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'home.html'
    navbar_selected_item = 'Enrollments Reports'
    navbar_name = 'potlako_reports'

    subject_screening_model = 'potlako_subject.subjectscreening'
    subject_consent_model = 'potlako_subject.subjectconsent'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screened_subjects = self.subject_screening_cls.objects.all().count()
        consented_subjects = self.subject_consent_cls.objects.all().count()
        enrolled_subjects = self.subject_consent_cls.objects.all().count()
        not_enrolled_subjects = self.subject_screening_cls.objects.filter(is_eligible=False).count()

        context.update(
            screened_subjects=screened_subjects,
            consented_subjects=consented_subjects,
            not_enrolled_subjects=not_enrolled_subjects,
            enrolled_subjects=enrolled_subjects,
        )

        return context
