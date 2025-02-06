from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, Auction_User, Admin, Category, Sub_Category, Session_date, Session_Time, Product, Bidder
from datetime import datetime

# View for Home page
def Home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

# View to display all auction items
def auction_items(request):
    items = Item.objects.all()

    for item in items:
        max_bid = get_max_bid_for_item(item)
        item.max_bid = max_bid
        item.save()

    return render(request, 'auction_items.html', {'items': items})

# Function to get the maximum bid for an auction item
def get_max_bid_for_item(item):
    # Assuming there is a Bidder model, we should query that model to get the max bid
    max_bid = Bidder.objects.filter(item=item).aggregate(max_bid=Max('bid_amount'))['max_bid']
    return max_bid if max_bid else 0

# View to display a specific auction item and allow placing a bid
def view_auction(request, pid):
    item = Item.objects.get(id=pid)

    if 'email' not in request.session:
        return redirect('login_user')

    user_email = request.session['email']
    user = Auction_User.objects.get(email=user_email)

    # Handling bid placement
    if request.method == 'POST':
        try:
            bid_amount = float(request.POST['bid_amt'])

            # Check if the bid is higher than the current maximum bid
            if bid_amount <= item.max_bid:
                return HttpResponse("Bid amount must be higher than the current maximum bid.")

            user.bid_amt = bid_amount
            user.status = "Bid Placed"
            user.save()

            item.max_bid = bid_amount  # Update the auction item with the new max bid
            item.save()

            return redirect('auction_items')  # Redirect back to the auction items page

        except ValueError:
            return HttpResponse("Invalid bid amount.")  # Handle non-numeric bid input

    return render(request, 'place_bid.html', {'item': item, 'user': user})

# View for placing a bid (you might want to modify this if needed)
def place_bid(request, item_id):
    item = Item.objects.get(id=item_id)

    if 'email' not in request.session:
        return redirect('login_user')

    user_email = request.session['email']
    user = Auction_User.objects.get(email=user_email)

    if request.method == 'POST':
        try:
            bid_amount = float(request.POST['bid_amt'])

            if bid_amount <= item.max_bid:
                return HttpResponse("Bid amount must be higher than the current maximum bid.")

            user.bid_amt = bid_amount
            user.status = "Bid Placed"
            user.save()

            item.max_bid = bid_amount
            item.save()

            return redirect('auction_items')  # Redirect back to the auction items page
        
        except ValueError:
            return HttpResponse("Invalid bid amount.")

    return render(request, 'place_bid.html', {'item': item, 'user': user})

# View for user home (bidder home page)
def Bidder_Home(request):
    return render(request, 'bidder_home.html')

# View for trainer home (auction user home page)
def Auction_User(request):
    return render(request, 'trainer_home.html')

# View for login page for users
def Login_User(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Auction_User.objects.get(email=email)
            if user.password == password:
                request.session['email'] = email
                return redirect('user_home')
            else:
                return HttpResponse("Incorrect password")
        except Auction_User.DoesNotExist:
            return HttpResponse("User not found")

    return render(request, 'login_user.html')

# View for contact page
def Contact(request):
    return render(request, 'contact.html')

# View for about page
def About(request):
    return render(request, 'about.html')

# View for editing user profile
def Edit_Profile(request):
    return render(request, 'edit_profile.html')

# View for editing user profile (alternative view)
def Edit_Profile1(request):
    return render(request, 'edit_profile1.html')

# View for logging out the user
def Logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('login_user')

# View for login page for admin
def Login_Admin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin_user = Admin.objects.get(email=email)
            if admin_user.password == password:
                request.session['email'] = email
                return redirect('admin_home')
            else:
                return HttpResponse("Incorrect password")
        except Admin.DoesNotExist:
            return HttpResponse("Admin not found")

    return render(request, 'login_admin.html')

# View for user signup
def Signup_User(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        new_user = Auction_User(email=email, password=password)
        new_user.save()
        return redirect('login_user')

    return render(request, 'signup_user.html')

# View for changing user password
def Change_Password(request):
    return render(request, 'change_password.html')

# View for changing user password (alternative view)
def Change_Password1(request):
    return render(request, 'change_password1.html')

# View for admin home page
def Admin_Home(request):
    return render(request, 'admin_home.html')

# View for adding new product
def Add_Product(request):
    return render(request, 'add_product.html')

# View for adding new product (alternative view)
def New_product(request):
    return render(request, 'new_product.html')

# View for deleting user
def user_delete(request, id):
    user = Auction_User.objects.get(id=id)
    user.delete()
    return redirect('admin_home')

# View for deleting seller user
def user_delete_seller(request, id):
    user = Auction_User.objects.get(id=id)
    user.delete()
    return redirect('admin_home')

# View for viewing the product details
def product_detail(request, pid):
    item = Item.objects.get(id=pid)
    return render(request, 'product_detail.html', {'item': item})

# View for viewing the product details (alternative view)
def product_detail2(request, pid):
    item = Item.objects.get(id=pid)
    return render(request, 'product_detail2.html', {'item': item})

# View for viewing the auction categories
def view_category(request):
    categories = Category.objects.all()
    return render(request, 'view_category.html', {'categories': categories})

# View for viewing the subcategories
def view_subcategory(request):
    subcategories = Sub_Category.objects.all()
    return render(request, 'view_subcategory.html', {'subcategories': subcategories})

# View for viewing the session dates
def view_session_date(request):
    session_dates = Session_date.objects.all()
    return render(request, 'view_session_date.html', {'session_dates': session_dates})

# View for viewing the session times
def view_session_time(request):
    session_times = Session_Time.objects.all()
    return render(request, 'view_session_time.html', {'session_times': session_times})

# View for adding a new category
def Add_Category(request):
    return render(request, 'add_category.html')

# View for adding a new subcategory
def Add_SubCategory(request):
    return render(request, 'add_subcategory.html')

# View for adding a new session date
def Add_Session_date(request):
    return render(request, 'add_session_date.html')

# View for adding a new session time
def Add_Session_time(request):
    return render(request, 'add_session_time.html')

# View for bidding status
def Bidding_Status(request):
    return render(request, 'bidding_status.html')

# View for bidding status (alternative view)
def Bidding_Status2(request):
    return render(request, 'bidding_status2.html')

# View for editing category
def Edit_Category(request, pid):
    category = Category.objects.get(id=pid)
    return render(request, 'edit_category.html', {'category': category})

# View for editing subcategory
def Edit_SubCategory(request, pid):
    subcategory = Sub_Category.objects.get(id=pid)
    return render(request, 'edit_subcategory.html', {'subcategory': subcategory})

# View for editing session date
def Edit_Session_date(request, pid):
    session_date = Session_date.objects.get(id=pid)
    return render(request, 'edit_session_date.html', {'session_date': session_date})

# View for editing session time
def Edit_Session_time(request, pid):
    session_time = Session_Time.objects.get(id=pid)
    return render(request, 'edit_session_time.html', {'session_time': session_time})

# View for deleting category
def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')

# View for deleting subcategory
def delete_subcategory(request, pid):
    subcategory = Sub_Category.objects.get(id=pid)
    subcategory.delete()
    return redirect('view_subcategory')

# View for deleting session date
def delete_session_date(request, pid):
    session_date = Session_date.objects.get(id=pid)
    session_date.delete()
    return redirect('view_session_date')

# View for deleting session time
def delete_session_time(request, pid):
    session_time = Session_Time.objects.get(id=pid)
    session_time.delete()
    return redirect('view_session_time')

# AJAX view for loading courses (for dynamic loading of courses in dropdowns)
def load_courses(request):
    category_id = request.GET.get('category_id')
    courses = Product.objects.filter(category_id=category_id)
    return render(request, 'load_courses.html', {'courses': courses})

# AJAX view for loading courses (alternative view)
def load_courses1(request):
    subcategory_id = request.GET.get('subcategory_id')
    courses = Product.objects.filter(subcategory_id=subcategory_id)
    return render(request, 'load_courses1.html', {'courses': courses})