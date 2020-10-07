
def control_objects_starter(table):
    hubs = {
        'table': table,
        'hubs': []
    }
    links = {
        'links': []
    }
    satellites = {
        'satellites': []
    }
    return [hubs, links, satellites]

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

def hub_base_picker(satellites):
    hub_bases = []
    for satellite in satellites:
        if 'time' in satellite:
            hub_bases.append('time')
        elif 'person' in satellite:
            hub_bases.append('person')
        elif 'object' in satellite:
            hub_bases.append('object')
        elif 'location' in satellite:
            hub_bases.append('location')
        elif 'event' in satellite:
            hub_bases.append('event')
    return hub_bases

def link_picker(satellites):
    satellites = list(dict.fromkeys(satellites))
    possible_links = ['person_time_link', 'person_object_link', 'person_location_link', 'person_event_link', 'object_time_link', 'object_location_link', 'object_event_link', 'time_location_link', 'time_event_link', 'location_event_link']
    probable_links = []
    definite_links = []
    for satellite in satellites:
        probable_links = probable_links + [i for i in possible_links if satellite in i]
    definite_links = [i for i in probable_links if probable_links.count(i) > 1]
    return list(dict.fromkeys(definite_links))

def link_id_picker(link):
    link_ids = {
        'time': 'time_id',
        'person': 'person_id',
        'object': 'object_id',
        'location': 'location_id',
        'event': 'event_id'
    }
    link_names = link.split('_')
    link_names.pop()

    values = {}
    for link_name in link_names:
        values.update({f"{link_name}_id": 0})

    return values

def link_generator(satellites):
    satellites = hub_base_picker(satellites)
    finished_links = []
    if len(satellites) == 1:
        return finished_links
    
    links = link_picker(satellites)
    for link in links:
        finished_link = {
            'link': link,
            'values': link_id_picker(link)
        }
        finished_links.append(finished_link)

    return finished_links


def select_satellite_names(req_data):
    satellite_names = []
    for keys, values in req_data['columns'].items():
        if req_data['columns'][keys]['satellite']:
            satellite_names.append(req_data['columns'][keys]['satellite'])

    satellite_names = list(dict.fromkeys(satellite_names))
    return satellite_names

def fill_satellites(satellite_names, req_data):
    finished_satellites = []
    for satellite_name in satellite_names:
        satellite = {
            'satellite': satellite_name,
            'columns': [],
            'hub': hub_picker(satellite_name),
            'hub_id': 0
        }
        for keys, values in req_data['columns'].items():
            if req_data['columns'][keys]['satellite'] == satellite_name:
                satellite['columns'].append(keys)
        finished_satellites.append(satellite)
    return finished_satellites