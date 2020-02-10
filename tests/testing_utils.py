import os
import platform
import tempfile
import shutil


IS_WINDOWS = platform.system().lower() == "windows"
RUNNING_ON_CI = os.environ.get("APPVEYOR", False)
RUNNING_TEST_FOR_MASTER_ON_CI = os.environ.get("APPVEYOR_REPO_BRANCH", "master") != "master"
CI_OVERRIDE = os.environ.get("APPVEYOR_CI_OVERRIDE", False)
RUN_BY_CANARY = os.environ.get("BY_CANARY", None) is not None


class FileCreator(object):
    def __init__(self):
        self.rootdir = tempfile.mkdtemp()

    def remove_all(self):
        if os.path.exists(self.rootdir):
            shutil.rmtree(self.rootdir)

    def create_file(self, filename, contents, mtime=None, mode="w"):
        """Creates a file in a tmpdir
        ``filename`` should be a relative path, e.g. "foo/bar/baz.txt"
        It will be translated into a full path in a tmp dir.
        If the ``mtime`` argument is provided, then the file's
        mtime will be set to the provided value (must be an epoch time).
        Otherwise the mtime is left untouched.
        ``mode`` is the mode the file should be opened either as ``w`` or
        `wb``.
        Returns the full path to the file.
        """
        full_path = os.path.join(self.rootdir, filename)
        if not os.path.isdir(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, mode) as f:
            f.write(contents)
        current_time = os.path.getmtime(full_path)
        # Subtract a few years off the last modification date.
        os.utime(full_path, (current_time, current_time - 100000000))
        if mtime is not None:
            os.utime(full_path, (mtime, mtime))
        return full_path

    def append_file(self, filename, contents):
        """Append contents to a file
        ``filename`` should be a relative path, e.g. "foo/bar/baz.txt"
        It will be translated into a full path in a tmp dir.
        Returns the full path to the file.
        """
        full_path = os.path.join(self.rootdir, filename)
        if not os.path.isdir(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
        with open(full_path, "a") as f:
            f.write(contents)
        return full_path

    def full_path(self, filename):
        """Translate relative path to full path in temp dir.
        f.full_path('foo/bar.txt') -> /tmp/asdfasd/foo/bar.txt
        """
        return os.path.join(self.rootdir, filename)
