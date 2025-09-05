from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import *

class Command(BaseCommand):
    help = "Seed database with sample data for Hotels, Cities, and Amenities"

    def handle(self, *args, **kwargs):
        fake = Faker()

    
        amenities_list = ["Free Wifi", "AC", "Breakfast", "Parking", "Pool", "TV", "24x7 Service"]
        amenities_objs = []
        for name in amenities_list:
            obj = Ameneties.objects.create(amenite_name=name)
            amenities_objs.append(obj)
        owner = HotelVendor.objects.first()
        if not owner:
            owner = HotelVendor.objects.create(username="seed_owner", password="1234")
        
        for _ in range(50):
            hotel = Hotel.objects.create(
                hotel_name=fake.company(),
                hotel_price=random.randint(500, 5000),
                hotel_location=fake.city(),
                hotel_offer_price=random.randint(300, 4000),
                hotel_description=fake.text(max_nb_chars=100),
                hotel_slug=fake.slug() + "-" + str(random.randint(1000, 9999)),
                hotel_owner=owner
        
            )
            hotel.amenities.set(random.sample(amenities_objs, random.randint(2, 4)))

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))
