from apiclient.discovery import build
from google.oauth2 import service_account
import apiclient
import httplib2


class MerchantsCenterClient:
    SCOPES = ['https://www.googleapis.com/auth/content']
    # SERVICE_ACCOUNT_FILE = 'C:/Users/Fede/Documents/Chimola/content-api-key.json'
    SERVICE_ACCOUNT_FILE = 'C:/Users/Fede/Documents/Chimola/Chimola-6e058f9ab064.json'

    def __init__(self, merchant_id):

        def build_request(http, *args, **kwargs):
            new_http = httplib2.Http()
            return apiclient.http.HttpRequest(new_http, *args, **kwargs)

        credentials = service_account.Credentials.from_service_account_file(
            MerchantsCenterClient.SERVICE_ACCOUNT_FILE,
            scopes=MerchantsCenterClient.SCOPES
        )

        self._service = build(
            'content',
            'v2',
            requestBuilder=build_request,
            credentials=credentials
        )
        self._merchant_id = merchant_id

    @property
    def service(self):
        return self._service

    @property
    def merchant_id(self):
        return self._merchant_id

    def send(self, product_feed):
        req = self.service.products().insert(
            merchantId=self.merchant_id, body=dict(product_feed))
        result = req.execute()
        print('Product "%s" with id=%s was sent'.format(
            result['title'], result['id']))
