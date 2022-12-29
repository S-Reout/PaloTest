## Welcome to "PaloTest" ##
A sample python & pytest project intended to test a web application


## Docker Setup ##
To run the tests in docker:
Please open the terminal and navigate to the "PaloTest" directory, and enter the following command:

``docker-compose up`` 

Per "docker-compose.yaml", command creates two containers running on linux os:

**web-app**: web application, running on port 8000.

**test-server**: test suite running via pytest. HTML report is generated internally after test run.


## Local Setup ##
To run tests locally (localhost):
Please open the terminal and navigate to the "PaloTest" directory, and enter the following command:

``docker-compose up web-app -d``

Command creates web application container. Port 8000 is exposed for external use.
In your IDE please add the following environment variables to Run/Debug Configuration:

BASE_URL=http://localhost:8000;

DEFAULT_USER=admin;

DEFAULT_PASS=admin;

(*Disclaimer: Credentials are added for convenience only, would not be revealed in a real project)


## Additional info ##
List of known bugs can be found in the document "Palo Alto - Testing Task Report.xlsx"


## Contact ##
Created by Reout Sagui (reouts@gmail.com) - feel free to contact me.

