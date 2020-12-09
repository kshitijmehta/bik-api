def product_list_customer_transformer(data):
    res = []
    for product_obj in data:
        res.append({
            'productId': product_obj['prodid'],
            'productCategoryName': product_obj['prodcategory'],
            'name': product_obj['prodname'],
            'description': product_obj['proddesc'],
            'priceINR': str(product_obj['inrprice']),
            'priceUSD': str(product_obj['usdprice']),
            'colour': product_obj['colour'],
            'size': product_obj['size'],
            'imagePaths': product_obj['prodimgpath'],
            'imageNames': product_obj['prodimgname'],
            'productDetailId': str(product_obj['proddetailid'].split(",")[0]),
            'subCategoryName': product_obj['prodsubcategory']
        })
    return res
