
# req_data = {
#     'database': 'testing_source', 
#     'schema': 'fcrb', 
#     'table': 'fcrb.episode', 
#     'columns': {
#         'einri': {
#             'selected': False, 
#             'primaryKey': True, 
#             'satellite': None
#         }, 
#         'falnr': {
#             'selected': False, 
#             'primaryKey': True, 
#             'satellite': 'sat_event_episode_type'
#         }, 
#         'bekat': {
#             'selected': True, 
#             'primaryKey': False, 
#             'satellite': 'sat_object_treatment_category'
#         }, 
#         'einzg': {
#             'selected': False, 
#             'primaryKey': False, 
#             'satellite': None
#         }, 
#         'statu': {
#             'selected': True, 
#             'primaryKey': False, 
#             'satellite': 'sat_event_episode_type'
#         }, 
#         'krzan': {
#             'selected': True, 
#             'primaryKey': False, 
#             'satellite': 'sat_event_episode_type'
#         }
#     }
# }

def control_objects_starter(table):
    hubs = {
        'table': table,
        'hubs': []
    }
    satellites = {
        'satellites': []
    }
    links = {
        'links': []
    }
    return [hubs, satellites, links]

def hub_picker(satellite):
    hubs = {
        'time': 'hub_time',
        'person': 'hub_person',
        'object': 'hub_object',
        'location': 'hub_location',
        'event': 'hub_event'
    }

    if 'time' in satellite:
        return hubs['time']
    elif 'person' in satellite:
        return hubs['person']
    elif 'object' in satellite:
        return hubs['object']
    elif 'location' in satellite:
        return hubs['location']
    elif 'event' in satellite:
        return hubs['event']

def hub_generator(hub, keys):
    return {
        'hub': hub,
        'keys': keys
    }

# hubs, links, satellites = control_objects_starter(req_data['table'])

def fill_hubs(hubs, req_data):
    hub_keys = []
    hub_names = []
    for keys, values in req_data['columns'].items():
        if req_data['columns'][keys]['satellite']:
            hub_names.append(hub_picker(req_data['columns'][keys]['satellite']))
            hub_names = list(dict.fromkeys(hub_names))
        if req_data['columns'][keys]['primaryKey']:
            hub_keys.append(keys)

    hubs_finished = []
    for hub in hub_names:
        hubs_finished.append({'hub': hub, 'keys': hub_keys})

    hubs['hubs'] = hubs_finished
    return hubs

# hubs = fill_hubs(hubs, req_data)
    

# print(hubs)
# print(links)
# print(satellites)
