def shipment_transformer(data):
    res = []
    for shipment_obj in data:
        res.append({
            'shipperId': shipment_obj['shipr_id'],
            'shipperName': shipment_obj['shipr_name'],
            'trackingLink': shipment_obj['shipr_link']
        })
    return res
