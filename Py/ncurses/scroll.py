# coding: utf-8

import curses as cs
import time
import sys


class WinManager:
    u""" Windows manager class. """
    
    #: Instance of `curses.WindowObject` returned from `curses.initscr`.
    stdscr = None
    
    #: Current active window, instance of `ListWindow`.
    active_win = None

    #: Map of actions that will take place when user pressed key.
    #: { char_code: callable_action }
    actions_map = None

    @property
    def wins(self):
        if not hasattr(self, '_wins'):
            self._wins = []
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value
        self.active_win = len(value) > 0 and value[0] or None

    def __init__(self):
        self.stdscr = cs.initscr()
        cs.noecho()
        cs.curs_set(0)

        self.actions_map = {
            cs.KEY_UP: self.mov_up,
            cs.KEY_DOWN: self.mov_down,
            ord('q'): self.exit,
            9: self.switch
        }

    def exit(self):
        cs.endwin()
        sys.exit(0)

    def run(self):
        while True:
            c = self.active_win.getch()
            action = self.actions_map.get(c)
            if callable(action): action()

    def mov(self, offset):
        win = self.active_win
        cursor, _ = win.getyx()
        win.clear_row(cursor)
        
        lcount = len(win.lines)
        win.current += offset
        win.current = win.current > 0 and win.current or 0
        win.current = win.current >= lcount and lcount - 1 or win.current

        cursor += offset
        cursor = cursor < 1 and 1 or cursor > win.vsize and win.vsize or cursor
        
        if cursor == 1 or cursor == win.vsize:
            win.clean()
            win.scroll_lines(cursor)
        else:
            win.move(cursor, 1)

        win.select_row(cursor)
        win.refresh()

    def mov_up(self):
        self.mov(-1)

    def mov_down(self):
        self.mov(1)

    def switch(self):
        win = self.active_win.tab_win
        if not win:
            i = self.wins.index(self.active_win) + 1
            win = i == len(self.wins) and self.wins[0] or self.wins[i]
        win.active()



class ListWindow:
    u""" .
    Window allows you to use the arrow keys on your keyboard 
    to navigate on text rows. 
    """

    #: Instance of `curses.WindowObject`
    win = None

    #: Neabordy window wich be switched then TAB key pressed.
    #: Instance of `ListWindow`.
    tab_win = None

    #: Count of lines available in window.
    vsize = None

    #: Count of chars available in line of window.
    hsize = None

    #: List of text items
    lines = None

    #: Current selected row.
    current = 0

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value:
            self.addstr(0, 1, value[:self.hsize])
            self._title = value

    def __init__(self, mgr, *a, **kw):
        mgr.wins.append(self)
        self.mgr = mgr
        self.win = cs.newwin(*a)
        self._recalc_bounds()
        self.tab_win = kw.get('tab_win')
        self.border(0, 0)
        self.keypad(True)
        self.title = kw.get('title')
        self.fill(kw.get('lines', []))
        self.move(1, 1)
        self.refresh()

    def __getattr__(self, name):
        return getattr(self.win, name)

    def _addstr(self, vpos, text): 
        self.addstr(vpos, 1, text[:self.hsize])

    def _recalc_bounds(self):
        y, x = self.getmaxyx()
        border_reserved = 2
        self.vsize = y - border_reserved
        self.hsize = x - border_reserved

    def active(self):
        self.mgr.active_win = self
    
    def clean(self):
        self.clear()
        self.border(0, 0)
        self.title = self.title

    def clear_row(self, vpos):
        self.chgat(vpos, 1, self.hsize, cs.A_NORMAL)
        
    def fill(self, lines):
        self.lines = lines
        for vpos, line in enumerate(lines[:self.vsize], start=1):
            self._addstr(vpos, line)
    
    def scroll_lines(self, cursor):
        offset = self.current - (cursor - 1)
        lines = self.lines[offset:][:self.vsize]
        for vpos, line in enumerate(lines, start=1):
            self._addstr(vpos, line)

    def select_row(self, vpos):
        self.chgat(vpos, 1, self.hsize, cs.A_REVERSE)


if __name__ == '__main__':
    lines = list(map(str, range(1, 40)))
    mgr = WinManager()
    fwin = ListWindow(mgr, 10, 30, 1, 5, title='First window', lines=lines)
    swin = ListWindow(mgr, 10, 30, 1, 35, title='Second window', lines=lines)
    twin = ListWindow(mgr, 10, 30, 11, 5, title='Third window', lines=lines)
    fwin.active()
    mgr.run()
    

