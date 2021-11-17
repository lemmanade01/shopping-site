"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """
    # changed "meli" to melon_id
    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # if no cart, render empty cart template
    if "cart" not in session:
        return render_template("cart.html")
    
    # - get the cart dictionary from the session
    cart = session["cart"]

    # initialize empty melon_object and order_total
    melon_objects = []
    order_total = 0
    # order_total = f"${self.price:.2f}"

    # loop over the cart dictionary, and for each melon id:
    for melon_id in cart:
        # returns the cren object from melon_types dict from melons.py read_melon_from_file
        melon = melons.get_by_id(melon_id)
        # get price of melon object
        price = melon.price

        # get melon_id qty in cart
        qty = cart[melon_id]
        print("\n"*10, "*"*10)
        print(qty)
        # calc total price for melon
        melon_cost = price * qty

        # add melon price to total order cost
        order_total += melon_cost

        # add quantity and total cost as attributes on the Melon object
        # won't print to console bc of __repr__
        melon.qty = qty
        melon.melon_cost = melon_cost

        # add updated Melon object to the list created above
        melon_objects.append(melon)
    
    # print("\n"*10, "*"*10)
    # print(cart, melon_objects, order_total)
    # print("\n"*10)

    # - pass the total order cost and the list of Melon objects to the template
    return render_template("cart.html", order_total=order_total, melon_objects=melon_objects)



@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    
    # if cart already exists, set cart var to existing cart
    if 'cart' in session:         
        cart = session['cart']     
    # else create an empty cart
    else:         
        cart = session['cart'] = {}     
          
    # Add melon to cart - either increment the count (if melon already in cart) or add to cart with a count of 1     
    cart[melon_id] = cart.get(melon_id, 0) + 1

    # # if cart key in session, already have cart
    # if "cart" in session:
    #     # if melon already in cart, add one
    #     if melon_id in session["cart"]:
    #         ## not incrementing
    #         session["cart"][melon_id] = session["cart"][melon_id] + 1
    #         print("Add one to melon_id")
    #     # else initialize new melon with value of 1
    #     else:
    #         session["cart"][melon_id] = 1
    # else: 
    #     # if no cart, create cart with melon_id = 1 
    #     session["cart"] = {melon_id: 1}

    flash("Melon added to cart!")
    # redirect the user to the cart page
    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
