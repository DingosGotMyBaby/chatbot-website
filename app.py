import os
from generator import generateforout
from flask import Flask, redirect, url_for, render_template
from flask_caching import Cache
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

app.secret_key = "" # Insert your random string here
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # DEV ONLY

app.config["DISCORD_CLIENT_ID"] = 1234  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "string"  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://localhost:5000/callback/"  # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = ""  # Required to access BOT resources.

# caching
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

cache = Cache(app)
discord = DiscordOAuth2Session(app)

# Index route
@app.route('/')
@cache.cached()
def index():
    return render_template("index.html")


@app.route('/privacy')
@cache.cached(timeout=1200)
def privacy():
    return render_template('privacy.html')


@app.route('/login')
def login():
    scope = ['identify', 'guilds']
    return discord.create_session(scope)


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route('/callback/')
def callback():
    discord.callback()

    found = False
    guild_check = discord.fetch_guilds()
    for guild in guild_check:
        if guild.id == 123456: # Checks if user is part of a guild
            found = True
            break

    if found is False:
        raise Unauthorized
    return redirect(url_for(".chatbot"))


@app.route('/chatbot')
@requires_authorization
@cache.cached(timeout=30)
def chatbot():
    out = generateforout()
    return render_template('chatbot.html', out=out)


## Redirect to main page cause effort
@app.route('/chatbot/')
@requires_authorization
def chatbotslash():
    return redirect(url_for(".chatbot"))


## Hidden URL for allowed people has removed from public release
## Admins know what the link is


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run()
