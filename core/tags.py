def tostringsourcetag(device_id: str, port: int) -> str:
    return f"@{device_id}:{port}"

def fromstringsourcetag(tag_string: str) -> tuple[str, int]:
    device_id, port = tag_string.lstrip("@").split(":")

    return device_id, int(port)



def tostringsourceid(device_id: str, port: int, source_path: str) -> str:
    return f"@{device_id}:{port}/{source_path}"



def fromstringsourceid(id_string: str) -> tuple[str, int, str]:
    source_tag, source_path = id_string.split("/")
    device_id, port = fromstringsourcetag(source_tag)

    return device_id, int(port), source_path



