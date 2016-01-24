import ckan.plugins as p
import ckan.plugins.toolkit as tk


class ExtrafieldsPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IConfigurer)
    p.implements(p.IDatasetForm)

    def create_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
        schema.update({
            'dataset_due_date': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_to_extras')],
            'dataset_due_date_info': [tk.get_validator('ignore_missing'),
                                      tk.get_converter('convert_to_extras')]
        })
        return schema

    def update_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
        schema.update({
            'dataset_due_date': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_to_extras')],
            'dataset_due_date_info': [tk.get_validator('ignore_missing'),
                                      tk.get_converter('convert_to_extras')]
        })
        return schema

    def show_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            'dataset_due_date': [tk.get_validator('ignore_missing'),
                                 tk.get_converter('convert_from_extras')],
            'dataset_due_date_info': [tk.get_validator('ignore_missing'),
                                      tk.get_converter('convert_from_extras')]
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
