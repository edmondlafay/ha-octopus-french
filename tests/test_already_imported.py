"""Tests for _already_imported date comparison."""

from custom_components.octopus_french.sensors.electricity import _already_imported


def test_none_last_date_never_skips():
    assert not _already_imported("2026-11-24T00:00:00+01:00", None)


def test_same_instant_different_offsets_is_skipped():
    # DB-restored value is UTC, API value has local offset: same instant.
    assert _already_imported("2026-11-24T00:00:00+01:00", "2026-11-23T23:00:00+00:00")


def test_next_day_not_skipped():
    assert not _already_imported("2026-11-25T00:00:00+01:00", "2026-11-23T23:00:00+00:00")


def test_half_hour_slot_of_restored_bucket_is_skipped():
    # 30-min restore marks hh:30 UTC as last imported.
    assert _already_imported("2026-11-24T11:30:00+01:00", "2026-11-24T10:30:00+00:00")
    assert not _already_imported("2026-11-24T12:00:00+01:00", "2026-11-24T10:30:00+00:00")
