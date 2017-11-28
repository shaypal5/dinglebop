"""A checksum-based incremental versioning scheme."""

from .util import sha3_256_checksum

from .versioning import _set_scheme_by_name


def _increment_version_gen(num_digits):
    fmt_str = 'v{' + '0:0{}d'.format(num_digits) + '}'
    def _increment_version(version=None):
        if version is None:
            current_ver = 0
        else:
            current_ver = int(version[1:])
        return fmt_str.format(current_ver + 1)
    return _increment_version


def checksum_incremental_by_num_digits(num_digits=None):
    """Returns a checksum-incremental versioning scheme by number of diguts.

    To make the scheme produce naturally lexicographically ordered version
    numbers, the maximum version number needs to be set in advance, and all
    version strings must be padded accordingly with zeroes. For example, to
    support up to 999 different versions of the dataset, the scheme needs to
    pad all version numbers to bring them up to a length-three version number
    string, so version 3 will be written as 'v003'.

    Parameters
    ---------
    num_digits : int, optional
        The fixed number of digits this versioning scheme will support. If not
        given, 8 is used, yielding a versioning scheme that can support up to
        100 million versions.

    Returns
    -------
    function
        A versioning scheme function.
    """
    if num_digits is None:
        num_digits = 8
    inc_ver = _increment_version_gen(num_digits)
    def checksum_incremental(dataset, filepath, dump_dtime, dingle_index):
        latest_entry = dingle_index.get_latest_dataset_entry(
            dataset.identifier)
        if not latest_entry:
            return inc_ver()
        latest_v = latest_entry['version']
        latest_checksum = latest_entry.get('checksum', None)
        new_checksum = sha3_256_checksum(filename=filepath)
        if new_checksum == latest_checksum:
            return latest_v
        return inc_ver(latest_v)
    return checksum_incremental


_set_scheme_by_name('checksum_incremental',
                    checksum_incremental_by_num_digits())
_set_scheme_by_name(None, checksum_incremental_by_num_digits())


def _increment_dateint_version_gen(num_digits):
    fmt_str = 'v{}.{' + '0:0{}d'.format(num_digits) + '}'
    def _increment_dateint_version(new_dtime, version=None):
        if version is None:
            current_ver = 0
        else:
            current_ver = int(version[10:])
        return fmt_str.format(new_dtime.strftime('%Y%M%d', current_ver + 1))
    return _increment_dateint_version


def checksum_dateint_incremental_by_num_digits(num_digits=None):
    """Returns a checksum-dateint-incremental versioning scheme.

    The resulting versioning scheme will yield version strings that reflect
    both the date of the version creation and changes in content.

    To make the scheme produce naturally lexicographically ordered version
    numbers, the maximum version number needs to be set in advance, and all
    version strings must be padded accordingly with zeroes. For example, to
    support up to 999 different versions of the dataset per-day, the scheme
    needs to pad all same-day version numbers to bring them up to a
    length-three version number string, so version 3 created on December 17th,
    2017 will yield a version string of 'v20171217.003'.

    Parameters
    ---------
    num_digits : int, optional
        The fixed number of digits this versioning scheme will support. If not
        given, 4 is used, yielding a versioning scheme that can support up to
        10,000 versions of the dataset per-day.

    Returns
    -------
    checksum_dateint_incremental : function
        A versioning scheme function.
    """
    if num_digits is None:
        num_digits = 4
    inc_ver = _increment_version_gen(num_digits)

    def checksum_dateint_incremental(dataset, filepath, dump_dtime,
                                     dingle_index):
        latest_entry = dingle_index.get_latest_dataset_entry(
            dataset.identifier)
        if not latest_entry:
            return inc_ver(new_dtime=dump_dtime, version=None)
        latest_v = latest_entry['version']
        latest_checksum = latest_entry.get('checksum', None)
        new_checksum = sha3_256_checksum(filename=filepath)
        if new_checksum == latest_checksum:
            return latest_v
        return inc_ver(dump_dtime, latest_v)
    return checksum_dateint_incremental


_set_scheme_by_name('checksum_dateint_incremental',
                    checksum_dateint_incremental_by_num_digits())
