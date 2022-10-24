import os

import pytest

from common.secret import SecretManager

EMAIL_DOMAIN = "kingpin.global"
MONGODB_CONNECTION_STRING = "mongodb+srv://devUser:ghzATDgDhDHcZvFP@dev.arg3n.mongodb.net/kingpin?retryWrites=true&w=majority"
LOGIN_ADMIN = "aserkilov@kingpin.global"
PASSWORD_ADMIN = SecretManager().get_password("password.admin")
LOGIN_RETAILER = "arsenserkilov@kingpin.global"
PASSWORD_RETAILER = SecretManager().get_password("password.retailer")
LOGIN_BRAND = "aserkilovbrand@kingpin.global"
PASSWORD_BRAND = SecretManager().get_password("password.brand")
COLLECTIONS_PATH = os.path.join(os.path.dirname(__file__), "../test_data/collections")
MAIN_COLLECTION_PATH = f"{COLLECTIONS_PATH}/main-collection.csv"
IMAGES_PATH = os.path.join(os.path.dirname(__file__), "../test_data/images")
MAIN_COLLECTION_IMAGE_PATH = f"{IMAGES_PATH}/main-collection.jpg"