from pyNfsClient import Portmap, Mount, NFSv3, MNT3_OK, NFS_PROGRAM, NFS_V3, NFS3_OK, DATA_SYNC
from random import random, randint
from time import sleep
import sys

# variable preparation
host = sys.argv[1]
mount_path = "/"

auth = {"flavor": 1,
        "machine_name": "host1",
        "uid": 0,
        "gid": 0,
        "aux_gid": list(),
        }

parent_a = f"DiR_{random()}"
print("Dir A name: {}".format(parent_a))
parent_b = f"DiR_{random()}"
print("Dir B name: {}".format(parent_b))
child_dir = f"DiR_{random()}"
print("Child Dir name: {}".format(child_dir))
fixed_xid = int(f"{randint(0,4294967295):010d}")
print("Fixed XID: {} ({})".format(fixed_xid, hex(fixed_xid)))

# portmap initialization
portmap = Portmap(host, timeout=3600)
portmap.connect()

# mount initialization
mnt_port = portmap.getport(Mount.program, Mount.program_version)
mount = Mount(host=host, port=mnt_port, timeout=3600, auth=auth)
mount.connect()

mnt_res =mount.mnt(mount_path, auth)
if mnt_res["status"] == MNT3_OK:
    root_fh = mnt_res["mountinfo"]["fhandle"]
    try:
        nfs_port = portmap.getport(NFS_PROGRAM, NFS_V3)
        # nfs actions
        nfs3 = NFSv3(host, nfs_port, 3600, auth=auth)
        nfs3.connect()
        # mkdir /A
        mkdir_a_res = nfs3.mkdir(dir_handle=root_fh, dir_name=parent_a)
        lookup_dir_a_res = nfs3.lookup(root_fh, parent_a)
        dir_a_handle = lookup_dir_a_res["resok"]["object"]["data"]
        # mkdir /B
        mkdir_b_res = nfs3.mkdir(dir_handle=root_fh, dir_name=parent_b)
        lookup_dir_b_res = nfs3.lookup(root_fh, parent_b)
        dir_b_handle = lookup_dir_b_res["resok"]["object"]["data"]
        # mkdir /A/C
        mkdir_child_a_res = nfs3.mkdir(dir_handle=dir_a_handle, dir_name=child_dir, xid=fixed_xid)
        # mkdir /B/C
        mkdir_child_b_res = nfs3.mkdir(dir_handle=dir_b_handle, dir_name=child_dir, xid=fixed_xid)
        print(f"mkdir status: {mkdir_child_b_res['status']}")
        lookup_child_b_res = nfs3.lookup(dir_b_handle, child_dir)
        # directory should exist
        if lookup_child_b_res["status"] == NFS3_OK:
            print("Dir B was found - PASS")
        else:
            print("Dir B is missing - FAIL")
    finally:
        if nfs3:
            nfs3.disconnect()
        mount.umnt()
        mount.disconnect()
        portmap.disconnect()
else:
    mount.disconnect()
    portmap.disconnect()
