"""
-------------------------------------------------------
Array versions of various sorts.
-------------------------------------------------------
Author:  David Brown
ID:      999999999
Email:   dbrown@wlu.ca
Section: CP164 A
__updated__ = "2021-12-16"
-------------------------------------------------------
"""
# Imports
from math import log, floor

from BST_linked import BST


class Sorts:
    """
    -------------------------------------------------------
    Defines a number of array-based sort operations.
    Uses class attribute 'swaps' to determine how many times
    elements are swapped by the class.
    Use: print(Sorts.swaps)
    Use: Sorts.swaps = 0
    -------------------------------------------------------
    """
    swaps = 0  # Tracks swaps performed.

    # The Sorts

    @staticmethod
    def gnome_sort(a):
        """
        -------------------------------------------------------
        Sorts an array using the Gnome Sort algorithm.
        Use: gnome_sort(a)
        -------------------------------------------------------
        Parameters:
            a - an array of comparable elements (list)
        Returns:
            None
        -------------------------------------------------------
        """
        n = len(a)
        pos = 0

        while pos < n - 1:

            if a[pos] <= a[pos + 1]:
                # Compared elements are in order
                pos += 1
            else:
                # Compared elements must be swapped
                Sorts._swap(a, pos, pos + 1)

                if pos > 0:
                    # Go back to compare newly-swapped element
                    pos -= 1
                else:
                    # index 0 contains smallest element so far
                    pos += 1
        return

    @staticmethod
    def radix_sort(a):
        """
        -------------------------------------------------------
        Performs a base 10 radix sort.
        Use: Sorts.radix_sort(a)
        -------------------------------------------------------
        Parameters:
            a - an array of base 10 integers (list)
        Returns:
            None
        -------------------------------------------------------
        """
        if len(a) > 0:
            # Find the largest number in a.
            max_val = max(a)
            # Find the number of digits in the largest number.
            passes = floor(log(max_val, 10) + 1)

            # Create the empty buckets.
            buckets = []

            for _ in range(10):
                buckets.append([])

            for digit in range(passes):
                # Calculate the digit extraction numerator and denominator.
                d = 10 ** digit
                n = d * 10

                for v in a:
                    # Assign the array values to the appropriate bucket.
                    # Extract the individual digit.
                    i = v % n // d
                    # Add the number to the proper bucket.
                    buckets[i].append(v)

                # Put the values back into the original array.
                # Use an index i rather than append because the length of a
                # never changes.
                i = 0

                for bucket in buckets:
                    while bucket != []:
                        a[i] = bucket.pop(0)
                        i += 1
        return

    # Sort Utilities

    @staticmethod
    def is_sorted(a):
        """
        -------------------------------------------------------
        Determines whether an array is sorted or not.
        Use: b = Sorts.is_sorted(a)
        -------------------------------------------------------
        Parameters:
            a - an array of comparable elements (?)
        Returns:
            srtd - True if contents of a are sorted,
                False otherwise (boolean)
       -------------------------------------------------------
        """
        srtd = True
        n = len(a)
        i = 0

        while srtd and i < n - 1:

            if a[i] <= a[i + 1]:
                i += 1
            else:
                srtd = False
        return srtd

    @staticmethod
    def _swap(a, i, j):
        """
        -------------------------------------------------------
        Swaps the data contents of two array elements.
        Updates 'swaps'. Values in a[i] and a[j] are swapped.
        Use: Sorts._swap(a, i, j)
        -------------------------------------------------------
        Parameters:
            a - an array of comparable elements (?)
            i - index of one value (int 0 <= i < len(a))
            j - index of another value (int 0 <= j < len(a))
        Returns:
            None
        -------------------------------------------------------
        """
        Sorts.swaps += 1

        temp = a[i]
        a[i] = a[j]
        a[j] = temp
        return

    @staticmethod
    def _shift(a, i, j):
        """
        -------------------------------------------------------
        Shifts the contents of a[j] to a[i]. Value in a[j] is copied to a[i].
        Updates 'swaps' - worth 1/3 of _swap
        Use: Sorts._shift(a, i, j)
        -------------------------------------------------------
        Parameters:
            a - an array of comparable elements (?)
            i - index of one value (int 0 <= i < len(a))
            j - index of another value (int 0 <= j < len(a))
        Returns:
            None
        -------------------------------------------------------
        """
        Sorts.swaps += 0.34

        a[i] = a[j]
        return
