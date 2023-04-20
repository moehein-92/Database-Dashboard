

**Title: Faculty Dashboard**

Purpose: The application is mainly aimed at students who want to find out more information about professors (faculty) or students who are looking for a professor who they want to work with as a graduate student. This application can be also useful for student looking for a professor who will be teaching one of the classes who is expert in a field or looking for an advisor.  Students can just enter the name of the professor and look up key information. Students can find out a professor's contact information, information related to papers that the professor has published, top research keywords, and other similar faculty members that the professor have collaborated with on publications. The application also provides the ability to add or remove a student's favorite faculty member.

**Video Demo Link:**

[Project video link](https://mediaspace.illinois.edu/media/t/1_fmp49o66)

**Installation:**

1. Pip install the following Python dependencies:
    - dash
    - mysql.connector
    - pymongo
    - neo4j
    - pandas
    - dash_bootstrap_components
    - plotly
    - numpy
    
2. Start up neo4j database in neo4j desktop. Not required for mysql and mongoDB.
3. Run the python application "app.py" in bash or powershell to start up the application.

**Usage:**

Start by entering the name of a faculty member in the search bar. The entered name needs to match the exact name of the faculty member in the database. Follow the approprite drop down menus or buttons to trigger different widgets in the application. See Design section below for detailed information on functions of the different widgets in the application. 


**Design:** 

The application is based on the Python Dash Plotly framework (https://dash.plotly.com/introduction). The frontend is composed of HTML, dash core components and dash bootstrap components. The Dash widgets in the application are connected to 3 different databases: MySQL, MongoDB and Neo4j.  

Implementation: How did you implement it?

There are a total of of 9 widgets in the application. The application also creates a table for favorite faculy members in MySQL DB if it doesn't exist yet.  These are implemented in Dash plotly with MySQL, MongoDB and Neo4j databases.  The dash widget sent different query to each of the databases.

__Widget 1: Basic Information__

Once faculty name has been entered into the text input, this widget connects to MySQL DB, sends a query with the name of the faculty and returns to display basic contact information of the faculty member such as phone and email along with a photo image.


__Widget 2: Popular Publications__

Similar to Widget 1, this widget sends a SQL query using the user input faculty name to display publications that the faculty member have published and sorted by the number of citations of each publication. Returns publication title, year and count of num_citations in a table format. 


__Widget 3: Publications by Year__

This widget uses an SQL query and Plotly graph object to display the publications the faculty member have published over time as a graph of year vs. the count of publications published in a year. The callback function for this widget also outputs the list of publications to be passed onto Widget 4.


__Widget 4: Filter Publications by Year__

This widget utilizes the Output of the callback function from Widget 3 to create a dropdown menu where users can search for publications of a professor and filter it by year published using Neo4j.


__Widget 5: Top Research Keywords__

This widget connects to MongoDB and sends a query for the top keywords based on score that is associated with the name of the faculty member and stores the results into a pandas dataframe. Uses the data stores in the dataframe to return a pie chart of the different keywords by percentage created through the plotly graph object.


__Widget 6: Collaborated Faculty__

This widget is meant to find similar faculty members to that of the user input faculty member. Similarity metric is based on if two faculty members have co-authored publications and sorted by the number of publications that they have co-authored. The widget sends a query to the Neo4j DB, stores results in a pandas DF and displays a table built using a plotly graph object.

__Widget 7: Add Favorite Faculty__

This widget allows user to add favorite faculty member and store it in MySQL DB if 'Add Faculty' button is clicked. The widget uses 2 callback functions. The first callback function is to open a dash boostrap modal component where the user is prompted to enter name, email and a comment of the favorite faculty member. The modal includes a 'Submit' button when clicked, triggers the second callback function that takes the input fields from the modal and writes it to the favoriteFaculty Table in MySQL DB. Also, the input fields are passed in as States so that the callback function isn't triggered unncessarily as soon as there is a change in the first callback.

__Widget 8: Delete Favorite Faculty__

This widget works similar to Widget 7 where the user is prompted to enter the name of the favorite faculty member to be deleted. The faculty member with that name is then deleted from the favoriteFaculty Table through a SQL query.

__Widget 9: Display Favorite Faculty__

This widget displays the current favorite faculty members that are in the favoriteFaculty Table. Also, whenever a new favorite faculty member is added, this new members is automatically displayed in the output of this widget.


**Database Techniques:**

1. We added indexing to faculty name and publication year in the Neo4j database since these query are slow, and also we use index hint in our query.

2. In a lot of our widgets, we take a user input such as 'faculty name' and use a prepared statement to query our MySQL database especially for insertion, deletion, and creation of table.

3. When creating the favoriteFaculty Table at the first time launching our application, we add constraints such as UNIQUE, NOT NULL and PRIMARY KEY to our input fields that the user will provide in Widget 7: Add Favorite Faculty.

**Extra-Credit Capabilities:** 

We utilized multi-database querying for extra-credit in our application.

This occurs in widgets 3 and 4 where the number of publications by year is first queried using MySQL which returns data that contain year and publication count per year. This result is used to create dynamic drop down menu for users to select publication by year whose options change based on faculty member. Next a Neo4j query is used to return a table of publications filtered by year for selected faculty.


