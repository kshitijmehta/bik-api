def product_quick_list_transformer(data):
    res = []
    for product_obj in data:
        res.append({
            'productId': str(product_obj['prodid']),
            'productCategoryName': product_obj['prod_categ_name'],
            'name': product_obj['prodname'],
            'priceINR': str(product_obj['prodinrprice']),
            'priceUSD': str(product_obj['produsdprice']),
            'imagePaths': product_obj['prodimgpath'],
            'imageNames': product_obj['prodimgname'],
            'productDetailId': str(product_obj['productdetailid'])
        })
    return res


def product_trending_latest_list(data):
    res = []
    for product_obj in data:

        res.append({
            'productId': str(product_obj['prod_id']),
            'productCategoryName': product_obj['prod_categ_name'],
            'name': product_obj['prod_name'],
            'priceINR': str(product_obj['prod_inr_price']),
            'priceUSD': str(product_obj['prod_usd_price']),
            'imagePaths': product_obj['prod_img_path'],
            'imageNames': product_obj['prod_img_name'],
            'productDetailId': str(product_obj['productdetailid'])
        })
    return res