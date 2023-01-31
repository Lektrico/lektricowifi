"""Exceptions for Lektrico charger."""


class ChargerError(Exception):
    """Generic Lektrico charger exception."""


class ChargerConnectionError(ChargerError):
    """Lektrico charger connection exception."""