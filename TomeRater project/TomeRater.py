import re
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("The update of the email was sucessfull. The new address is: {address}".format(address=self.email))

    def __repr__(self):
        return "User name: {name} \nEmail address: {address} \nbooks read: {number}".format(name=self.name, address=self.email, number=len(self.books))

    def __eq__(self, other_user):
        return(self.name == other_user.name and self.email == other_user.email)

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        all_ratings = 0
        for book_rating in self.books.values():
            if book_rating == None:
                continue
            all_ratings += book_rating
        try:
            average = all_ratings / len(self.books)
        except ZeroDivisionError:
            return 0
        return average


class Book(object):

    def __init__(self, title, isbn, prize=0):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.prize = prize

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_prize(self):
        return self.prize

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The isbn was successfully updated to: {isbn}".format(isbn=self.isbn))

    def add_rating(self, rating):
        if 0 <= int(rating) <= 4:
            self.ratings.append(rating)
        else:
            print("Rating Invalid")

    def eq(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True

    def get_average_rating(self):
        all_book_ratings = 0
        for book_rating in self.ratings:
            if book_rating == None:
                continue
            all_book_ratings += int(book_rating)
        try:
            average = all_book_ratings / len(self.ratings)
        except ZeroDivisionError:
            return 0
        return average

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, prize=0):
        super().__init__(title, isbn, prize)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{book} by {author}".format(book=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, prize=0):
        super().__init__(title, isbn, prize)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on{subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "This is a Tome Rater object."

    def __eq__(self, other):
        return(self.users == other.user and self.books == other.books)

    def create_book(self, title, isbn, prize=0):
        if self.check_isbn(isbn):
            return
        book = Book(title, isbn, prize)
        self.books[book] = 0
        return book

    def create_novel(self, title, author, isbn, prize=0):
        if self.check_isbn(isbn):
            return
        new_fiction = Fiction(title, author, isbn, prize)
        self.books[new_fiction] = 0
        return new_fiction

    def create_non_fiction(self, title, subject, level, isbn, prize=0):
        if self.check_isbn(isbn):
            return
        new_non_fiction = Non_Fiction(title, subject, level, isbn, prize)
        self.books[new_non_fiction] = 0
        return new_non_fiction

    def check_isbn(self, isbn):
        for book in self.books.keys():
            if book.isbn == isbn:
                print("There is already a book existing with the same ISBN({x}). Please try again".format(x=isbn))
                return True

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print("No user with email: {email}".format(email= email))
        else:
            self.users[email].read_book(book, rating)
            if rating:
                book.add_rating(rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        #Checks that the email is not yet existing
        if email in self.users.keys():
            print("A user with this email is already existing")
            return
        #Checks that the email provided fits to the requireed format.
        pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not re.match(pattern, email):
            print("This is not a regular email address. Please try it again.")
            return
        self.users[email] = User(name, email)
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)
        return self.users[email]

    #Analyis
    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users:
            print(user)

    def most_read_book(self):
        maxbook = max(self.books, key= self.books.get)
        return "The most read book is: {x}".format(x=maxbook.get_title())

    def get_n_most_read_books(self, n):
        if len(self.books) == 0:
            print("Not a single book is listed. Please add books first and come back later.")
            return
        elif n > len(self.books):
            print("The list of books is only {length} books long. So if you ask for the top {n} books, this doesnt work.".format(length=len(self.books), n=n))
            return
        else:
            sorted_books = sorted(self.books, key=self.books.get, reverse=True)[:n]
            ranking = 1
            for book in sorted_books:
                print("The number {rank} most read book is: {book}, which was read {amount} times.".format(rank=ranking, book=book.title, amount=self.books[book]))
                ranking += 1
            return sorted_books

    def highest_rated_book(self):
        bookdict = {}
        for book in self.books.keys():
            bookdict[book] = book.get_average_rating()
        maxbook = max(bookdict, key=bookdict.get)
        return "The highest rated book is: {x}".format(x=maxbook.get_title())

    def most_positive_user(self):
        userdict = {}
        for user in self.users.values():
            userdict[user.name] = user.get_average_rating()
        maxuser = max(userdict, key=userdict.get)
        return "The most positive user is: {x}".format(x=maxuser)

    def get_n_most_expensive_books(self, n):
        if len(self.books) == 0:
            print("Not a single book is listed. Please add books first and come back later.")
            return
        elif n > len(self.books):
            print(
                "The list of books is only {length} books long. So if you ask for the top {n} books, this doesnt work.".format(
                    length=len(self.books), n=n))
            return
        else:
            prizedict = {}
            for book in self.books.keys():
                prizedict[book] = book.get_prize()
            sorted_prize_dict = sorted(prizedict, key=prizedict.get, reverse=True)[:n]
            ranking = 1
            for book in sorted_prize_dict:
                print("The number {number} most expensive book is {bookname} with a prize of {prize}".format(number= ranking, bookname=book.title, prize=book.prize))
                ranking += 1
            return sorted_prize_dict


#testing
#Tome_Rater = TomeRater()
#book1 = Tome_Rater.create_book("book1", 123, 23)
#book2 = Tome_Rater.create_book("book2", 123456789, 12)
#book3 = Tome_Rater.create_book("book3", 987654321, 34)
#book4 = Tome_Rater.create_book("book4", 123, 23)
#user1 = Tome_Rater.add_user("user1", "user1@email.com", [book1, book2, book3])
#user2 = Tome_Rater.add_user("user2", "user2@email.com", [book2])
#user3 = Tome_Rater.add_user("user3", "alles@alles", [book1])

#print(Tome_Rater.testbook())#test
#booka = Tome_Rater.create_book("booka", 1234567, 55)
#bookb = Tome_Rater.create_book("bookb", 12345678, 78)
#print(Tome_Rater.testbook())#test
#novela = Tome_Rater.create_novel("novela", "novelwriter", 12345, 2)

#nonfictiona = Tome_Rater.create_non_fiction("nonfictiona", "nonfictionsubject", "advanced", 1234, 90)

#Tome_Rater.add_book_to_user(booka, "user1@email.com", 3)

#print(Tome_Rater.books)
#print(Tome_Rater.users)
#Tome_Rater.print_catalog()
#Tome_Rater.print_users()
#print(Tome_Rater.most_read_book())
#print(Tome_Rater.most_positive_user())

#print(Tome_Rater.highest_rated_book())

#Tome_Rater.get_n_most_read_books(7)
#Tome_Rater.get_n_most_expensive_books(3)

