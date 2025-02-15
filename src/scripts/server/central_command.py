from .recieve.position_estimate import handle_position_estimate
from .recieve.use_item import handle_use_item

command_to_func = {
    'PE': handle_position_estimate,
    'USE': handle_use_item,
}

def command_center(data: dict):
    '''Recieves data from serial and distributes to recieve logic
    Expects {'command': {PE, USE}, Args: {kwargs}}} 
    '''
    if 'command' in data:
        if data['command'] in command_to_func:
            command_to_func[data['command']](**data['args'])
    
    #LOG error in recieved command
