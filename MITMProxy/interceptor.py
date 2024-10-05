from logger import Logger
from mitmproxy import http, ctx
import json


DOMAIN_INDEX = 0

WILD_CARD_ADDRESSES = [
    'https://*.pscp.tv',
    'https://*.video.pscp.tv',
    'https://*.tw.img.com',
    'wss://*.pscp.tv',
    'https://*.giphy.com'
]


RELEVANT_DOMAINS = [
    'https://api.x.ai/3',
    'https://api.x.ai',                         # 200 with no data coming back, content-type header set to 'application/grpc' with grpc-status header set to 12
    'https://api.x.com',
    'https://api.twitter.com',
    'https://api.x.com',
    'https://api-stream.twitter.com',
    'https://api-stream.x.com',
    'https://ads-api.twitter.com',
    'https://ads-api.x.com',
    'https://aa.twitter.com',
    'https://aa.x.com',
    'https://caps.twitter.com',
    'https://caps.x.com',
    'https://pay.twitter.com',                  # Request gets cancelled
    'https://pay.x.com',                        # 302 to "https://pay.twitter.com"
    'https://sentry.io',                        # 302 with same path, not url just path
    'https://ton.twitter.com',                  # 400 with 'access-control-expose-headers' set to 'Content-Length,x-ton-expected-size'
    'https://ton.x.com',                        # 302 to "https://ton.twitter.com"
    'https://ton-staging.atla.twitter.com',     # 502
    'https://ton-staging.atla.x.com',           # SSL/TLS handshake error (  << OpenSSL Error([('SSL routines', '', 'sslv3 alert handshake failure')])  )
    'https://ton-staging.pdxa.twitter.com',     # 502
    'https://ton-staging.pdxa.x.com',           # SSL/TLS handshake error (  << OpenSSL Error([('SSL routines', '', 'sslv3 alert handshake failure')])  )
    'https://twitter.com',                      # 401
    'https://x.com',                            # 302 to "https://twitter.com"
    'https://upload.twitter.com',               # 404
    'https://upload.x.com',                     # 302 to "https://upload.twitter.com"
    'https://www.google-analytics.com',         # 404
    'https://accounts.google.com/gsi/status',   # 404
    'https://accounts.google.com/gsi/log',      # 404
    'https://checkoutshopper-live.adyen.com',   # 404
    'https://vmap.snappytv.com',                # 502
    'https://vmapstage.snappytv.com',           # 502
    'https://vmaprel.snappytv.com',             # 502
    'https://vmap.grabyo.com',                  # 403 with returming html page talks about 'CloudFront'
    'https://dhdsnappytv-vh.akamaihd.net',      # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://pdhdsnappytv-vh.akamaihd.net',     # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mdhdsnappytv-vh.akamaihd.net',     # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mdhdsnappytv-vh.akamaihd.net',     # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mpdhdsnappytv-vh.akamaihd.net',    # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mmdhdsnappytv-vh.akamaihd.net',    # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mdhdsnappytv-vh.akamaihd.net',     # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://mpdhdsnappytv-vh.akam',            # 502
    'https://mmdhdsnappytv-vh.akamaihd.net',    # 400 with Server header set to 'AkamaiGHost' and returns an html that says requested url is invalid
    'https://dwo3ckksxlb0v.cloudfront.net',     # 400 with html response saying invalid auth and invalid arguments
    'https://media.riffsy.com',                 # 404 with Server header set to 'sffe'
    'https://media.tenor.com',                  # 404 with Server header set to 'sffe'
    'https://c.tenor.com',                      # 404 with Server header set to 'sffe'
    'https://ads-twitter.com',                  # 502
    'https://analytics.twitter.com',            # 404
    'https://analytics.x.com.aihd.net'          # SSL/TLS handshake error (  << OpenSSL Error([('SSL routines', '', 'tlsv1 alert internal error')])  )
]


BASE_TASK_JSON_URL = "https://api.twitter.com/1.1/onboarding/task.json"

TWITTER_PUBLIC_KEY = "2CB16598-CB82-4CF7-B332-5990DB66F3AB"
TWITTER_PUBLIC_DEV_KEY = "DF58DD3B-DFCC-4502-91FA-EDC0DC385CFF"
TWITTER_PUBLIC_TRANSPARENT_KEY = "4CB8C8B0-40FF-439C-9D0D-9A389ADA18CB"
TWITTER_PUBLIC_TRANSPARENT_DEV_KEY = "6627C16B-DA60-47A5-85F7-CFF23BD2BE69",

TRANSACTION_ID = "f63a8fee6817f38e"

TASK_JSON_HEADERS = [(b'date', b'Thu, 28 Dec 2023 20:44:42 GMT'), (b'perf', b'7469935968'), (b'pragma', b'no-cache'), (b'server', b'tsa_o'), (b'expires', b'Tue, 31 Mar 1981 05:00:00 GMT'), (b'content-type', b'application/json; charset=utf-8'), (b'cache-control', b'no-cache, no-store, must-revalidate, pre-check=0, post-check=0'), (b'last-modified', b'Thu, 28 Dec 2023 20:44:43 GMT'), (b'content-length', b'100'), (b'x-frame-options', b'SAMEORIGIN'), (b'content-encoding', b'gzip'), (b'x-transaction-id', b'bbc2c81999d50f70'), (b'x-xss-protection', b'0'), (b'x-rate-limit-limit', b'187'), (b'x-rate-limit-reset', b'1703797167'), (b'content-disposition', b'attachment; filename=json.json'), (b'x-content-type-options', b'nosniff'), (b'x-rate-limit-remaining', b'185'), (b'strict-transport-security', b'max-age=631138519'), (b'access-control-allow-origin', b'https://twitter.com'), (b'access-control-allow-credentials', b'true'), (b'access-control-expose-headers', b'X-Twitter-Spotify-Access-Token,X-Twitter-Client-Version,X-Twitter-Diffy-Request-Key,X-Rate-Limit-Limit,X-TD-Mtime,X-Twitter-Client,Backoff-Policy,X-Rate-Limit-Remaining,Content-Length,X-Rate-Limit-Reset,X-Transaction-Id,X-Acted-As-User-Id,X-Twitter-Polling,X-Twitter-UTCOffset,X-Response-Time'), (b'x-response-time', b'138'), (b'x-connection-hash', b'68c9c0f6f83d42b0580d0d06779cfe2c9412619cebcff200ae31bb6135665f89')]


class Interceptor:

    def __init__(self):
        self.logger = Logger()
        self.is_task_json_handled = False
        self.new_task_json_url = BASE_TASK_JSON_URL.replace("api.twitter.com/1.1", RELEVANT_DOMAINS[DOMAIN_INDEX][8:])
        ctx.log.info(f"NEW TASK JSON URL: {self.new_task_json_url}")

    def request(self, flow: http.HTTPFlow) -> None:
        if "client-api.arkoselabs.com" in flow.request.url:
            flow.request.url = flow.request.url.replace("client-api", "roblox-api")
        flow.request.url = flow.request.url.replace(TWITTER_PUBLIC_KEY, TWITTER_PUBLIC_TRANSPARENT_KEY)
        flow.request.url = flow.request.url.replace("arkose_challenge_signup_web_prod", "arkose_challenge_transparent_signup_prod")
        flow.request.url = flow.request.url.replace("arkose_challenge_signup_mobile_prod", "arkose_challenge_transparent_signup_prod")
        if flow.request.method == "POST":
            flow.request.text = flow.request.text.replace(TWITTER_PUBLIC_KEY, TWITTER_PUBLIC_TRANSPARENT_KEY)
            flow.request.text = flow.request.text.replace("arkose_challenge_signup_web_prod", "arkose_challenge_transparent_signup_prod")
            flow.request.text = flow.request.text.replace("arkose_challenge_signup_mobile_prod", "arkose_challenge_transparent_signup_prod")

        if flow.request.url == BASE_TASK_JSON_URL and not self.is_task_json_handled and flow.request.method == "POST":
            flow.request.url = flow.request.url.replace("api.twitter.com/1.1", RELEVANT_DOMAINS[DOMAIN_INDEX][8:])

    def response(self, flow: http.HTTPFlow) -> None:
        if self.is_arkose_condition(flow.request.url):
            new_response_content = self.process_arkose_response(flow)
            if new_response_content:
                flow.response.content = new_response_content

        # if flow.request.url.startswith("https://abs.twimg.com/responsive-web/client-web-legacy/main") and flow.request.url.endswith("js") and flow.request.method == "GET":
        #    flow.response.content = flow.response.text.replace(',u.send(e.data)', ',console.log(e);u.send(e.data)').encode("utf-8")

        if flow.request.url == "https://iframe.arkoselabs.com/2CB16598-CB82-4CF7-B332-5990DB66F3AB/index.html?theme=default":
            with open("enfo.html") as doc:
                data = doc.read()
            flow.request.text = data

        if flow.request.url == self.new_task_json_url and not self.is_task_json_handled and flow.request.method == "POST":
            ctx.log.info("\n------===------\n\n\ntask.json response received\n\n\n------===------")

            for header in flow.response.headers:
                if header == "grpc-status":
                    ctx.log.info(f"\n====\n\n\ngrpc-status: {flow.response.headers['grpc-status']}\n\n\n===")
                del flow.response.headers[header]
            for header in TASK_JSON_HEADERS:
                flow.response.headers[header[0].decode()] = header[1].decode()
            # flow.response.headers["access-control-allow-origin"] = "*"

            new_response_text = generate_verification_tasks_json_response(flow.request.text)
            compressed_content = new_response_text.encode("utf-8")
            flow.response.content = compressed_content
            # flow.response.text = new_response_text
            # flow.response.status_code = 200

            flow.request.url = BASE_TASK_JSON_URL
            self.is_task_json_handled = True

        self.logger.log_flow(flow)

    def process_arkose_response(self, flow: http.HTTPFlow):
        try:
            json_content = json.loads(flow.response.text)
            if json_content.get("response") == "answered":
                json_content['solved'] = True
                content = json.dumps(json_content, separators=(",", ":")).encode('utf-8')
                return content
        except ValueError as e:
            ctx.log.warn(f"Error processing Arkose response from {flow.request.url}\nError: {str(e)[:200]}.\nDue to error, flow content not changed.")
            return flow.response.content

    def is_arkose_condition(self, url: str) -> bool:
        return 'arkose' in url and url.endswith(('fc/a/', 'fc/c/', 'fc/ac/', 'fc/ca/'))


def generate_verification_tasks_json_response(request_body_string):
    request_body = json.loads(request_body_string)
    flow_token = request_body["flow_token"][1:]
    name = request_body["subtask_inputs"][0]["sign_up"]["name"]
    email = request_body["subtask_inputs"][0]["sign_up"]["email"]
    username = f"{name}9" + '3915'

    def endpoint_template(name):
        return f'callback.json?product=metric-tracking&identifier=generic-metric-tracking-cb&params=%7B%22data%22%3A%5B%7B%22dataset%22%3A%22signup_events%22%2C%22signup_event_data%22%3A%7B%22subtask_id%22%3A%22{name}%22%2C%22flow_token%22%3A%22g%3B{"%3A".join(flow_token.split(":"))}%3A4%22%2C%22flow_name%22%3A%22signup%22%2C%22flow_start_location%22%3A%22manual_link%22%2C%22signup_flow_name%22%3A%22signup%22%7D%7D%5D%7D'
    privacy_options_endpoint = endpoint_template("PrivacyOptions")
    enter_password_endpoint = endpoint_template("EnterPassword")

    new_response_body = {
        "flow_token": 'g' + flow_token[:-1] + '4',
        "status": "success",
        "subtasks": [
            {
                "subtask_id": "EnterPassword", "callbacks": [
                    {"trigger": "impression", "endpoint": enter_password_endpoint},
                    {"trigger": "impression", "scribe_config": {"page": "onboarding",
                                                                "section": "signup", "component": "EnterPassword", "action": "impression"}}
                ],
                "enter_password": {
                    "primary_text": {"text": "You'll need a password", "entities": []},
                    "next_link": {"link_type": "task", "link_id": "next_link", "label": "Next"},
                    "secondary_text": {"text": "Make sure it’s 8 characters or more.", "entities": []},
                    "hint": "Password",
                    "name": name,
                    "username": username,
                    "email": email
                },
                "progress_indication":
                    {"text": {"text": "Step 5 of 5", "entities": []}}
            },
            {
                "subtask_id": "PrivacyOptions", "callbacks": [
                    {"trigger": "impression", "endpoint": privacy_options_endpoint},
                    {"trigger": "impression", "scribe_config": {"page": "onboarding",
                                                                "section": "signup", "component": "PrivacyOptions", "action": "impression"}}
                ],
                "privacy_options": {
                    "primary_text": "Privacy options",
                    "secondary_text": "Privacy",
                    "discoverable_by_email": True,
                    "discoverable_by_email_label": "Let others find me by my email address",
                    "discoverable_by_email_detail_text": {"text": "People who have your email address will be able to connect with you on X.", "entities": []},
                    "discoverable_by_phone": True,
                    "discoverable_by_phone_label": "Let others find me by my phone number",
                    "discoverable_by_phone_detail_text": {"text": "People who have your phone number will be able to connect with you on X.", "entities": []},
                    "next_link": {"link_type": "subtask", "link_id": "next_link", "label": "Done", "subtask_id": "EnterPassword"}
                }
            }
        ]
    }
    return json.dumps(new_response_body, separators=(',', ':'))


addons = [Interceptor()]
