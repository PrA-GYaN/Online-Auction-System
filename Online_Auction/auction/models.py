from django.db import models

# Model for Users who participate in the auction
class Auction_User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    bid_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # User's current bid amount
    status = models.CharField(max_length=50, default="Inactive")  # User's status, e.g., "Active", "Applied"
    
    def __str__(self):
        return self.name

class Admin(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="Inactive")  # Admin's status, e.g., "Active", "Inactive"

    def __str__(self):
        return self.name

# Model for Items being auctioned
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Current highest bid
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    status = models.CharField(max_length=50, default="Active")  # Item's status, e.g., "Active", "Sold"

    def __str__(self):
        return self.name


# Model for Bidders who are participating in the auction
class Bidder(models.Model):
    user = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # Bidder is a user
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Item being bid on
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount the bidder bids
    bid_time = models.DateTimeField(auto_now_add=True)  # Time when the bid was placed

    def __str__(self):
        return f"{self.user.name} bidding on {self.item.name}"


# Model to store auction results
class Result(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # The item being auctioned
    winner = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # The winning user
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)  # The winning bid amount
    auction_date = models.DateTimeField(auto_now_add=True)  # The date and time of the auction result

    def __str__(self):
        return f"Result for {self.item.name} - Winner: {self.winner.name}"


# Model for Payment details related to auctions
class Payment(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)  # Result of the auction
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid by the winner
    payment_date = models.DateTimeField(auto_now_add=True)  # When the payment was made
    status = models.CharField(max_length=50, default="Pending")  # Payment status (Pending, Completed, etc.)

    def __str__(self):
        return f"Payment for {self.result.item.name} by {self.result.winner.name}"


# Model to track member fees (for auction participation, etc.)
class Member_fee(models.Model):
    user = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # The user paying the fee
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the fee
    payment_date = models.DateTimeField(auto_now_add=True)  # Date the fee was paid
    status = models.CharField(max_length=50, default="Paid")  # Payment status (Paid, Pending, etc.)

    def __str__(self):
        return f"Fee for {self.user.name}"


# Model for item categories (to classify items in the auction)
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Model for sub-categories under each category
class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # The parent category
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Model for session dates (could be for auction dates or special event dates)
class Session_date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


# Model for session times (to specify auction time slots)
class Session_Time(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# Model for individual products being auctioned
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Active")  # Product status (e.g., Active, Sold)

    def __str__(self):
        return self.name


# Model for products that have been auctioned off
class Aucted_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # The product that was auctioned
    winner = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # The winner of the auction
    final_price = models.DecimalField(max_digits=10, decimal_places=2)  # The final auction price

    def __str__(self):
        return f"{self.product.name} - Sold to {self.winner.name}"


# Model for participants in the auction (could be users or bidders)
class Participant(models.Model):
    user = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # The participant
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # The item they are participating in
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Their bid amount
    status = models.CharField(max_length=50, default="Pending")  # Participant's status (Pending, Accepted)

    def __str__(self):
        return f"{self.user.name} bidding on {self.item.name}"


# Model for sending feedback about the auction or the system
class Send_Feedback(models.Model):
    user = models.ForeignKey(Auction_User, on_delete=models.CASCADE)  # The user submitting feedback
    feedback = models.TextField()  # The content of the feedback
    date_sent = models.DateTimeField(auto_now_add=True)  # When the feedback was sent

    def __str__(self):
        return f"Feedback from {self.user.name}"


# Model to store the status of auction items
class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name