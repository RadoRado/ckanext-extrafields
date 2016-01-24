import ckan.plugins as p
import ckan.plugins.toolkit as tk

import time
import datetime


def dataset_expired(date):
    # TODO: Fixme - make anoter helper that decides if time check should be done
    if date.strip() == "":
        return False

    today = datetime.date.today()
    parsed = time.strptime(date, '%Y-%m-%d')
    due_date = datetime.date(parsed.tm_year, parsed.tm_mon, parsed.tm_mday)

    return today > due_date


class ExtrafieldsPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IConfigurer)
    p.implements(p.IDatasetForm)
    p.implements(p.ITemplateHelpers)

    def _modify_package_schema(self, schema):
        schema.update({
            'due_date': [tk.get_validator('ignore_missing'),
                         tk.get_converter('convert_to_extras')],
            'due_date_info': [tk.get_validator('ignore_missing'),
                              tk.get_converter('convert_to_extras')]
        })

        return schema

    def create_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).show_package_schema()
        schema.update({
            'due_date': [tk.get_converter('convert_from_extras'),
                         tk.get_validator('ignore_missing')],
            'due_date_info': [tk.get_converter('convert_from_extras'),
                              tk.get_validator('ignore_missing')],

        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def update_config(self, config_):
        tk.add_template_directory(config_, 'templates')
        tk.add_public_directory(config_, 'public')
        tk.add_resource('fanstatic', 'extrafields')

    def get_helpers(self):
        helpers = {
            'extrafields_dataset_expired': dataset_expired
        }

        return helpers
