
import pxul

from collections import defaultdict
import cPickle as pickle
import os

__package = 'trax'


def debug(string):
    pxul.logging.logger.debug('[{package}] {msg}'.format(package=__package, msg=string))

class Trax(object):

    def __init__(self, traxdir='.trax'):
        self._traxdir = traxdir
        self._logcount = defaultdict(lambda: 0)

    def _path(self, name):
        return os.path.join(self._traxdir, name)

    def _cpt(self, name):
        return self._path(name) + '.cpt'

    def _logdir(self, name):
        return self._path(name)

    def _log(self, name, i):
        logdir = self._logdir(name)
        logpath = os.path.join(logdir, str(i)) + '.log'
        return logpath

    def _logpaths(self, name):
        for i in xrange(self._logcount[name]):
            yield self._log(name, i)

    def _clear_log(self, name):
        while self._logcount[name] > 0:
            i = self._logcount[name] - 1
            path = self._log(name, i)
            os.unlink(path)
            self._logcount[name] -= 1
        os.rmdir(self._logdir(name))
        debug("Cleared log for '{}'".format(name))

    def _write(self, obj, path):
        p = os.path.abspath(path)
        pxul.os.ensure_dir(os.path.dirname(p))
        with open(p, 'wb') as fd:
            pickle.dump(obj, fd, protocol=pickle.HIGHEST_PROTOCOL)
        debug('Stored value in {}'.format(path))

    def _read(self, path):
        with open(path, 'rb') as fd:
            obj = pickle.load(fd)
        debug('Loaded value in {}'.format(path))
        return obj

    def checkpoint(self, **kws):
        "Checkpoint a 'name'->value and clear the logs for 'name'"
        for name, val in kws.iteritems():
            cpt = self._cpt(name)
            self._write(val, cpt)
            self._clear_log(name)

    def log(self, **kws):
        "Log a 'name'->value"
        for name, val in kws.iteritems():
            log = self._log(name, self._logcount[name])
            self._write(val, log)
            self._logcount[name] += 1

    def recover(self, name, create=None, replay_log=lambda state, log: log):
        """
        Recover 'name's value from a checkpoint and then replay the log.

        Parameters:
          name :: str : the name of the value
          create :: fun() -> a: a 0-ary function to create the value if it is not in Trax
          replay_log :: state -> log -> state: function to fold over the log values to update the state

        Returns
          The state of the checkpoint with the logs replayed.
        """

        if create is None:
            raise ValueError, "'create' must not be None"

        cpt = self._cpt(name)
        if not os.path.exists(cpt):
            state = create()
            self.checkpoint(**{name:state})
            return state
        else:
            state = self._read(cpt)
            for logpath in self._logpaths(name):
                log = self._read(logpath)
                state = replay_log(state, log)
            return state
