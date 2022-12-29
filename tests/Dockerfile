# OS
from ubuntu

# Install Python 3.10 and pip
RUN apt-get update -y
RUN apt-get install -y python3.10 python3-pip

# Copy tests folder content
copy * /tests/

# Install packages
RUN pip install -r ./tests/requirements.txt

# Run pytest on tests folder
cmd ["pytest", "tests/", "--html", "tests/report.html"]
