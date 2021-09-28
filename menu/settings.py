
# service_settings = {'lang': 'en', 'format': 'plain', 'result': 'msg'}

service_settings = {
    'lang': {'code': 'eng', 'desc': 'English'},
    'isTable': {'code': 'false', 'desc': 'plain'},
    'result': {'code': 'message', 'desc': 'message'},
    'update': False,
}


# def set_settings(dataset, key, subkey, value):
#     """
#     func for set settings service
#     """
#     dataset[key][subkey] = value

#     return dataset


# def get_val_settings(dataset, key, subkey):
#     """
#     func for get value of settings service
#     """
#     # return dataset.get(key)
#     return dataset[key][subkey]


def get_default_settings():
    """
    func for get settings service
    """
    return service_settings
