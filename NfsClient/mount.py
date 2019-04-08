import struct
import logging
from .rpc import RPC
from .pack import nfs_pro_v3Unpacker
from .const import MOUNT_PROGRAM, MOUNT_V3, MNT3_OK, MOUNTSTAT3

log = logging.getLogger(__package__)


class MountAccessError(Exception):
    pass


class Mount(RPC):
    program = MOUNT_PROGRAM
    program_version = MOUNT_V3

    def null(self, auth=None):
        log.debug("Mount NULL on %s" % self.host)
        super(Mount, self).request(self.program, self.program_version, 0, auth=auth)
        return {"status": MNT3_OK, "message": MOUNTSTAT3[MNT3_OK]}

    def mnt(self, path, auth=None):
        data = struct.pack('!L', len(path))
        data += path.encode()
        data += b'\x00'*((4-len(path) % 4) % 4)

        log.debug("Do mount on %s" % path)
        data = super(Mount, self).request(self.program, self.program_version, 1, data=data, auth=auth)

        unpacker = nfs_pro_v3Unpacker(data)
        return unpacker.unpack_mountres3()

    def umnt(self, path, auth=None):
        data = struct.pack("!L", len(path))
        data += path.encode()
        data += b"\x00" * ((4 - len(path) % 4) % 4)

        log.debug("Do umount on %s" % path)
        super(Mount, self).request(self.program, self.program_version, 3, data=data, auth=auth)

        return {"status": MNT3_OK, "message": MOUNTSTAT3[MNT3_OK]}

    def export(self):
        log.debug("Get mount export on %s" % self.host)
        export = super(Mount, self).request(self.program, self.program_version, 5)

        unpacker = nfs_pro_v3Unpacker(export)
        return unpacker.unpack_exports()
