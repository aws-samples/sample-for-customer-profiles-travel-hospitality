import random
import string
import re
from datetime import datetime, date, timedelta
from faker import Faker
fake = Faker('en_US')

def generateHotelData():
    loyaltyObj = generateHotelLoyaltyData()
    prefObj = generateHotelPreferencesData(loyaltyObj)
    booking = generateHotelBookingData(loyaltyObj)
    stayRevenue = []
    for b in booking:
        stayRevenue.extend(generateStayRevenueData(b))
    return {
        "Loyalty": loyaltyObj,
        "Preferences": prefObj,
        "Booking": booking,
        "StayRevenue": stayRevenue
    }

def get_random_hotel_tiers(loyalty_tiers, loyalty_points):
    current_tier = random.choice(loyalty_tiers)
    try:
        current_tier_index = loyalty_tiers.index(current_tier)
        if current_tier_index < len(loyalty_tiers) - 1:
            next_tier = loyalty_tiers[current_tier_index + 1]
            if current_tier_index == 0:
                current_tier_points = random.randint(100, loyalty_points[current_tier_index])
            else:
                current_tier_points = random.randint(loyalty_points[current_tier_index]+1, loyalty_points[current_tier_index+1])
            next_tier_points = loyalty_points[current_tier_index+1] - current_tier_points
        else:
            current_tier_points = random.randint(loyalty_points[current_tier_index], 15000)
            next_tier_points = 0
            next_tier = ""
    except ValueError:
        next_tier = None
    return current_tier, next_tier, current_tier_points, next_tier_points

def generateHotelLoyaltyData():
    loyalty_levels = ["Bronze", "Silver", "Gold", "Platinum"]
    loyalty_points = [1000, 3000, 5000, 10000]
    current_loyalty, next_loyalty, current_points, next_level_points = get_random_hotel_tiers(loyalty_levels, loyalty_points)
    loyaltyID = "H"+str(random.randrange(11111111, 99999999, 8))
    
    gender = random.choice(['M', 'F']).upper()
    firstName = fake.first_name_male() if gender == 'M' else fake.first_name_female()
    middleName = random.choice(string.ascii_letters).upper()
    lastName = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=71).strftime("%m/%d/%Y")
    email = fake.safe_email()
    phoneNumber = re.sub(r'\D+', '', fake.phone_number().split("x")[0])
    
    loyaltyObj = {
        "LoyaltyId": loyaltyID,
        "FirstName": firstName,
        "LastName": lastName,
        "MiddleName": middleName,
        "Gender": gender,
        "BirthDate": dob,
        "Email": email,
        "PhoneNumber": phoneNumber,
        "PhoneCountryCode": "+1",
        "AccountStatus": "ACTIVE",
        "AccountType": random.choice(['PERSONAL', 'CORPORATE']),
        "AddressLine1": fake.street_address(),
        "AddressLine2": fake.secondary_address() if random.choice([True, False]) else "",
        "AddressLine3": "",
        "AddressLine4": "",
        "City": fake.city(),
        "State": fake.state_abbr(),
        "PostalCode": fake.postcode(),
        "CountryCode": "US",
        "LastUpdated": datetime.now().isoformat() + 'Z',
        "CreatedDate": datetime.now().isoformat() + 'Z',
        "ProgramId": "HOTEL_REWARDS",
        "ProgramName": "Hotel Rewards Program",
        "CurrentStatusLevelDescription": current_loyalty,
        "NextStatusLevelDescription": next_loyalty,
        "PointsUnit": "points",
        "PointsBalance": current_points,
        "PointsToNextLevel": next_level_points,
        "EnrollDate": fake.date_time_between(start_date="-5y", end_date='-1y').isoformat() + 'Z',
        "LifetimePoints": random.randint(5000, 50000)
    }
    return loyaltyObj

def generateHotelPreferencesData(loyaltyObj):
    preferences = {
        "LoyaltyId": loyaltyObj['LoyaltyId'],
        "PreferenceId": fake.uuid4(),
        "PreferenceName": "Standard Hotel Preferences",
        "SmokingPreference": random.choice(['Non-Smoking', 'Smoking']),
        "CleaningTime": random.choice(['Morning', 'Afternoon', 'Evening']),
        "CheckInType": random.choice(['Standard', 'Early', 'Mobile']),
        "CheckOutType": random.choice(['Standard', 'Late', 'Express']),
        "RoomFloor": random.choice(['Low', 'High', 'Middle']),
        "ElevatorProximity": random.choice(['Near', 'Far']),
        "QuietZone": random.choice(['true', 'false']),
        "RoomView": random.choice(['City', 'Ocean', 'Garden', 'Pool']),
        "RoomType": random.choice(['Standard', 'Suite', 'Executive']),
        "BedType": random.choice(['King', 'Queen', 'Double']),
        "MattressType": random.choice(['Firm', 'Soft', 'Medium']),
        "PillowType": random.choice(['Down', 'Synthetic', 'Memory Foam']),
        "NumberOfPillows": random.randint(2, 6),
        "Language": "EN",
        "EmailLanguage": "EN",
        "CarRentalVendor": random.choice(['Hertz', 'Avis', 'Enterprise']),
        "VehicleType": random.choice(['Compact', 'Mid-size', 'Full-size', 'SUV']),
        "MealType": random.choice(['Continental', 'American', 'Vegetarian']),
        "FavoriteCuisine": random.choice(['Italian', 'Asian', 'American', 'Mediterranean']),
        "Beverage": random.choice(['Coffee', 'Tea', 'Water', 'Juice']),
        "DietaryRestriction": random.choice(['None', 'Vegetarian', 'Vegan', 'Gluten-Free']),
        "AllergyInfo": random.choice(['None', 'Nuts', 'Dairy', 'Shellfish']),
        "LoyaltyProgramName": loyaltyObj['ProgramName'],
        "LoyaltyMembershipId": loyaltyObj['LoyaltyId'],
        "Wheelchair": random.choice(['true', 'false']),
        "DisabilityType": random.choice(['None', 'Mobility', 'Visual', 'Hearing']),
        "SupportAnimal": random.choice(['true', 'false']),
        "BathroomAccessibility": random.choice(['Standard', 'Roll-in Shower', 'Grab Bars']),
        "MarketingOptIn": random.choice(['true', 'false']),
        "MarketingChannelType": random.choice(['Email', 'SMS', 'Mail']),
        "MarketingFrequency": random.choice(['Weekly', 'Monthly', 'Quarterly']),
        "ContactDetailEmail": loyaltyObj['Email'],
        "ContactDetailPhone": loyaltyObj['PhoneNumber'],
        "ContactDetailCommunicationMethod": random.choice(['Email', 'Phone', 'SMS']),
        "PaymentMethodName": random.choice(['Visa', 'MasterCard', 'American Express']),
        "PaymentMethodType": "Credit Card",
        "PetType": random.choice(['None', 'Dog', 'Cat']),
        "SpecialRequestType": random.choice(['None', 'Anniversary', 'Birthday', 'Business']),
        "SpecialRequestName": random.choice(['Flowers', 'Champagne', 'Cake', 'None']),
        "InterestName": random.choice(['Spa', 'Fitness', 'Business Center', 'Pool']),
        "ReferenceId": loyaltyObj['LoyaltyId'],
        "ReferenceType": "profile",
        "Status": "Active",
        "StartDate": datetime.now().isoformat() + 'Z',
        "EndDate": (datetime.now() + timedelta(days=365)).isoformat() + 'Z',
        "CreatedDate": datetime.now().isoformat() + 'Z',
        "CreatedBy": "system",
        "UpdatedDate": datetime.now().isoformat() + 'Z',
        "UpdatedBy": "system"
    }
    return preferences

def generateHotelBookingData(loyaltyObj):
    hotel_brands = ['Sunlight Hotels', 'Moonrise Resorts', 'Evergreen Lodging', 'Coastal Inns', 'Mountain View Hotels', 
                'Starlight Suites', 'Oasis Stays', 'Crystal Palace Hotels', 'Royal Crown Resorts', 'Emerald Bay Inns']
    hotel_codes = ['SUN001', 'MON002', 'EVE003', 'COA004', 'MVH005', 
                  'STR006', 'OAS007', 'CRY008', 'RCR009', 'EBI010']    
    room_types = ['Standard King', 'Standard Queen', 'Suite', 'Executive Room']
    
    bookings = []
    noOfBookings = random.randint(3, 10)
    
    for index in range(noOfBookings):
        checkInDate = fake.date_between(start_date="-30d", end_date='+90d')
        numberOfNights = random.randint(1, 7)
        checkOutDate = checkInDate + timedelta(days=numberOfNights)
        
        current_date = date.today()
        
        if current_date > checkOutDate:
            status = random.choice(['Completed', 'Cancelled'])
        elif current_date >= checkInDate:
            status = random.choice(['Checked In', 'Cancelled'])
        else:
            status = random.choice(['Confirmed', 'Cancelled'])
        
        brandCode = random.choice(hotel_brands)
        hotelCode = random.choice(hotel_codes)
        roomType = random.choice(room_types)
        amountPerNight = random.randint(150, 500)
        
        booking = {
        "LoyaltyId": loyaltyObj['LoyaltyId'],
        "ReservationId": fake.uuid4(),
        "ConfirmationNumber": fake.license_plate().replace(" ","").replace("-",""),
        "FirstName": loyaltyObj['FirstName'],
        "MiddleName": loyaltyObj['MiddleName'],
        "LastName": loyaltyObj['LastName'],
        "Email": loyaltyObj['Email'],
        "PhoneNumber": loyaltyObj['PhoneNumber'],
        "Status": status,
        "TripType": random.choice(['Business', 'Leisure']),
        "BrandCode": brandCode,
        "HotelCode": hotelCode,
        "GroupId": fake.uuid4() if random.choice([True, False]) else "",
        "TransactionId": fake.uuid4(),
        "CreatedDate": fake.date_time_between(start_date="-60d", end_date='-30d').isoformat() + 'Z',
        "CreatedBy": "user",
        "UpdatedDate": datetime.now().isoformat() + 'Z',
        "UpdatedBy": "system",
        "ProcessedDate": datetime.now().isoformat() + 'Z',
        "CheckInDate": checkInDate.isoformat(),
        "CheckOutDate": checkOutDate.isoformat(),
        "EarlyCheckIn": random.choice(['true', 'false']),
        "LateCheckIn": random.choice(['true', 'false']),
        "EarlyCheckOut": random.choice(['true', 'false']),
        "LateCheckOut": random.choice(['true', 'false']),
        "DigitalKey": random.choice(['true', 'false']),
        "RoomKeys": random.randint(1, 4),
        "RoomTypeCode": roomType.replace(" ", "").upper(),
        "RoomTypeName": roomType,
        "RoomNumber": str(random.randint(100, 999)),
        "RoomCapacity": random.randint(2, 6),
        "SmokingAllowed": random.choice(['true', 'false']),
        "AccessibilityType": random.choice(['None', 'Wheelchair', 'Hearing', 'Visual']),
        "NumberOfNights": numberOfNights,
        "NumberOfGuests": random.randint(1, 4),
        "AdultGuests": random.randint(1, 3),
        "ChildGuests": random.randint(0, 2),
        "AmountPerNight": amountPerNight,
        "TotalAmountBeforeTax": amountPerNight * numberOfNights,
        "TotalAmountAfterTax": round((amountPerNight * numberOfNights) * 1.12, 2),
        "CurrencyCode": "USD",
        "CurrencyName": "US Dollar",
        "CurrencySymbol": "$",
        "PaymentType": random.choice(['Credit Card', 'Debit Card', 'Cash']),
        "CreditCardType": random.choice(['Visa', 'MasterCard', 'American Express']),
        "CreditCardToken": fake.credit_card_number(),
        "NameOnCreditCard": f"{loyaltyObj['FirstName']} {loyaltyObj['LastName']}",
        "DiscountCode": fake.lexify(text='????').upper() if random.choice([True, False]) else "",
        "DiscountPercent": random.randint(0, 20) if random.choice([True, False]) else 0,
        "LoyaltyProgramName": loyaltyObj['ProgramName'],
        "LoyaltyTier": loyaltyObj['CurrentStatusLevelDescription'],
        "RatePlanCode": random.choice(['BAR', 'ADV', 'CORP', 'GOV']),
        "RatePlanName": random.choice(['Best Available Rate', 'Advance Purchase', 'Corporate', 'Government']),
        "RatePlanDescription": "Standard hotel rate plan",
        "CreationChannelId": random.choice(['Web', 'Mobile', 'Phone', 'Walk-in']),
        "BookingMethod": random.choice(['Online', 'Phone', 'In-Person']),
        "Refundable": random.choice(['true', 'false']),
        "CancellationCharge": random.randint(0, 50) if random.choice([True, False]) else 0,
        "CancellationReason": random.choice(['Guest Request', 'No Show', 'Weather']) if status == 'Cancelled' else "",
        "CancellationComment": fake.sentence() if status == 'Cancelled' else "",
        "AdditionalNote": fake.sentence() if random.choice([True, False]) else "",
        "PreferenceRef": fake.uuid4(),
        "SameDayRate": random.choice(['true', 'false']),
        "Reserver": f"{loyaltyObj['FirstName']} {loyaltyObj['LastName']}"
        }
        bookings.append(booking)
    return bookings

def generateStayRevenueData(booking):
    revenue_items = []
    
    # Only generate revenue items for completed bookings
    if booking['Status'] != 'Completed':
        return revenue_items
    
    # Calculate tax per night
    total_tax = round(booking['TotalAmountAfterTax'] - booking['TotalAmountBeforeTax'], 2)
    tax_per_night = round(total_tax / booking['NumberOfNights'], 2)
    
    # Generate Room Rate and Taxes for each night
    for night in range(booking['NumberOfNights']):
        night_date = datetime.fromisoformat(booking['CheckInDate']) + timedelta(days=night)
        
        # Room Rate entry
        revenue_item = {
            "StayRevenueId": fake.uuid4(),
            "ReservationId": booking['ReservationId'],
            "GuestId": booking['LoyaltyId'],
            "HotelCode": booking['HotelCode'],
            "StartDate": night_date.isoformat(),
            "RevenueType": 'Room Rate',
            "RevenueDescription": 'Nightly room charge',
            "RevenueAmount": str(booking['AmountPerNight']),
            "CurrencyCode": booking['CurrencyCode'],
            "CurrencyName": booking['CurrencyName'],
            "CurrencySymbol": booking['CurrencySymbol'],
            "ProcessedDate": booking['ProcessedDate'],
            "RevenueStatus": "Posted" if booking['Status'] == 'Completed' else "Pending",
            "CreatedDate": booking['CreatedDate'],
            "CreatedBy": booking['CreatedBy'],
            "UpdatedDate": booking['UpdatedDate'],
            "UpdatedBy": booking['UpdatedBy']
        }
        revenue_items.append(revenue_item)
        
        # Taxes entry for this night
        revenue_item = {
            "StayRevenueId": fake.uuid4(),
            "ReservationId": booking['ReservationId'],
            "GuestId": booking['LoyaltyId'],
            "HotelCode": booking['HotelCode'],
            "StartDate": night_date.isoformat(),
            "RevenueType": 'Taxes',
            "RevenueDescription": 'Local and state taxes',
            "RevenueAmount": str(tax_per_night),
            "CurrencyCode": booking['CurrencyCode'],
            "CurrencyName": booking['CurrencyName'],
            "CurrencySymbol": booking['CurrencySymbol'],
            "ProcessedDate": booking['ProcessedDate'],
            "RevenueStatus": "Posted" if booking['Status'] == 'Completed' else "Pending",
            "CreatedDate": booking['CreatedDate'],
            "CreatedBy": booking['CreatedBy'],
            "UpdatedDate": booking['UpdatedDate'],
            "UpdatedBy": booking['UpdatedBy']
        }
        revenue_items.append(revenue_item)
    
    # Optional revenue items
    optional_types = [
        {'type': 'Parking', 'description': 'Daily parking fee'},
        {'type': 'Incidentals', 'description': 'Room service and minibar'},
        {'type': 'Store Purchase', 'description': 'Hotel store purchases'},
        {'type': 'Bar', 'description': 'Lobbty Bar'},
        {'type': 'Restaurant', 'description': 'Dinning at Restaurant'},
        {'type': 'Laundry', 'description': 'Laundry services'}
    ]
        
    # Randomly select 1-4 optional items
    num_optional_items = random.randint(1, 4)
    selected_optional = random.sample(optional_types, num_optional_items)
        
    for revenue_type in selected_optional:
        revenue_item = {
            "StayRevenueId": fake.uuid4(),
            "ReservationId": booking['ReservationId'],
            "GuestId": booking['LoyaltyId'],
            "HotelCode": booking['HotelCode'],
            "StartDate": booking['CheckInDate'],
            "RevenueType": revenue_type['type'],
            "RevenueDescription": revenue_type['description'],
            "RevenueAmount": str(round(random.uniform(10.0, 100.0), 2)),
            "CurrencyCode": booking['CurrencyCode'],
            "CurrencyName": booking['CurrencyName'],
            "CurrencySymbol": booking['CurrencySymbol'],
            "ProcessedDate": booking['ProcessedDate'],
            "RevenueStatus": "Posted",
            "CreatedDate": booking['CreatedDate'],
            "CreatedBy": booking['CreatedBy'],
            "UpdatedDate": booking['UpdatedDate'],
            "UpdatedBy": booking['UpdatedBy']
        }
        revenue_items.append(revenue_item)
    
    return revenue_items