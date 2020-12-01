def admin_user_transformer(data):
    res = []
    for user_obj in data:
        res.append({
            'userId': user_obj['userid'],
            'emailAddress': user_obj['emailid'],
            'mobile': user_obj['mobno'],
            'firstName': user_obj['fname'],
            'lastName': user_obj['lname'],
            'dob': str(user_obj['dob']),
            'gender': user_obj['gender'],
            'discount': user_obj['userdiscount'],
            'addressId': user_obj['addrid'],
            'addressLineOne': user_obj['addrline1'],
            'addressLineTwo': user_obj['addrline2'],
            'addressLineThree': user_obj['addrline3'],
            'city': user_obj['city'],
            'state': user_obj['state'],
            'pincode': user_obj['pincode'],
            'country': user_obj['country'],
        })
    return res
