import pycloudkit as pck
import core.utils as utils
import core.config as config
import core.parser as parser
import core.protocol as protocol
import core.db.resourcesdatabase as rdb
import core.db.devicesdatabase as ddb
import asyncio

# Set up the server
ip: str = utils.get_local_ip()
port: int = config.port

# Create a new Async server
server = pck.AsyncServer(ip, port)
resources = rdb.ResourceDatabase('db/resources.db')
devices = ddb.DevicesDatabase('db/devices.db')

@server.route('/')
async def main_page(request: pck.RequestType) -> pck.ResponseType:
    """Handle the main page request."""
    with open('frontend/html/index.html', 'r') as f: 
        return pck.ResponseType(status_code=200, body=f.read(), headers={'Content-Type': 'text/html'})
    
@server.route('/api/setresource', pck.HTTPMethod.POST)
async def set_resource(request: pck.RequestType) -> pck.ResponseType:
    """Handle the set resource request."""
    _protocol: protocol.SetDataProtocol = parser.request_to_set_protocol(request)
    # Perform the set resource operation
    return utils.perform_set_data_protocol(resources, devices, _protocol)

@server.route('/api/getresource')
async def get_resource(request: pck.RequestType) -> pck.ResponseType:
    """Handle the get resource request."""
    _protocol: protocol.GetDataProtocol = parser.request_to_get_protocol(request)
    # Perform the get resource operation
    return utils.perform_get_data_protocol(resources, _protocol)

@server.route('any')
async def any_route(request: pck.RequestType) -> pck.ResponseType:
    """Handle any route request."""
    # Try to open the requested file
    try:
        with open(f'frontend/{request.path}', 'r') as f: 
            content_type: str = utils.get_file_content_type(request.path)
            return pck.ResponseType(status_code=200, body=f.read(), headers={'Content-Type': content_type})
    except FileNotFoundError:
        return pck.ResponseType(status_code=404, body='File not found', headers={'Content-Type': 'text/html'})

def main():
    # Register the server with the cloud
    asyncio.run(server.start())

if __name__ == '__main__':
    main()

