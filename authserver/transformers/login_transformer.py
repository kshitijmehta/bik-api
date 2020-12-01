
def login_transformer(data, email):
    return {
        'userId': data['userid'],
        'emailAddress': email,
        'mobile': data['mobno'],
        'firstName': data['fname'],
        'lastName': data['lname'],
        'dob': str(data['dob']),
        'gender': data['gender'],
        'discount': data['discount'],
        'addressId': data['addrid'],
        'addressLineOne': data['addrline1'],
        'addressLineTwo': data['addrline2'],
        'addressLineThree': data['addrline3'],
        'city': data['city'],
        'state': data['state'],
        'pincode': data['pincode'],
        'country': data['country'],
    }
