"""
Python STIX 2.0 Data Markings API.

These high level functions will operate on both object level markings and
granular markings unless otherwise noted in each of the functions.
"""

from stix2.markings import granular_markings, object_markings


def get_markings(obj, selectors=None, inherited=False, descendants=False):
    """
    Get all markings associated to the field(s).

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the properties appear.
        inherited: If True, include object level markings and granular markings
            inherited relative to the properties.
        descendants: If True, include granular markings applied to any children
            relative to the properties.

    Returns:
        list: Marking identifiers that matched the selectors expression.

    Note:
        If ``selectors`` is None, operation will be performed only on object
        level markings.

    """
    if selectors is None:
        return object_markings.get_markings(obj)

    results = granular_markings.get_markings(
        obj,
        selectors,
        inherited,
        descendants
    )

    if inherited:
        results.extend(object_markings.get_markings(obj))

    return list(set(results))


def set_markings(obj, marking, selectors=None):
    """
    Removes all markings associated with selectors and appends a new granular
    marking. Refer to `clear_markings` and `add_markings` for details.

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the properties appear.
        marking: identifier or list of marking identifiers that apply to the
            properties selected by `selectors`.

    Returns:
        A new version of the given SDO or SRO with specified markings removed
        and new ones added.

    Note:
        If ``selectors`` is None, operations will be performed on object level
        markings. Otherwise on granular markings.

    """
    if selectors is None:
        return object_markings.set_markings(obj, marking)
    else:
        return granular_markings.set_markings(obj, marking, selectors)


def remove_markings(obj, marking, selectors=None):
    """
    Removes granular_marking from the granular_markings collection.

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the properties appear.
        marking: identifier or list of marking identifiers that apply to the
            properties selected by `selectors`.

    Raises:
        InvalidSelectorError: If `selectors` fail validation.
        MarkingNotFoundError: If markings to remove are not found on
            the provided SDO or SRO.

    Returns:
        A new version of the given SDO or SRO with specified markings removed.

    Note:
        If ``selectors`` is None, operations will be performed on object level
        markings. Otherwise on granular markings.

   """
    if selectors is None:
        return object_markings.remove_markings(obj, marking)
    else:
        return granular_markings.remove_markings(obj, marking, selectors)


def add_markings(obj, marking, selectors=None):
    """
    Appends a granular_marking to the granular_markings collection.

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the properties appear.
        marking: identifier or list of marking identifiers that apply to the
            properties selected by `selectors`.

    Raises:
        InvalidSelectorError: If `selectors` fail validation.

    Returns:
        A new version of the given SDO or SRO with specified markings added.

    Note:
        If ``selectors`` is None, operations will be performed on object level
        markings. Otherwise on granular markings.

    """
    if selectors is None:
        return object_markings.add_markings(obj, marking)
    else:
        return granular_markings.add_markings(obj, marking, selectors)


def clear_markings(obj, selectors=None):
    """
    Removes all granular_marking associated with the selectors.

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the field(s) appear(s).

    Raises:
        InvalidSelectorError: If `selectors` fail validation.
        MarkingNotFoundError: If markings to remove are not found on
            the provided SDO or SRO.

    Returns:
        A new version of the given SDO or SRO with specified markings cleared.

    Note:
        If ``selectors`` is None, operations will be performed on object level
        markings. Otherwise on granular markings.

    """
    if selectors is None:
        return object_markings.clear_markings(obj)
    else:
        return granular_markings.clear_markings(obj, selectors)


def is_marked(obj, marking=None, selectors=None, inherited=False, descendants=False):
    """
    Checks if field(s) is marked by any marking or by specific marking(s).

    Args:
        obj: An SDO or SRO object.
        selectors: string or list of selectors strings relative to the SDO or
            SRO in which the field(s) appear(s).
        marking: identifier or list of marking identifiers that apply to the
            properties selected by `selectors`.
        inherited: If True, include object level markings and granular markings
            inherited to determine if the properties is/are marked.
        descendants: If True, include granular markings applied to any children
            of the given selector to determine if the properties is/are marked.

    Returns:
        bool: True if ``selectors`` is found on internal SDO or SRO collection.
            False otherwise.

    Note:
        When a list of marking identifiers is provided, if ANY of the provided
        marking identifiers match, True is returned.

        If ``selectors`` is None, operation will be performed only on object
        level markings.

    """
    if selectors is None:
        return object_markings.is_marked(obj, marking)

    result = granular_markings.is_marked(
        obj,
        marking,
        selectors,
        inherited,
        descendants
    )

    if inherited:
        granular_marks = granular_markings.get_markings(obj, selectors)
        object_marks = object_markings.get_markings(obj)

        if granular_marks:
            result = granular_markings.is_marked(
                obj,
                granular_marks,
                selectors,
                inherited,
                descendants
            )

        result = result or object_markings.is_marked(obj, object_marks)

    return result


class MarkingsMixin():
    pass


# Note that all of these methods will return a new object because of immutability
MarkingsMixin.get_markings = get_markings
MarkingsMixin.set_markings = set_markings
MarkingsMixin.remove_markings = remove_markings
MarkingsMixin.add_markings = add_markings
MarkingsMixin.clear_markings = clear_markings
MarkingsMixin.is_marked = is_marked
