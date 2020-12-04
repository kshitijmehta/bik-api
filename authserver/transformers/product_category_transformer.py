def product_category_transformer(data, is_admin):
    res = []
    for sub_category in data:
        res.append({
            'categoryId': sub_category['ps_id'],
            'categoryName': sub_category['cat_name'],
        })
    if is_admin:
        res.append({
            'categoryId': '0',
            'categoryName': 'Admin',
        })
    return res
