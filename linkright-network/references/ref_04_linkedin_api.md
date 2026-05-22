# ref_04 — LinkedIn API Setup

## Overview

LinkedIn's API allows posting to your profile programmatically via OAuth 2.0 + UGC Posts endpoint.
This enables scheduled posting from linkright-network without manual copy-paste.

**Limitations:**
- Personal profiles require the "Share on LinkedIn" OAuth scope
- Organization pages require additional scopes
- Free developer access: 500 API calls/day, share posts only (no read of feed/connections)
- LinkedIn actively rate-limits and can restrict apps that post at volume

---

## Setup Steps

### Step 1 — Create LinkedIn Developer App

1. Go to: https://developer.linkedin.com/apps
2. Click "Create app"
3. App name: `linkright-personal` (or any name)
4. LinkedIn Page: your company/personal page (required — create one if needed)
5. App logo: upload any image
6. Submit for review

### Step 2 — Request OAuth Scopes

Under "Products" tab in your app:
- Enable: **Share on LinkedIn** — grants `w_member_social` scope

Optional (requires approval):
- **Sign In with LinkedIn** — grants `r_emailaddress`, `r_liteprofile`
- **Marketing Developer Platform** — for org page posting

Note: scope approval can take 1-3 business days.

### Step 3 — Get OAuth Tokens

LinkedIn uses OAuth 2.0 Authorization Code flow.

**Authorization URL:**
```
https://www.linkedin.com/oauth/v2/authorization?
  response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=http://localhost:8080/callback
  &scope=w_member_social
  &state=RANDOM_STRING
```

Run local server to catch callback:
```bash
python3 -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print('CODE:', params.get('code', ['not found'])[0])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Got it. Close this window.')

HTTPServer(('localhost', 8080), H).handle_request()
"
```

**Exchange code for access token:**
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code' \
  -d 'code=AUTH_CODE_FROM_ABOVE' \
  -d 'client_id=YOUR_CLIENT_ID' \
  -d 'client_secret=YOUR_CLIENT_SECRET' \
  -d 'redirect_uri=http://localhost:8080/callback'
```

Response: `{"access_token": "...", "expires_in": 5183944}`

Token expires in ~60 days. Store in `~/.linkright/.env` (not in git).

### Step 4 — Get Your Person URN

```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  'https://api.linkedin.com/v2/userinfo'
```

Returns: `{"sub": "urn:li:person:XXXX"}` — save the `sub` value.

---

## Posting via UGC Posts Endpoint

```bash
curl -X POST 'https://api.linkedin.com/v2/ugcPosts' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'X-Restli-Protocol-Version: 2.0.0' \
  -d '{
    "author": "urn:li:person:YOUR_PERSON_ID",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": "YOUR POST TEXT HERE"
        },
        "shareMediaCategory": "NONE"
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }'
```

Success response: `201 Created` with `id` field = post URN.

---

## Token Storage Format

Add to `~/.linkright/.env` (create if it doesn't exist):
```bash
LINKEDIN_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
LINKEDIN_PERSON_URN=urn:li:person:XXXX
LINKEDIN_EXPIRES_AT=YYYY-MM-DD
```

**NEVER commit this file.** Add to `.gitignore` if linkright-memory is a git repo.

---

## Rate Limits

| Limit | Value |
|---|---|
| Posts per day | 150 (practical limit is much lower before throttle) |
| API calls per day | 500 (free tier) |
| Token lifetime | ~60 days, then re-authorize |

---

## Refresh Flow

LinkedIn does not issue refresh tokens for the Share on LinkedIn scope.
When token expires: re-run Step 3 above to get a new access token.

---

## linkright-network Integration

The `linkedin_post.py` script reads from `~/.linkright/.env` (default `--token-file`).
It looks for `LINKEDIN_ACCESS_TOKEN=<value>`. Setup is manual (one-time OAuth flow above).
After setup, posting is automated via: `python3 linkedin_post.py --text '<post>' --confirm`

If the token is missing or expired:
```bash
python3 linkedin_post.py --text 'test' --dry-run
# FileNotFoundError: Token file not found → re-run Step 3 above
```
