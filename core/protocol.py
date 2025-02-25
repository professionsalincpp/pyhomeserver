import dataclasses
from core.servertypes import *


@dataclasses.dataclass
class SetDataProtocol:
    """Protocol for setting data."""
    device_id: DeviceId
    port: Port
    source_path: str
    data: JSON
    @property
    def source_id(self):
        """Source id property"""
        return SourceId(SourceTag(self.device_id, self.port), self.source_path)

    @property
    def source_tag(self):
        """Source tag property"""
        return SourceTag(self.device_id, self.port)

    



@dataclasses.dataclass
class GetDataProtocol:
    """Protocol for getting data."""
    device_id: DeviceId
    port: Port
    source_path: str
    @property
    def source_id(self):
        """Source id property"""
        return SourceId(SourceTag(self.device_id, self.port), self.source_path)

    

    @property
    def source_tag(self):
        """Source tag property"""
        return SourceTag(self.device_id, self.port)

    





    



    

