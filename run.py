from flask import Flask, request, session, redirect, url_for
import urllib
import requests
 
app = Flask(__name__)
app.secret_key = 'iwonttellyou'
 
redirect_uri = 'http://74ab9cc.ngrok.com/callback'
client_id = '669297741475-6nhd955cc71kqoe88qse2qdad4bb1hn0.apps.googleusercontent.com'  # get from https://code.google.com/apis/console
client_secret = 'xpopv_Q9UGJFGanuNj3iki2f'
 
auth_uri = 'https://accounts.google.com/o/oauth2/auth'
token_uri = 'https://accounts.google.com/o/oauth2/token'
scope = ('https://www.googleapis.com/auth/userinfo.profile',
         'https://www.googleapis.com/auth/userinfo.email')
profile_uri = 'https://www.googleapis.com/oauth2/v1/userinfo'
 
 
@app.route('/')
def index():
    if 'email' not in session:
        return 'Please <a href="/login">login</a>'
    else:
        return ('Hello <b>{}</b>.'
                '<a href="/logout">logout</a>').format(session['email'])
 
 
@app.route('/logout')
def logout():
    session.pop('email', '')
    return redirect(url_for('index'))
 
 
@app.route('/login')
def login():
    # Step 1
    params = dict(response_type='code',
                  scope=' '.join(scope),
                  client_id=client_id,
                  approval_prompt='force',  # or 'auto'
                  redirect_uri=redirect_uri)
    url = auth_uri + '?' + urllib.parse.urlencode(params)
    return redirect(url)
 
 
@app.route('/callback')
def callback():
    if 'code' in request.args:
        # Step 2
        code = request.args.get('code')
        data = dict(code=code,
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    grant_type='authorization_code')
        r = requests.post(token_uri, data=data)
        # Step 3
        access_token = r.json()['access_token']
        r = requests.get(profile_uri, params={'access_token': access_token})
        session['email'] = r.json()['email']
        return redirect(url_for('index'))
    else:
        return 'ERROR'



@app.route('/getalbum')
def getalbum():
    url ="https://picasaweb.google.com/data/feed/api/user/default"
    rs =requests.get(url)
    return rs
 
if __name__ == '__main__':
    app.run(debug=False)