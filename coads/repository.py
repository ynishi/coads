from dataclasses import dataclass
import google.ads.google_ads.client
import boto3


@dataclass
class Token:
    developer_token: str = 'DEVELOPER'
    client_id: str = 'CLIENT'
    client_secret: str = 'SECRET'
    refresh_token: str = 'REFRESH'


@dataclass
class TokenRepository:
    host: str = ''

    def get_token(self, cid) -> Token:
        host = self.host
        return Token()


@dataclass
class ClientFactory:
    host: str = ''

    def get_client(self, token: Token) -> google.ads.google_ads.client.GoogleAdsClient:
        host = self.host
        if host == '':
            return None
        if token == Token():
            return None
        return (google.ads.google_ads.client.GoogleAdsClient
                .load_from_dict(token))


@dataclass
class ConversionS3Repository:
    s3 = None

    def connect(self):
        self.s3 = boto3.client('s3')

    def put_dict(self, bucket: str, cid: str, data: str):
        self.s3.put_object(
            self.config['bucketname'], cid, data)
