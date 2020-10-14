"""
check.py
====================================
Functions to check data attributed inline.
"""

import logging

import pandas as pd


def check_missing_iso(record: dict):
    """
    Function to check for missing ISO codes

    Note: will not throw an error for "unknown" values which much be
    handled later

    """

    if pd.isnull(record["iso"]):

        raise ValueError(
            "Record: "
            + record["who_id"]
            + " Dataset: "
            + record["dataset"]
            + " - Missing ISO code."
        )

    return None


def check_missing_who_code(record: dict):
    """
    Function to check for null who codes

    Note: will not throw an error for "unknown" values which much be
    handled later

    """

    if pd.isnull(record["who_code"]):

        raise ValueError(
            "Record: "
            + record["who_id"]
            + " Dataset: "
            + record["dataset"]
            + " - Missing WHO code."
        )

    return None
