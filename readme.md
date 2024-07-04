Example docker compose

name: <your project name>
services:
    campsite_checker_ab:
        ports:
            - 6901:6901
            - 5901:5901
        environment:
            - ENV_URL='https://shop.albertaparks.ca/camping/chinook-provincial-recreation-area/r/campgroundDetails.do?contractCode=ABPP&parkId=330293#sr_a'
			- ENV_START_DATE="Fri Jul 19 2024"
			- ENV_HOW_LONG="3"
			- ENV_USER_NAME=""
			- ENV_PASSWORD=""
			- ENV_TOKEN=""
			- ENV_CHATID=""
			- ENV_DELAY=4
        container_name: campsite_checker_ab
        image: campsite_checker_ab