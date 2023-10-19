from __future__ import print_function
from daqhats import hat_list, HatError

def select_hat_device(filter_by_id):
    selected_hat_address = None
    hats = hat_list(filter_by_id=filter_by_id)
    number_of_hats = len(hats)
    if number_of_hats < 1:
        raise HatError(0, 'Error: No HAT devices found')
    elif number_of_hats == 1:
        selected_hat_address = hats[0].address
    else:
        for hat in hats:
            print('Address ', hat.address, ': ', hat.product_name, sep='')
        print('')
        address = int(input('Select the address of the HAT device to use: '))
        for hat in hats:
            if address == hat.address:
                selected_hat_address = address
                break
    if selected_hat_address is None:
        raise ValueError('Error: Invalid HAT selection')
    return selected_hat_address


def enum_mask_to_string(enum_type, bit_mask):
    item_names = []
    if bit_mask == 0:
        item_names.append('DEFAULT')
    for item in enum_type:
        if item & bit_mask:
            item_names.append(item.name)
    return ', '.join(item_names)


def chan_list_to_mask(chan_list):
    chan_mask = 0
    for chan in chan_list:
        chan_mask |= 0x01 << chan
    return chan_mask


def validate_channels(channel_set, number_of_channels):
    valid_chans = range(number_of_channels)
    if not channel_set.issubset(valid_chans):
        raise ValueError('Error: Invalid channel selected - must be '
                         '{} - {}'.format(min(valid_chans), max(valid_chans)))
