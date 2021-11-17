from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

potlako_reports = Navbar(name='potlako_reports')

no_url_namespace = True if settings.APP_NAME == 'potlako_reports' else False

potlako_reports.append_item(
    NavbarItem(name='Enrollments Reports',
               label='Enrollments Reports',
               fa_icon='fa-cogs',
               url_name='potlako_reports:home_url'))

potlako_reports.append_item(
    NavbarItem(name='Cancer Reports',
               label='Cancer Reports',
               fa_icon='fa-cogs',
               url_name='potlako_reports:cancer_url'))

potlako_reports.append_item(
    NavbarItem(name='Worklist Reports',
               label='Worklist Reports',
               fa_icon='fa-cogs',
               url_name='potlako_reports:worklist_url'))

potlako_reports.append_item(
    NavbarItem(name='Follow Up Reports',
               label='Follow Up Reports',
               fa_icon='fa-cogs',
               url_name='potlako_reports:follow_up_url'))

site_navbars.register(potlako_reports)
