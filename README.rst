pyNfsClient
===============

.. contents::
   :local:

Introduction
------------

pyNfsClient is a generic open source toolkit for Linux NFS file system simulation as client.
Constructed parameters sent via RPC and then analyse the response in reference to NFS protocol specifications (RFC1813).
You could form your custom scenarios that consist of basic actions to meet expecations.
**Currently only NFS v3 supported, NFS v4.1 is under development.**

pyNfsClient is operating system and application independent. The toolkit is implemented using 
`Python <https://www.python.org>`__, supports both
Python 2.7 and Python 3.

pyNfsClient project is hosted on GitHub_ where you can find source code,
an issue tracker, and some further documentation.

.. _GitHub: https://github.com/CharmingYang0/NfsClient
.. _PyPI: https://pypi.org/project/NfsClient

.. image:: https://img.shields.io/pypi/v/NfsClient.svg?label=version
   :target: https://pypi.org/project/NfsClient/
   :alt: Latest version

Installation
------------

If you already have `Python <https://www.python.org>`__ with `pip <http://pip-installer.org>`__ installed,
you can simply run::

    pip install pyNfsClient

Alternatively you can get source code by downloading the source
distribution from PyPI_ and extracting it, or by cloning the project repository
from GitHub_. After that you can install the framework with::

    python setup.py install

Example
-------

Below is a simple example which lookup a file and then do several operations on it.

.. code:: python

    from pyNfsClient import (Portmap, Mount, NFSv3, MNT3_OK, NFS_PROGRAM,
                           NFS_V3, NFS3_OK, DATA_SYNC)
    
    # variable preparation
    host = "192.221.4.119"
    mount_path = "/nfsshare"
    
    auth = {"flavor": 1,
            "machine_name": "host1",
            "uid": 0,
            "gid": 0,
            "aux_gid": list(),
            }
    
    # portmap initialization
    portmap = Portmap(host, timeout=3600)
    portmap.connect()
    
    # mount initialization
    mnt_port = portmap.getport(Mount.program, Mount.program_version)
    mount = Mount(host=host, port=mnt_port, timeout=3600)
    mount.connect()
    
    # do mount
    mnt_res =mount.mnt(mount_path, auth)
    if mnt_res["status"] == MNT3_OK:
        root_fh =mnt_res["mountinfo"]["fhandle"]
        try:
            nfs_port =portmap.getport(NFS_PROGRAM, NFS_V3)
            # nfs actions
            nfs3 =NFSv3(host, nfs_port, 3600)
            nfs3.connect()
            lookup_res = nfs3.lookup(root_fh, "file.txt", auth)
            if lookup_res["status"] == NFS3_OK:
                fh = lookup_res["resok"]["object"]["data"]
                write_res = nfs3.write(fh, offset=0, count=11, content="Sample text",
                                       stable_how=DATA_SYNC, auth=auth)
                if write_res["status"] == NFS3_OK:
                    read_res = nfs3.read(fh, offset=0, auth=auth)
                    if read_res["status"] == NFS3_OK:
                        read_content = str(read_res["resok"]["data"], encoding="utf-8")
                        assert read_content.startswith("Sample text")
                else:
                    print("write failed")
            else:
                print("Lookup failed")
        finally:
            if nfs3:
                nfs3.disconnect()
            mount.umnt(mount_path, auth)
            mount.disconnect()
            portmap.disconnect()
    else:
        mount.disconnect()
        portmap.disconnect()

License
-------

**The MIT License (MIT)**

Copyright (c) 2019 `Cooper Yang <https://github.com/CharmingYang0>`__

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
