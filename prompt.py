import json
import requests

url = 'http://127.0.0.1:8000/alexa/ask/'
payload = {
  "session": {
    "sessionId": "SessionId.76d60893-e489-4888-bd99-e45ea7f4d264",
    "application": {
      "applicationId": "amzn1.ask.skill.e54c5b30-3545-4d27-8a0a-72eaa0c479fa"
    },
    "attributes": {
      "launched": "true"
    },
    "user": {
      "userId": "amzn1.ask.account.AE33HOWEPDXXSW46VJHVYU7ZDUR7BSWV4MKPRY7455QT5RBYKFLQERMIBRMN672WA6WKHWXYH4IREYHFZ2MJFZWVD6N35NUQ5DNETI6IZE6OLJOIGBP4AUN336KMJ77T23TTU5XKQQUVZRG7YMHQ4EMAERJGT2I4KCMGLFHWBLOBELVP4KC6EIXGQ7RBSI4ZEIJZ6QBGHHPLQKA"
    },
    "new": "false"
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.b59e1164-82f5-4e10-82fa-676afbdd67c7",
    "locale": "en-GB",
    "timestamp": "2017-04-25T16:18:59Z",
    "intent": {
      "name": "showImg",
      "slots": {
        "num": {
          "name": "num",
          "value": "0"
        }
      }
    }
  },
  "version": "1.0"
}


headers = {'Content-Type' : 'application/json;charset=UTF-8',
			'Host' : 'ovh.de',
			'Content-Length' : '',
			'Accept' : 'application/json',
			'Accept-Charset' : 'utf-8',
			'Signature' : '',
			'SignatureCertChainUrl' : 'https://s3.amazonaws.com/echo.api/echo-api-cert.pem',
			}

response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
