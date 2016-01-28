import time
import datetime


def dataset_expired(date):
    # FIXME: make anoter helper that decides if time check should be done
    if date.strip() == "":
        return False

    today = datetime.date.today()
    parsed = time.strptime(date, '%Y-%m-%d')
    expiration_date = datetime.date(parsed.tm_year,
                                    parsed.tm_mon,
                                    parsed.tm_mday)

    return today > expiration_date


class TemplateHelpers:

    def get_helpers(self):
        helpers = {
            'extrafields_dataset_expired': dataset_expired
        }

        return helpers
