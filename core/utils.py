from core.parser import parse_value_type
from core.protocol import *
from core.constants import FILE_EXTENSIONS_CONTENT_TYPE
from core.db.resourcesdatabase import ResourceDatabase
from core.db.devicesdatabase import DevicesDatabase
from core.db.sqlitetypes import *
import socket
import pycloudkit as pck


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]



def get_file_extension(path: str) -> str:
    return path.split('.')[-1]


def get_file_content_type(path: str) -> str:
    return FILE_EXTENSIONS_CONTENT_TYPE.get(get_file_extension(path), 'text/html')



def perform_protocol(protocol: SetDataProtocol | GetDataProtocol) -> pck.ResponseType:
    if isinstance(protocol, SetDataProtocol):
        return protocol.perform()
    elif isinstance(protocol, GetDataProtocol):
        return protocol.perform()
    else:
        raise ValueError("Invalid protocol")

    

def perform_set_data_protocol(resdb: ResourceDatabase, devdb: DevicesDatabase, protocol: SetDataProtocol) -> pck.ResponseType:
    """
    Perform the necessary database operations to set the data
    

    Parameters:
    resdb (ResourceDatabase): The database to store the data in
    protocol (SetDataProtocol): The protocol containing the data to set

    
    Returns:
    pck.ResponseType: The response to send back to the client
    """

    source_id: SourceId = protocol.source_id
    value = protocol.data.get('value')
    value_type: sqlite3_type = parse_value_type(protocol.data.get('type'))
    if value is None:
        raise ValueError("Missing required data field 'value'")

    
    if value_type == INTEGER:
        value = int(value)
    elif value_type == REAL:
        value = float(value)
    elif value_type == TEXT:
        value = str(value)
    elif value_type == BLOB:
        value = bytes(value, 'utf-8')
    else:
        raise ValueError("Invalid value type")

    devdb.add_device_source(source_id.source_tag, source_id.path, value_type)
    result = resdb.store(source_id, value)

    if not result:
        return pck.ResponseType(status_code=500, headers={}, body='Failed to set data')

    return pck.ResponseType(status_code=200, headers={}, body='Data set successfully')



def perform_get_data_protocol(db: ResourceDatabase, protocol: GetDataProtocol) -> pck.ResponseType:

    # Perform the necessary database operations to get the data

    # ...

    source_id: SourceId = protocol.source_id
    value = db.retrieve(source_id)

    return pck.ResponseType(status_code=200, headers={}, body=str(value))



def format_tag(source_tag: SourceTag) -> str:
    return f"{source_tag.device_id}_{source_tag.port}"

