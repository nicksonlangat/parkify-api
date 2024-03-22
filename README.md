## INTRODUCTION

Parkify API is the backend codebase for an online parking garage.
The whole idea of the system is simple; seamlessly allow users
to find parking spots in the facility and park their vehicles.

The system needs to allow users to:

- Create accounts and login.
- Select a spot that supports their vehicle type.
- Book the spot.
- Pay for the booked spot.
- Download the parking ticket/receipt as a PDF.
- Receive the ticket via their email address.
- Receive an SMS confirmation on their booking.

The system will not allow:

- A user to book the same spot twice for the same car on that day.
- A user to book a spot that another car has booked on that day.
- A user to book a spot that doesn't support their car type.

Here is a detailed document where I share more about the system [view it here](/design_docs/thought_process.md).

### RUNNING THE PROJECT

To run the project:

- clone the repo `[here](https://github.com/nicksonlangat/parkify-api.git)`
- create a virtual environment `virtualenv env`
- install dependencies `pip install -r requirements.txt`
- use the `Makefile` to run migrations `make migrate`
- use the `Makefile` to add admin `make su`
- use the `Makefile` to start celery `make celery`
- use the `Makefile` to run the dev server `make run`
- [Go to this link](http://localhost:8000) to view the application in browser.
