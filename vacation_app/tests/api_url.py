class APIUrl(object):

    vacations = '/api/vacations/'
    users = '/api/users/'
    mails = '/api/mails/'

    @staticmethod
    def vacations_id(id):
        return APIUrl.vacations + str(id) + '/'

    @staticmethod
    def users_id(id):
        return APIUrl.users + str(id) + '/'

    @staticmethod
    def mails_id(id):
        return APIUrl.mails + str(id) + '/'
