def load_config():
    try:
        with open('utils/config.ini') as cfg:
            lines = cfg.readlines()
            open_folder_status = eval(lines[0].split('=')[1])
            tolerence = int(lines[1].split('=')[1])
        return open_folder_status,tolerence
    except FileNotFoundError:
        return (False,4)

def write_config(open_folder_status,tolerence):
    open_folder = 'open_folder={}\n'.format(open_folder_status)
    tolerence = 'freq={}'.format(tolerence)
    lines = [open_folder,tolerence]
    with open('utils/config.ini','w') as cfg:
        cfg.writelines(lines)
    return True