import os
import sys
import subprocess
import shutil
import kaa
import kaa.log


def select_clipboard():
    """Select clipboard class for the platform."""
    return Clipboard()


class Clipboard:
    CLIPCOMMAND = 'xclip'
    COPYCOMMAND = 'xclip -i -selection clipboard'
    PASTECOMMAND = 'xclip  -o -selection clipboard'

    """Basic clipboard class without platform's native clipboard."""

    # Max history of clipboard entry.
    MAX_CLIPBOARD = 10

    def _get_hist(self):
        return kaa.app.config.hist('clipboard', max_hist=self.MAX_CLIPBOARD)

    def get(self):
        """Get current clipboard entry."""
        all = self.get_all()

        try:
            ret = subprocess.check_output(self.PASTECOMMAND, shell=True, universal_newlines=False).decode()
        except:
            ret = all[0] if all else ''
        if ret:
            self._get_hist().add(ret)
        
        return ret

    def get_all(self):
        """Get clipboard history."""

        return [s for s, i in self._get_hist().get() if s]

    def _set(self, s):
        p = subprocess.Popen(
            self.COPYCOMMAND,
            stdin=subprocess.PIPE,
            shell=True,
            universal_newlines=False)
        p.stdin.write(s.encode())
        p.stdin.close()
        p.wait()
        self._get_hist().add(s)

    def set(self, s):
        self._set(s)