from flask import Flask, request, redirect, render_template, Blueprint
from RequestFactory import RequestFactory
from RequestsUUIDBuilder import UUIDTools
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import RequestHTTPS
import RequestResolverDAO
app = Flask(__name__, static_url_path='')
factory = RequestFactory(1)
aiidTool = UUIDTools()

# Limiter is here to ensure app doesnt get spammed.
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "50 per hour"]
)

# Fallback route that handles any errors - ensures user doesn't get any default error pages.
@app.route("/fallback", methods=["POST", "GET"])
def fallback():
    url = "https://www.childsplayclothing.com/wo/en"
    if request.method == "POST":
        try:
            code = request.form.get("Code")
            url = RequestResolverDAO.getFrontUrlFromDatabase(code)
            if not url:
                url = "https://www.childsplayclothing.com/wo/en"
        except Exception as e:
            url = "https://www.childsplayclothing.com/wo/en"
        return redirect(url, code=301)
    else:
        return render_template("error.html")

# Redirecter for items. Only difference between this route and the general redirect route is the overall endpoint
# being used. A different endpoint is used to ensure staff do not get confused between the two (i.e item redirect
# is for items and was the original used for redirects, general redirect is for everything else).
@app.route("/item_redirect", methods=["POST", "GET"])
def itemRedirecter():

    # Use the factory to make an IP object. The IP object is then processed using .run() to get the final URL.
    ip = factory.makeIPObj(str(request.remote_addr), str(request.args["product"]))
    ip.run()

    if ip.getFailState() != True:
        return redirect(ip.getFinalUrl(), code=301)

# Redirecter for general links. Only difference between this route and the item redirect route are the links.
@app.route("/general_redirect", methods=["POST", "GET"])
def generalRedirecter():

    ip = factory.makeIPObj(str(request.remote_addr), str(request.args["id"]))
    ip.run()

    if ip.getFailState() != True:
        return redirect(ip.getFinalUrl(), code=301)

# Main error handler if fallback route fails.
@app.route("/error")
@app.errorhandler(500)
def errorPage(e):
    return render_template("error.html")

# Item creation and general creation. Uses different split methods,
# Item creation splits by "style" text, general creation splits by "id" text.
@app.route("/create_item", methods=["POST", "GET"])
@limiter.exempt
def itemCreator():

    if request.method == "GET":
        return render_template("url-generator-item.html", title="Create an item link")

    else:
        if RequestHTTPS.checkUrlForOk(request.form.get("URL")):
            uuid = aiidTool.setArgAndUUIDToDatabase(aiidTool.dissectURLByStyle(request.form.get("URL")))
            returnUrl = "https://redirect.childsplayclothing.co.uk/item_redirect?product=" + str(uuid)

            if uuid is not None:
                return render_template("url-generation.html", title="Create an item link", URLer=returnUrl)
            else:
                return render_template("url-generator-item.html", title="Create an item link", res="URL entered is invalid. Please try again")
        else:
            return render_template("url-generator-item.html", title="Create an item link", res="URL entered is invalid. Please try again")


@app.route("/create_general", methods=["POST", "GET"])
@limiter.exempt
def generalCreator():

    if request.method == "GET":
        return render_template("url-generator-general.html", title="Create a general link")

    else:
        if RequestHTTPS.checkUrlForOk(request.form.get("URL")):
            uuid = aiidTool.setArgAndUUIDToDatabase(aiidTool.dissectURLByRegex(request.form.get("URL")))
            returnUrl = "https://redirect.childsplayclothing.co.uk/general_redirect?id=" + str(uuid)

            if uuid is not None:
                return render_template("url-generation.html", title="Create a general link", URLer=returnUrl)
            else:
                return render_template("url-generator-general.html", title="Create a general link", res="URL entered is invalid. Please try again")
        else:
            return render_template("url-generator-general.html", title="Create a general link", res="URL entered is invalid. Please try again")

# Debugging for pretending to be from an IP address. IP being used here is stored in the header
@app.route("/force_ip", methods=["POST", "GET"])
def force_ip():

    ip = factory.makeIPObj(str(request.args["forced_ip"]), str(request.args["id"]))
    ip.run()

    if ip.getFailState() != True:
        return redirect(ip.getFinalUrl(), code=301)


if __name__ == '__main__':
    app.run()

