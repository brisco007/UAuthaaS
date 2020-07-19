from biling_and_payment.models import CompteUser

class AuthorizationByAccountingTools :
    @staticmethod
    def isTheUserAuthorized(user_id):
        userAccount = CompteUser.objects.filter(userId = user_id)
        if len(userAccount) != 0:
            return True
        else :
            return False

            