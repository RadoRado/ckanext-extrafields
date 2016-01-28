import time
import datetime


def parse_date(date):
    parsed = time.strptime(date, '%Y-%m-%d')
    return (parsed.tm_year, parsed.tm_mon, parsed.tm_mday)


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


def dateformat(value, format="%d/%m/%Y"):
    year, month, day = parse_date(value)
    d = datetime.date(year, month, day)
    return d.strftime(format)


class TemplateHelpers:

    def get_helpers(self):
        helpers = {
            'extrafields_dataset_expired': dataset_expired,
            'extrafields_dateformat': dateformat
        }

        return helpers
