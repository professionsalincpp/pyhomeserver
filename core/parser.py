import core.protocol as protocol
import pycloudkit as pck
import json
from core.db.sqlitetypes import *



def request_to_set_protocol(request: pck.RequestType) -> protocol.SetDataProtocol:
    """Parse the request and extract the required data"""
    device_id: str = request.params.get("device_id")
    port: int = request.params.get("port")
    source_path: str = request.params.get("source_path")
    data: bytes = request.body

    # Test the all parameters are present
    if device_id is None or port is None or source_path is None or data is None:
        raise ValueError("Missing required parameters")

    # Extract the json from data
    data_json = json.loads(data)

    return protocol.SetDataProtocol(device_id, port, source_path, data_json)





def request_to_get_protocol(request: pck.RequestType) -> protocol.GetDataProtocol:
    """Parse the request and extract the required data"""
    device_id: str = request.params.get("device_id")
    port: int = request.params.get("port")
    source_path: str = request.params.get("source_path")

    # Test the all parameters are present
    if device_id is None or port is None or source_path is None:
        raise ValueError("Missing required parameters")

    return protocol.GetDataProtocol(device_id, port, source_path)





def parse_value_type(value_type: str) -> sqlite3_type:
    """Parse the value type and return the corresponding sqlite3 type"""
    value_type = value_type.lower()

    # Return the corresponding sqlite3 type
    if value_type in ["int", "integer", "number"]:
        return INTEGER
    elif value_type in ["float", "real"]:
        return REAL
    elif value_type in ["string", "text"]:
        return TEXT
    elif value_type in ["bytes", "blob"]:
        return BLOB

    raise ValueError(f"Invalid value type: {value_type}")



    

