import dataclasses
import json
from core.tags import *


class DeviceId(str):
    """Device ID."""
    pass



class Port(int):
    """Port number."""
    pass



class JSON(dict):
    """JSON object."""
    def stringify(self):
        return json.dumps(self)

    @staticmethod
    def loads(obj) -> "JSON":
        json_obj: JSON = JSON(json.loads(obj))
        return json_obj



@dataclasses.dataclass
class SourceTag:
    """Tag for identifying the source"""
    device_id: DeviceId
    port: Port
    def to_string(self):
        return tostringsourcetag(self.device_id, self.port)

    

    @staticmethod
    def from_string(tag_string: str) -> "SourceTag":
        device_id, port = fromstringsourcetag(tag_string)
        return SourceTag(device_id, port)



@dataclasses.dataclass
class SourceId:
    """Source ID."""
    source_tag: SourceTag
    path: str
    def to_string(self):
        return tostringsourceid(self.source_tag.device_id, self.source_tag.port, self.path)

    @staticmethod
    def from_string(source_id_string: str) -> "SourceId":
        device_id, port, path = fromstringsourceid(source_id_string)
        source_tag = SourceTag(DeviceId(device_id), Port(port))

        return SourceId(source_tag, path)





