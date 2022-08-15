# Generate fake users and posts for testing purposes
from turtle import title
from faker import Faker
from users.models import CustomUser
from blog.models import Post
import random

# Generate five random users
def users(count=5):
    fake = Faker()
    
    i = 0
    while i < count:
        # Create Random Users
        try:
            CustomUser.objects.create_user(username=fake.user_name(), email=fake.email(), 
                                            password='password', confirmed=True)
            i += 1
        except Exception as e:
            print(e)
    
    return True
            
# Create Random Posts for Users
def random_posts(count=20):
    fake = Faker()
    # Get list of all users and their corresponding pk
    persons = CustomUser.objects.all()
    users_list = list(persons)
    
    # Generate random posts for users
    for i in range(count):
        p = Post.objects.create(title=fake.sentence(nb_words=5), content=fake.text(),
                                author=random.choice(users_list))
        p.save()     
        
    return True  


 
        