from errno import *
from toolbox import TestError

###############################################################################
#
# Try to violate permissions
#
###############################################################################

def subtest_1(ctx):
    """Impermissible open O_TRUNC|O_WRONLY"""
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, wo=1, tr=1, err=EACCES, as_bin=1)
    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f, wo=1, write="shark")
    ctx.open_file(f, ro=1, read="sharkyyy:zzz")
    ctx.open_file(f, ro=1, read="sharkyyy:zzz", as_bin=1)

def subtest_2(ctx):
    """Impermissible open O_WRONLY"""
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, wo=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f, wo=1, write="shark")
    ctx.open_file(f, ro=1, read="sharkyyy:zzz")
    ctx.open_file(f, ro=1, read="sharkyyy:zzz", as_bin=1)

def subtest_3(ctx):
    """Impermissible open O_APPEND"""
    f = ctx.rootfile() + ctx.termslash()

    ctx.open_file(f, app=1, err=EACCES, as_bin=1)
    ctx.open_file(f, app=1, err=EACCES, as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.open_file(f, app=1, write="shark")
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzzshark")
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzzshark", as_bin=1)

    #
    #
    #
def subtest_4(ctx):
    """Impermissible truncate"""
    f = ctx.rootfile() + ctx.termslash()

    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 12:
            raise TestError(f + ": Initial size (" + str(size) + ") is not 12")
    ctx.truncate(f, 4, err=EACCES, as_bin=1)
    ctx.truncate(f, 4, err=EACCES, as_bin=1)
    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 12:
            raise TestError(f + ": Size (" + str(size) + ") is not still 12")
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz", as_bin=1)
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
    ctx.truncate(f, 4)
    if not ctx.termslash():
        size = ctx.get_file_size(f)
        if size != 4:
            raise TestError(f + ": Size (" + str(size) + ") is not 4")
    ctx.open_file(f, ro=1, read=":xxx")
    ctx.open_file(f, ro=1, read=":xxx", as_bin=1)

    #
    #
    #
def subtest_5(ctx):
    """Impermissible utimes"""
    f = ctx.rootfile() + ctx.termslash()

    if not ctx.termslash():
        atime = ctx.get_file_atime(f)
        mtime = ctx.get_file_mtime(f)
    ctx.utimes(f, err=EACCES, as_bin=1)
    ctx.utimes(f, err=EACCES, as_bin=1)
    if not ctx.termslash():
        if ctx.get_file_atime(f) != atime:
            raise TestError(f + ": Access time unexpectedly changed")
        if ctx.get_file_mtime(f) != mtime:
            raise TestError(f + ": Modification time unexpectedly changed")
    ctx.utimes(f)
    if not ctx.termslash():
        if ctx.get_file_atime(f) == atime:
            raise TestError(f + ": Access time didn't change")
        if ctx.get_file_mtime(f) == mtime:
            raise TestError(f + ": Modification time didn't change")
    ctx.open_file(f, ro=1, read=":xxx:yyy:zzz")
