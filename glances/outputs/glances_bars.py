# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# Copyright (C) 2019 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Manage bars for Glances output."""

from __future__ import division

from math import modf


class Bar(object):

    """Manage bar (progression or status).

    import sys
    import time
    b = Bar(10)
    for p in range(0, 100):
        b.percent = p
        print("\r%s" % b),
        time.sleep(0.1)
        sys.stdout.flush()
    """

    def __init__(self, size, percentage_char='|', empty_char=' ', pre_char='[', post_char=']', with_text=True):
        # Build curses_bars
        self.__curses_bars = [empty_char] * 5 + [percentage_char] * 5
        # Bar size
        self.__size = size
        # Bar current percent
        self.__percent = 0
        # Min and max value
        self.min_value = 0
        self.max_value = 100
        # Char used for the decoration
        self.__pre_char = pre_char
        self.__post_char = post_char
        self.__empty_char = empty_char
        self.__with_text = with_text

    @property
    def size(self, with_decoration=False):
        # Return the bar size, with or without decoration
        if with_decoration:
            return self.__size
        if self.__with_text:
            return self.__size - 6

    @property
    def percent(self):
        return self.__percent

    @percent.setter
    def percent(self, value):
        if value <= self.min_value:
            value = self.min_value
        if value >= self.max_value:
            value = self.max_value
        self.__percent = value

    @property
    def pre_char(self):
        return self.__pre_char

    @property
    def post_char(self):
        return self.__post_char

    def get(self):
        """Return the bars."""
        frac, whole = modf(self.size * self.percent / 100.0)
        ret = self.__curses_bars[8] * int(whole)
        if frac > 0:
            ret += self.__curses_bars[int(frac * 8)]
            whole += 1
        ret += self.__empty_char * int(self.size - whole)
        if self.__with_text:
            ret = '{}{:5.1f}%'.format(ret, self.percent)
        return ret

    def __str__(self):
        """Return the bars."""
        return self.get()
