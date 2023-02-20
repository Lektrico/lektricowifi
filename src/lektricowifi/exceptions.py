"""Exceptions for Lektrico device."""


class DeviceError(Exception):
    """Generic Lektrico device exception."""


class DeviceConnectionError(DeviceError):
    """Lektrico device connection exception."""