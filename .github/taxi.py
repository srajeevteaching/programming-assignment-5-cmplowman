# Chris Plowman
# Course: CS151, Dr. Rajeev
# Date: 11/16/21
# PA5

import csv
import math

CSV_STARTTIME = 1
CSV_ENDTIME = 2
CSV_PAYMENT = 5
CSV_PAYMENTTYPE = 6
CSV_PICKUPLAT = 8
CSV_PICKUPLON = 9
CSV_DROPOFFLAT = 10
CSV_DROPOFFLON = 11

# A function that, given a filename, loads the data and returns it as a list of lists.
def load_data(filename):
	try:
		f = open(filename, "r")
	except FileNotFoundError:
		print("Exception: \"{}\" not found!".format(filename))
		return []

	# https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.kite.com%2Fpython%2Fanswers%2Fhow-to-read-a-%2560csv%2560-file-into-a-list-in-python&amp;data=04%7C01%7Ccmplowman%40loyola.edu%7Cd5e4dbb90267456d42b508d9ac4a7a1d%7C30ae0a8f3cdf44fdaf34278bf639b85d%7C0%7C0%7C637730258156949158%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000&amp;sdata=haazojHrXIQOJTYWQbs8HamwAmLwgPZZKIFuGV6XV7A%3D&amp;reserved=0
	data = []
	csv_reader = csv.reader(f)
	for row in csv_reader:
		data.append(row)

	f.close()
	return data

# A function that, given four floating point parameters (corresponding to the
# latitude and longitude of two locations) uses the formula given in Item 3
# of the problem statement to return the distance between the given points.
#
# Use the math.radians function to convert the lat/lon degrees to radians before
# calling the math module's trigonometric functions.
#
# Test your function with the coordinates Baltimore (+39.2904, -76.6122) and
# Washington DC (+38.9072, -77.0369). The result should be 34.92485 miles.
#
# The distance between two locations (lat1, lon1) and (lat2, lon2) in miles can
# be calculated using the formula:
#
#   distance_in_miles = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)) * 3959
def distance_between(lat1, lon1, lat2, lon2):
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2)

	return float(math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * 3959)

# For each of the three tasks in the instructions section:
#   1) Output the average cost for cash and (separately) credit card payments.
#   2) Output the count of all trips that started or ended on a user-given date.
#   3) Output to a file (name provided by the user) the information for all trips
#      with a pickup or dropoff location that is within a given distance of a given location.
#
#   NOTE: Each outputted line should be in the same format as the input file.
#
# Write a function that does the calculation, taking inputs as parameters and returns the
# corresponding value (if applicable).
#
#   NOTE: These three functions *should not* use input/output operations.

def average_cost(data):
	cost_cash = 0.0
	cost_credit = 0.0
	count_cash = 0
	count_credit = 0

	for row in data:
		if row[CSV_PAYMENTTYPE] == "Cash":
			count_cash += 1
			cost_cash += float(row[CSV_PAYMENT])
		else:
			count_credit += 1
			cost_credit += float(row[CSV_PAYMENT])

	# watch for divide by 0
	return "cash: ${:.2f}".format(cost_cash / count_cash if count_cash else 1) + ", " + "credit: ${:.2f}".format(cost_credit / count_credit if count_credit else 1)

def count_trips_by_date(data, date):
	trips = 0

	for row in data:
		if row[CSV_STARTTIME] == date or row[CSV_ENDTIME] == date:
			trips += 1

	return trips

def output_trips_by_distance(data, filename, distance, lat, lon):
	try:
		f = open(filename, "w", newline="")
	except IOError:
		print("Exception: Could not open \"{}\"!".format(filename))
		return

	for row in data:
		distance_pickup = distance_between(float(row[CSV_PICKUPLAT]), float(row[CSV_PICKUPLON]), lat, lon)
		distance_dropoff = distance_between(float(row[CSV_DROPOFFLAT]), float(row[CSV_DROPOFFLON]), lat, lon)
		if distance_pickup < distance or distance_dropoff < distance:
			csv.writer(f).writerow(row)

	f.close()

# For each of the three tasks in the instructions section (above) write a function that gathers
# and validates all necessary inputs from the user, calls the corresponding functions (above)
# and presents the results to the user.
#
#   NOTE: These three functions *should* use input/output operations.

def io_average_cost(data):
	print("average_cost() = {}".format(average_cost(data)))

def io_count_trips_by_date(data):
	date = str(input("date (YYYY-MM-DD HH:MM:SS): "))
	print("count_trips_by_date(\"{}\") = ".format(date) + str(count_trips_by_date(data, date)))

def io_output_trips_by_distance(data):
	# initialize to test values
	filename = "taxi.out"
	distance = 0.25
	lat = 41.980264
	lon = -87.913625

	while True:
		try:
			filename = input("filename: ")
			distance = float(input("distance: "))
			lat = float(input("latitude: "))
			lon = float(input("longitude: "))
		except ValueError:
			print("Exception: Invalid value!")
		else:
			break

	output_trips_by_distance(data, filename, distance, lat, lon)
	print("output_trips_by_distance(\"{}\")".format(filename))

# A main function to drive the program. Allow the user to choose one of the three operations
# described in the instructions. After completing the chosen option, the program should loop,
# allowing the user to choose another operation or to end the program.
def main():
	filename = input("enter file name: ")
	data = load_data(filename)
	if len(data):
		while True:
			print("1) average_cost")
			print("2) count_trips_by_date")
			print("3) output_trips_by_distance")
			print("4) quit")
			choice = input("choice: ")
			if choice == "1":
				io_average_cost(data)
			elif choice == "2":
				io_count_trips_by_date(data)
			elif choice == "3":
				io_output_trips_by_distance(data)
			elif choice == "4":
				break
			else:
				continue

main()
