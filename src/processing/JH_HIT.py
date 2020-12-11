import pandas as pd
from countrycode.countrycode import countrycode

# hot fix for sys.path issues in test environment
try:

    from processing import utils
    from processing import check

except Exception as e:

    from src.processing import utils
    from src.processing import check


def transform(record: dict, key_ref: dict, country_ref: pd.DataFrame, who_coding: pd.DataFrame, prov_measure_filter: pd.DataFrame):
    """
    Apply transformations to JH_HIT records.

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
    prov_measure_filter : pd.DataFrame
        Reference for filtering by `prov_measure` values.

    Returns
    -------
    type
        Record with transformations applied.

    """

    # 1.
    if pd.isnull(record['locality']) and pd.isnull(record['usa_county']):
        return(None)

    # 2. generator function of new record with correct keys (shared)
    new_record = utils.generate_blank_record()

    # 3. replace data in new record with data from old record using column
    # reference (shared)
    record = utils.apply_key_map(new_record, record, key_ref)

    # 4.
    record = apply_prov_measure_filter(record, prov_measure_filter)

    # replace with a None - passing decorator
    if record is None:
        return(None)

    # 5. Handle date - infer format (shared)
    record = utils.parse_date(record)

    # 6. Assign unique ID (shared)
    #record = utils.assign_id(record)

    # 7. replace non ascii characters (shared)

    # 8. replace sensitive country names by ISO (utils)
    record = utils.replace_sensitive_regions(record)

    # 9. assign ISO code
    record['iso'] = countrycode(codes=record['country_territory_area'], origin='country_name', target='iso3c')

    # 10. check for missing ISO codes (shared)
    check.check_missing_iso(record)

    # 11. Join WHO accepted country names (shared)
    record = utils.assign_who_country_name(record, country_ref)

    # 12. Join who coding from lookup (shared)
    record = utils.assign_who_coding(record, who_coding)

    # 13. check for missing WHO codes (shared)
    check.check_missing_who_code(record)

    # 14. replace admin_level values
    record = utils.replace_conditional(record, 'admin_level', '', 'unknown')
    record = utils.replace_conditional(record, 'admin_level', 'Yes', 'national')
    record = utils.replace_conditional(record, 'admin_level', 'No', 'state')

    # Replace JH enforcement == 'unknown' with None
    record = utils.replace_conditional(record, 'enforcement', 'unknown', None)

    # Replace JH targeter values
    record = utils.replace_conditional(record, 'targeted', 'geographic subpobulation', None)
    record = utils.replace_conditional(record, 'targeted', 'entire population', None)

    # 15. fill_not_enough_to_code
    record = fill_not_enough_to_code(record)

    # 16. replace unknown non_compliance_penalty
    record = utils.replace_conditional(record, 'non_compliance_penalty', 'unknown', 'Not Known')

    record = utils.remove_tags(record)

    record = blank_record_and_url(record)

    return(record)


def blank_record_and_url(record: dict):
    """
    Assign who_code == 11 and 'Not enough to code' to records with no `comments` AND no `url`.

    Parameters
    ----------
    record : dict
        Input record.

    Returns
    -------
    type
        Record with coding altered.

    """

    if (pd.isna(record['comments'])) and (pd.isna(record['link'])) and (pd.isna(record['alt_link'])):

        record['who_code'] = '11'
        record['who_category'] = 'Not enough to code'
        record['who_subcategory'] = 'Not enough to code'
        record['who_measure'] = 'Not enough to code'

    return(record)


def apply_prov_measure_filter(record: dict, prov_measure_filter: pd.DataFrame):
    """
    Filter only some `prov_measure` and `prov_category` values.

    Only some JH_HIT codings are accepted.

    Relies on `prov_measure_filter` defined in `config`.

    Parameters
    ----------
    record : dict
        Input record.
    prov_measure_filter : pd.DataFrame
        Config of which codings to drop. Defined in `config` directory.

    Returns
    -------
    type
        If coding is included in WHO PHSM dataset, record, else None.

    """

    if record['prov_category'] in list(prov_measure_filter['prov_category']) and record['prov_measure'] in list(prov_measure_filter['prov_measure']):

        return record

    else:

        return(None)

def fill_not_enough_to_code(record: dict):
    """
    Function to add "not enough to code" label when comments are blank.

    Parameters
    ----------
    record : dict
        Input record.

    Returns
    -------
    type
        Record with `prov_measure` and `prov_category` values altered conditionally.

    """

    if record['comments'] == '' and record['prov_category'] != 'school_closed':

        record['prov_measure'] = 'not_enough_to_code'
        record['prov_category'] = 'not_enough_to_code'

    return(record)
