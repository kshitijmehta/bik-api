def product_colour_transformer(data):
    res = []
    for colour_obj in data:
        res.append({
            'colourId': colour_obj['col_id'],
            'code': colour_obj['col_code'],
            'value': colour_obj['col_value']
        })
    return res
