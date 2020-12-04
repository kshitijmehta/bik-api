def product_list_transformer(data):
    res = []
    for size_obj in data:
        res.append({
            'productId': size_obj['prodid'],
            'productCategoryName': size_obj['prodcategory'],
            'name': size_obj['prodname'],
            'description': size_obj['proddesc'],
            'latest': size_obj['latest'],
            'trending': size_obj['trending'],
            'quantity': size_obj['qty']
        })
    return res


def single_product_transformer(data):
    res = []
    for size_obj in data:
        res.append({
            'productId': size_obj['prodid'],
            'productCategoryName': size_obj['prodcategory'],
            'name': size_obj['prodname'],
            'description': size_obj['proddesc'],
            'priceINR': str(size_obj['inrprice']),
            'priceUSD': str(size_obj['usdprice']),
            'colour': size_obj['colour'],
            'size': size_obj['size'],
            'quantity': size_obj['qty'],
            'subCategory': size_obj['subcategoryid'],
            'sizeId': size_obj['sizeid'],
            'colourId': size_obj['colourid'],
            'imageNames': size_obj['imagename'],
            'imagePaths': size_obj['imagepath'],
            'productDetailId': size_obj['proddetailid']
        })
    return res