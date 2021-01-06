import pandas as pd
from countrycode.countrycode import countrycode

# hot fix for sys.path issues in test environment
try:

    from processing import utils
    from processing import check

except Exception:

    from src.processing import utils
    from src.processing import check


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame):
    """
    Apply transformations to ACAPS records.

    Parameters
    ----------
    record : dict
        Input record.
    key_ref : dict
        Reference for key mapping.
    country_ref : pd.DataFrame
        Reference for WHO accepted country names.
    who_coding : pd.DataFrame
        Reference for WHO coding.

    Returns
    -------
    dict
        Record with transformations applied.

    """

    # 1. Create a new blank record
    new_record = utils.generate_blank_record()

    # 2. replace data in new record with data from old record using key_ref
    record = utils.apply_key_map(new_record, record, key_ref)

    # Remove records where area covered is a single space
    if record['area_covered'] == ' ':

        record['area_covered'] = ''

    # 6. Assign unique ID (shared)
    #record = utils.assign_id(record)

    # shift areas that should be countries.
    record = utils.replace_country(record, 'Denmark', 'Greenland')

    # 3. Make manual country name changes
    record = utils.replace_conditional(record, 'country_territory_area', 'DRC', 'Democratic Republic of the Congo')
    record = utils.replace_conditional(record, 'country_territory_area', 'CAR', 'Central African Republic')
    record = utils.replace_conditional(record, 'country_territory_area', 'DPRK', 'North Korea')
    record = utils.replace_conditional(record, 'country_territory_area', 'Eswatini', 'Swaziland')

    # Make manual measure_stage changes
    record = utils.replace_conditional(record, 'measure_stage', 'Introduction / extension of measures', 'introduction / extension of measures')
    record = utils.replace_conditional(record, 'measure_stage', 'Phase-out measure', 'phase-out')

    # Make manual non_compliance_penalty changes
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Legal Action', 'legal action')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Legal action', 'legal action')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Legal', 'legal action')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Up to detention', 'up to detention')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Up to Detention', 'up to detention')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Arrest/Detention', 'arrest/detention')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Deportation', 'deportation')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Refusal to enter the country', 'refused entry')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Refusal to enter the Country', 'refused entry')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Refusal to Enter the Country', 'refused entry')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Other (add in comments)', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Fines', 'fines')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Other', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Not Available', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Not available', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Not available ', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'not available ', 'not known')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Not Applicable', 'not applicable')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'Not applicable', 'not applicable')
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'not applicable ', 'not known')

    # Replace targeted values
    record = utils.replace_conditional(record, 'targeted', 'checked', None)
    record = utils.replace_conditional(record, 'targeted', 'Checked', None)
    record = utils.replace_conditional(record, 'targeted', 'general', None)
    record = utils.replace_conditional(record, 'targeted', 'General', None)

    # 4. replace sensitive country names by ISO (utils)
    record = utils.replace_sensitive_regions(record)

    # 5. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 6. check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # 7. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 12. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 13. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 8. Add WHO PHSM admin_level values
    record = utils.add_admin_level(record)

    record = utils.remove_tags(record)

    return(record)
