from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json

from .models import Product, CartItem, Order, OrderItem


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "core/home.html")


# =========================================================
# MENU
# =========================================================

def menu(request):
    products = Product.objects.all()

    return render(request, "core/menu.html", {
        "products": products
    })


# =========================================================
# CART
# =========================================================

def cart(request):
    cart_items = CartItem.objects.select_related("product").all()

    subtotal = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    # Delivery charge
    delivery = 40

    total = subtotal + delivery if cart_items else 0

    return render(request, "core/cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery": delivery if cart_items else 0,
        "total": total
    })


# =========================================================
# UPDATE CART
# =========================================================

@csrf_exempt
def update_cart(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Invalid request method"
        }, status=400)

    try:
        data = json.loads(request.body)

        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))

        # Validate product ID
        if not product_id:
            return JsonResponse({
                "error": "Product ID is required"
            }, status=400)

        # Quantity cannot be negative
        if quantity < 0:
            return JsonResponse({
                "error": "Quantity cannot be negative"
            }, status=400)

        # Get product
        product = get_object_or_404(Product, id=product_id)

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            product=product
        )

        # -------------------------------------------------
        # REMOVE ITEM
        # -------------------------------------------------

        if quantity == 0:
            cart_item.delete()

            return JsonResponse({
                "status": "deleted",
                "product": product.name,
                "quantity": 0
            })

        # -------------------------------------------------
        # SET QUANTITY
        # -------------------------------------------------

        # IMPORTANT:
        # Set the quantity instead of adding it again.
        #
        # Example:
        # Current quantity = 2
        # New quantity = 3
        # Result = 3
        #
        # NOT:
        # 2 + 3 = 5

        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({
            "status": "success",
            "product": product.name,
            "quantity": cart_item.quantity
        })

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON data"
        }, status=400)

    except ValueError:
        return JsonResponse({
            "error": "Invalid quantity"
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)

# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    # -----------------------------------------------------
    # SHOW CHECKOUT PAGE
    # -----------------------------------------------------

    if request.method == "GET":
        return render(request, "core/checkout.html")


    # -----------------------------------------------------
    # PROCESS ORDER
    # -----------------------------------------------------

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        cart_data = request.POST.get("cart_data")


        # -------------------------------------------------
        # VALIDATE CUSTOMER DETAILS
        # -------------------------------------------------

        if not name or not phone or not address:

            return render(request, "core/checkout.html", {
                "error": "Please fill in all the required fields."
            })


        # -------------------------------------------------
        # CHECK CART DATA
        # -------------------------------------------------

        if not cart_data:

            return render(request, "core/checkout.html", {
                "error": "Your cart is empty."
            })


        # -------------------------------------------------
        # CONVERT JSON TO PYTHON
        # -------------------------------------------------

        try:

            cart = json.loads(cart_data)

        except json.JSONDecodeError:

            return render(request, "core/checkout.html", {
                "error": "Invalid cart data."
            })


        # -------------------------------------------------
        # CHECK EMPTY CART
        # -------------------------------------------------

        if not cart:

            return render(request, "core/checkout.html", {
                "error": "Your cart is empty."
            })


        # -------------------------------------------------
        # CALCULATE SUBTOTAL
        # -------------------------------------------------

        subtotal = 0


        for item in cart:

            product_id = item.get("id")
            quantity = int(item.get("qty", 1))


            if not product_id:
                return render(request, "core/checkout.html", {
                    "error": "Invalid product in cart."
                })


            if quantity <= 0:
                return render(request, "core/checkout.html", {
                    "error": "Invalid product quantity."
                })


            # Get the real product from database
            product = get_object_or_404(
                Product,
                id=product_id
            )


            # Use database price
            subtotal += product.price * quantity


        # -------------------------------------------------
        # DELIVERY
        # -------------------------------------------------

        delivery = 40

        total = subtotal + delivery


        # -------------------------------------------------
        # CREATE ORDER
        # -------------------------------------------------

        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            total=total
        )


        # -------------------------------------------------
        # CREATE ORDER ITEMS
        # -------------------------------------------------

        for item in cart:

            product_id = item.get("id")
            quantity = int(item.get("qty", 1))


            product = get_object_or_404(
                Product,
                id=product_id
            )


            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )


        # -------------------------------------------------
        # DO NOT CLEAR CART HERE
        # -------------------------------------------------
        #
        # The cart must remain until payment succeeds.
        #
        # -------------------------------------------------

        return redirect(
            "payment_page",
            order_id=order.id
        )
# =========================================================
# PAYMENT PAGE
# =========================================================

# =========================================================
# PAYMENT PAGE
# =========================================================

def payment_page(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        # -------------------------------------------------
        # CASH ON DELIVERY
        # -------------------------------------------------

        if payment_method == "COD":

            # COD does not require Razorpay.
            # Mark the order as confirmed.
            order.payment_status = "COD"
            order.save()

            return redirect("success")

        # -------------------------------------------------
        # ONLINE PAYMENT
        # -------------------------------------------------

        elif payment_method == "online":

            return redirect(
                "online_payment",
                order_id=order.id
            )

    return render(request, "core/payment.html", {
        "order": order
    })

# =========================================================
# ONLINE PAYMENT
# =========================================================
# =========================================================
# ONLINE PAYMENT - CREATE RAZORPAY ORDER
# =========================================================

def online_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    # -----------------------------------------------------
    # CREATE RAZORPAY CLIENT
    # -----------------------------------------------------

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # -----------------------------------------------------
    # CREATE RAZORPAY ORDER
    # -----------------------------------------------------

    if not order.razorpay_order_id:

        amount_in_paise = order.total * 100

        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"order_{order.id}",
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

    # -----------------------------------------------------
    # SHOW RAZORPAY CHECKOUT
    # -----------------------------------------------------

    return render(request, "core/online_payment.html", {
        "order": order,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": order.razorpay_order_id,
        "amount": order.total * 100,
    })

# =========================================================
# VERIFY RAZORPAY PAYMENT
# =========================================================

@csrf_exempt
def verify_payment(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=400)

    try:

        data = json.loads(request.body)

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        if not razorpay_order_id:
            return JsonResponse({
                "status": "error",
                "message": "Missing Razorpay order ID"
            }, status=400)

        if not razorpay_payment_id:
            return JsonResponse({
                "status": "error",
                "message": "Missing Razorpay payment ID"
            }, status=400)

        if not razorpay_signature:
            return JsonResponse({
                "status": "error",
                "message": "Missing Razorpay signature"
            }, status=400)

        # -------------------------------------------------
        # FIND OUR ORDER
        # -------------------------------------------------

        order = get_object_or_404(
            Order,
            razorpay_order_id=razorpay_order_id
        )

        # -------------------------------------------------
        # VERIFY SIGNATURE
        # -------------------------------------------------

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        # -------------------------------------------------
        # PAYMENT VERIFIED
        # -------------------------------------------------

        order.razorpay_payment_id = razorpay_payment_id
        order.payment_status = "Paid"
        order.save()

        return JsonResponse({
            "status": "success"
        })

    except razorpay.errors.SignatureVerificationError:

        return JsonResponse({
            "status": "error",
            "message": "Payment verification failed"
        }, status=400)

    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

# =========================================================
# SUCCESS
# =========================================================

def success(request):
    return render(request, "core/success.html")


# =========================================================
# CHATBOT
# =========================================================

# @csrf_exempt
# def chatbot_view(request):
#
#     if request.method == "POST":
#
#         data = json.loads(request.body)
#         message = data.get("message", "").lower()
#
#         reply = chatbot_response(message, request)
#
#         return JsonResponse({
#             "reply": reply
#         })


# def chatbot_response(message, request):
#     pass
