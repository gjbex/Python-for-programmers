class IntervalNode:
    """Node used by :class:`IntersectionTree`.

    Parameters
    ----------
    interval: tuple
        A tuple ``(start, end)`` representing the interval. ``start`` must
        be less than or equal to ``end``.
    """

    __slots__ = ("interval", "max", "left", "right")

    def __init__(self, interval):
        self.interval = interval
        self.max = interval[1]
        self.left = None
        self.right = None


class IntersectionTree:
    """A simple interval/"intersection" tree implementation.

    The tree stores intervals and supports searching for intervals that
    intersect with a query interval.  The public ``insert`` and ``search``
    methods perform validation of the input and delegate the actual work to
    the private ``_insert`` and ``_search`` helpers.  This ensures that the
    validation is performed only once per operation and not on every
    recursive call.
    """

    def __init__(self):
        self.root = None

    # ------------------------------------------------------------------
    # Helper methods
    def _validate_interval(self, interval):
        """Validate *interval* and return it as ``(start, end)``.

        Parameters
        ----------
        interval : tuple
            The candidate interval.

        Returns
        -------
        tuple
            ``(start, end)`` with ``start`` and ``end`` as floats/ints.

        Raises
        ------
        ValueError
            If the interval is not a 2-tuple or ``start`` > ``end``.
        """

        if not (isinstance(interval, (tuple, list)) and len(interval) == 2):
            raise ValueError("interval must be a tuple of two values")
        start, end = interval
        if start > end:
            raise ValueError("interval start must be <= end")
        return (start, end)

    # ------------------------------------------------------------------
    # Public API
    def insert(self, interval):
        """Insert *interval* into the tree after validation."""

        validated = self._validate_interval(interval)
        self.root = self._insert(self.root, validated)
        return self

    def search(self, interval):
        """Return a list of intervals intersecting ``interval``."""

        validated = self._validate_interval(interval)
        return self._search(self.root, validated, [])

    # ------------------------------------------------------------------
    # Private recursive helpers
    def _insert(self, node, interval):
        """Recursive part of :meth:`insert`.

        Parameters
        ----------
        node : IntervalNode or ``None``
            The current node in the recursion.
        interval : tuple
            Interval to insert.  Assumed to be valid.
        """

        if node is None:
            return IntervalNode(interval)

        start, _ = interval
        node_start = node.interval[0]
        if start < node_start:
            node.left = self._insert(node.left, interval)
        else:
            node.right = self._insert(node.right, interval)

        node.max = max(node.max, interval[1])
        return node

    def _search(self, node, interval, result):
        """Recursive part of :meth:`search`.

        Parameters
        ----------
        node : IntervalNode or ``None``
            Current node in traversal.
        interval : tuple
            Interval to search for.  Assumed to be valid.
        result : list
            Accumulator list for overlapping intervals.
        """

        if node is None:
            return result

        start, end = interval
        node_start, node_end = node.interval

        if node_start <= end and start <= node_end:
            result.append(node.interval)

        if node.left is not None and node.left.max >= start:
            self._search(node.left, interval, result)
        if node.right is not None and node_start <= end:
            self._search(node.right, interval, result)

        return result


__all__ = ["IntersectionTree", "IntervalNode"]
