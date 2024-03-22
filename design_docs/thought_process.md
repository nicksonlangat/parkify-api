## INTRODUCTION

This is an overview my thought process I followed while designing and developing the backend
layer for an online parking garage. I start by breaking down everything into small chunks
that I can then tackle individually.

### REQUIREMENTS
 - Parking owners can add parking spots.
 - Users can book available spots.
 - Users can create and log in to their accounts.
 - Users can save their vehicles for easiser future booking.
 - Users can generate pdf receipts upon successful booking.
 - Users can receive pdf receipts via email.
 - Users can receive booking information via SMS.

 The system needs to be architected such that:
 - Users may not double book a given spot.
 - Users may not book an already booked spot.
 - Users can only see available spots, admins can perform CRUD on spots.
 - Users can only see vehicle types, admins can perform CRUD on vehicle types.


### DATABASE CHOICE
The nature of this problem is largely relational in that the database tables will be connected to one another
via foreign keys and this therefore means I will go with a relational database in the choice of
Postgre since I tend to over bias towards it. It certainly is a good choice for this type of a problem.
So in this instance, I will create my database tables inside a PostgreSQL database.

The following are the database tables the app will need:

#### Accounts table

This is where we will store all user information when they register accounts into the system.
The data contained will look like the table below:

| id    | primary key, int, serial |
| -------- | ------- |
| name  | string    |
| email | string     |
| phone_number    | string    |
| password    | hash    |


#### Vehicle types table

This is where we will store all types of vehicles that the parking garage can accomodate.
The data contained will look like the table below:

| id    | primary key, int, serial |
| -------- | ------- |
| name  | string    |
| parking_fee  | float    |


#### Spots table

This is where we will store all available spots in the parking garage based on vehicle type.
The data contained will look like the table below:

| id    | primary key, int, serial |
| -------- | ------- |
| vehicle_type_id    | foreign key referencing vehicle_type.id |
| floor_number  | string    |
| spot_number  | string, unique    |
| is_available | bool     |


#### Bookings table

This is where we will store booking information.
The data contained will look like the table below:

| id    | primary key, int, serial |
| -------- | ------- |
| spot_id    | foreign key referencing spot.id |
| vehicle_type_id    | foreign key referencing vehicle_type.id |
| booking_number | string     |
| registration_number | string     |
| start_date  | date    |
| end_date | date     |
| is_paid | bool     |



### SCALING
