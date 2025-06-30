import random
import string
import re
import pandas as pd

from datetime import datetime, date, time, timedelta
from faker import Faker
fake = Faker('en_US')


def generateData():
    loyaltyObj = generateLoyaltyData()
    prefObj = generatePreferencesData(loyaltyObj)
    booking = generateBookingData(loyaltyObj)
    return {
        "Loyalty": loyaltyObj,
        "Preferences": prefObj,
        "Booking": booking
    }

def get_random_loyalty_tiers(loyalty_tiers, loyalty_points):
    
    current_tier = random.choice(loyalty_tiers)

    try:
        # Find the index of the current tier in the list
        current_tier_index = loyalty_tiers.index(current_tier)
        
        # The next tier is the element at the next index, if it exists
        if current_tier_index < len(loyalty_tiers) - 1:
            next_tier = loyalty_tiers[current_tier_index + 1]
            if current_tier_index == 0:
                current_tier_points = random.randint(100, loyalty_points[current_tier_index])
            else:
                current_tier_points = random.randint(loyalty_points[current_tier_index]+1, loyalty_points[current_tier_index+1])
            next_tier_points = loyalty_points[current_tier_index+1] - current_tier_points
        else:
            # If the current tier is the highest, there is no next tier
            current_tier_points = random.randint(loyalty_points[current_tier_index], 15000)
            next_tier_points = 0
            next_tier = ""
    except ValueError:
        # Handle cases where the randomly selected tier is not found (though this shouldn't happen with choice())
        next_tier = None

    return current_tier, next_tier, current_tier_points, next_tier_points

def generateLoyaltyData():
    
    loyalty_levels = ["Bronze", "Silver", "Gold", "Platinum"]
    loyalty_points = [1000, 3000, 5000, 10000]
    current_loyalty, next_loyalty, current_points, next_level_points = get_random_loyalty_tiers(loyalty_levels, loyalty_points)
    loyaltyID = "L"+str(random.randrange(11111111, 99999999, 8))
    
    gender = random.choice(['M', 'F']).upper()
    if(gender == 'M'):
        firstName = fake.first_name_male()
    else:
    	firstName = fake.first_name_female()
        
    middleName = random.choice(string.ascii_letters).upper()
    lastName = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=71).strftime("%m/%d/%Y")
    email = fake.safe_email()
    phoneNumber = fake.phone_number().split("x")[0]
    phoneNumber = re.sub(r'\D+', '', phoneNumber)

    streetAddress1 = fake.street_address()
    city = fake.city()
    zipCode = fake.postcode()

    accountStatus = 'ACTIVE'
    accountType = random.choice(['PERSONAL', 'CORPORATE']).upper()

    loyaltyObj = {
        "LoyaltyId": loyaltyID,
        "FirstName": firstName,
        "LastName": lastName,
        "MiddleName": middleName,
        "Gender": gender,
        "BirthDate": dob,
        "Email": email,
        "PhoneNumber": phoneNumber,
        "AccountStatus": accountStatus,
        "AccountType": accountType,
        "AddressLine1": streetAddress1,
        "City": city,
        "PostalCode": zipCode,
        "CountryCode": "US",
        "LastUpdated": datetime.now().isoformat(),
        "CreatedDate": datetime.now().isoformat(),
        "ProgramId": "1",
        "ProgramName": "Loyalty Tier Program",
        "CurrentStatusLevelDescription": current_loyalty,
        "NextStatusLevelDescription": next_loyalty,
        "PointsUnit": "miles",
        "PointsBalance": current_points,
        "MilesToNextLevel": next_level_points,
        "EnrollDate": fake.date_time_between(start_date="-5y", end_date='-1y').isoformat(),
        "LifetimeMiles": random.randint(1000, 10000)
    }
    return loyaltyObj

def generatePreferencesData(loyaltyObj):
    preferences = {
        "LoyaltyId": loyaltyObj['LoyaltyId'],
        "PreferenceId": fake.uuid4(),
        "SeatDescription": random.choice(['Window','Aisle']),
        "CabinDescription": random.choice(['Economy','Premium Economy','Business','First']),
        "Language": "EN",
        "MealType": random.choice(['Gluten Friendly','Kosher','Vegan (Strict)','Asian Vegeterian']),
        "DietaryRestriction": random.choice(['None','Nut Allergy']),
        "FareTypeDescription": random.choice(['Lowest available Fare','Flexible fare','Unrestricted fare']),
        "AirportCode": random.choice(['SFO','ORD','JFK','DAL','IAD','LAX']),
        "ReferenceId": loyaltyObj['LoyaltyId'],
        "ReferenceType": "profile",
        "LastUpdated": datetime.now().isoformat(),
        "CreatedDate": datetime.now().isoformat(),
        "Wheelchair": random.choice(['true','false']),
        "DisabilityType": random.choice(['Blind','Deaf','Cognitive Disability','Other disability requiring assistance']),
        "SupportAnimal": random.choice(['true','false']),
        "MarketingOptIn": random.choice(['true','false']),
        "MarketingChannelType": random.choice(['Email','SMS']),
        "ContactDetailCommunicationMethod": random.choice(['Email','SMS']),
        "ContactDetailEmail": loyaltyObj['Email'],
        "TravelType": "Non-stop"
    }
    return preferences

def generateBookingData(loyaltyObj):
    df = pd.read_csv('../assets/sample_air_routes.csv')
    df = df.fillna('')
    bookings = []
    noOfBookings = random.randint(3, 15)
    createDayOfTravelBooking = random.choice(['TRUE', 'FALSE'])
    print(f"createDayOfTravelBooking {createDayOfTravelBooking}")
    for index in range(noOfBookings):
        flightIndex = random.randint(1, 25)
        specific_row_iloc = df.iloc[flightIndex]
        
        if createDayOfTravelBooking == 'TRUE':
            travelDt = date.today()+timedelta(days=1)
            createDayOfTravelBooking = 'FALSE'
        else:
            travelDt = fake.date_between(start_date="-30d", end_date='+90d')
        
        depDateTime = travelDt.strftime('%Y-%m-%d')+'T'+specific_row_iloc['DepartureTime']
        arrDateTime = (travelDt).strftime('%Y-%m-%d')+'T'+specific_row_iloc['ArrivalTime']
        current_time = date.today()
        flightDuration = (datetime.strptime(arrDateTime, '%Y-%m-%dT%H:%M:%S'))-(datetime.strptime(depDateTime, '%Y-%m-%dT%H:%M:%S'))
        
        if current_time > travelDt:
            status = 'Completed'
        else:
            status = 'On Time'
        
        booking = {
            "LoyaltyId": loyaltyObj['LoyaltyId'],
            "BookingId": fake.uuid4(),
            "PNR": fake.license_plate().replace(" ","").replace("-",""),
            "FirstName": loyaltyObj['FirstName'],
            "MiddleName": loyaltyObj['MiddleName'],
            "LastName": loyaltyObj['LastName'],
            "Email": loyaltyObj['Email'],
            "PhoneNumber": loyaltyObj['PhoneNumber'],
            "DateOfBirth": loyaltyObj['BirthDate'],
            "CreatedOn": fake.date_time_between(start_date="-60d", end_date='-30d').isoformat(),
            "CreationChannelId": random.choice(['Web','Mobile','Agency','CSR']),
            "LastUpdated": datetime.now().isoformat(),
            "LastUpdatedBy": "user",
            "SegmentId": fake.uuid4(),
            "From": specific_row_iloc['From'],
            "To": specific_row_iloc['To'],
            "FlightNumber": str(specific_row_iloc['FlightNumber']),
            "DepartureDate": depDateTime,
            "SchDepartureTime": depDateTime,
            "DepartureTime": specific_row_iloc['DepartureTime'],
            "ArrivalDate": arrDateTime,
            "SchArrivalTime": arrDateTime,
            "ArrivalTime": specific_row_iloc['ArrivalTime'],
            "IsArmed": "false",
            "TravellerId": fake.uuid4(),
            "IsIntrntl": specific_row_iloc['IsIntrntl'],
            "HasPaidPremimumAccess": random.choice(['true','false']),
            "BagCheckinCount": random.randint(0,2),
            "Price": int(specific_row_iloc['Price']),
            "TravellerPrice": int(specific_row_iloc['Price']),
            "Status": status,
            "BkdClsOfSrv": random.choice(['Economy','Premium Economy','Business','First']),
            "SeatNbr": str(random.randint(1,32))+random.choice(['A','B','C','D','E','F']),
            "FlightMiles": int(specific_row_iloc['FlightMiles']),
            "MilesEarnAmount": int(specific_row_iloc['MilesEarnAmount']),
            "FlightDuration": str(flightDuration)
        }
        bookings.append(booking)
    return bookings