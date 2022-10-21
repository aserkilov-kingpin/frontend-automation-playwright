from common.secret import SecretManager

EMAIL_DOMAIN = "kingpin.global"
MONGODB_CONNECTION_STRING = "mongodb+srv://devUser:ghzATDgDhDHcZvFP@dev.arg3n.mongodb.net/kingpin?retryWrites=true&w=majority"
LOGIN_ADMIN = "aserkilov@kingpin.global"
PASSWORD_ADMIN = SecretManager().get_password("password.admin")
LOGIN_RETAILER = "arsenserkilov@kingpin.global"
PASSWORD_RETAILER = SecretManager().get_password("password.retailer")
LOGIN_BRAND = "aserkilovbrand@kingpin.global"
PASSWORD_BRAND = SecretManager().get_password("password.brand")
