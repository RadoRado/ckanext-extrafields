import ckan.plugins as p
import ckan.plugins.toolkit as tk
from template_helpers import TemplateHelpers
from ckan.common import _, ungettext
# from ckan.lib.plugins import DefaultTranslation


def either_compiled_at_or_expires_on(key,
                                     flattened_data,
                                     errors,
                                     context):
    keys = [('compiled_at',), ('expires_on',)]
    present_keys = filter(lambda key: flattened_data[key].strip() != "", keys)

    if len(present_keys) == 0:
        raise tk.Invalid(_('Either compiled_at or expires_on must be present'))


class ExtrafieldsPlugin(p.SingletonPlugin,
                        tk.DefaultDatasetForm,
                        # DefaultTranslation,
                        TemplateHelpers):
    p.implements(p.IConfigurer)
    # p.implements(p.ITranslation)
    p.implements(p.IDatasetForm)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IValidators)

    def _modify_package_schema(self, schema):
        schema.update({
            'compiled_at': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'expires_on': [tk.get_validator('ignore_missing'),
                           tk.get_converter('convert_to_extras')],
            'expiration_info': [tk.get_validator('ignore_missing'),
                                tk.get_converter('convert_to_extras')],
            '__after': [tk.get_validator('either_compiled_at_or_expires_on')]
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
            'compiled_at': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'expires_on': [tk.get_converter('convert_from_extras'),
                           tk.get_validator('ignore_missing')],
            'expiration_info': [tk.get_converter('convert_from_extras'),
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

    def get_validators(self):
        return {
            'either_compiled_at_or_expires_on': either_compiled_at_or_expires_on
        }
