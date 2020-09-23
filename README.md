# Penn Labs Backend Challenge

## Documentation

### Models

For the user model, I decided to give the following attributes to each user object:
- `user_id`: Unique user ID. Serves as the primary key of the user.
- `username`: Username. Serves as unique identifier for a user in the system which is 
used by a given user for login purposes.
- `email`: Email address. The unique address that is associated with the user's school email account as provided by the university.
- `first`: First name of the user. Consists of a string of 80 maximum characters.
- `middle`: Middle name of the user (if given). Can be blank (default is blank string).
- `last`: Last name of the user. Consists of a string of 80 maximum characters.
- `student_type`: User's student type. Can be either `Undergraduate` or `Graduate`.
- `class_year`: User's graduation class year. Designates the year (as an integer)
that the user is expected to graduate with a degree.
- `major`: User's major or area of study. Designates the academic discipline for which
the user has decided to pursue a degree for. Default value is `Undecided`.
- `sub_school`: User's associated school. Designates the sub-school (e.g. SEAS, Wharton) that is the user is associated with at the university.
- `club_id`: ID of a favorite club associated with the user. Serves as a foreign key.
- `club`: Indicates a club that has been favorited by the user.

For the club model, I decided to give the following attributes to each club object:
- `code`: Club's code designation. Serves as a unique identifier of the club similar to how usernames designate individual users in the system.
- `name`: Name of the club. Consists of a string of 80 maximum characters.
- `description`: Description of the club. Serves as a comprehensive summary of the 
club in terms of its activities, mission, goals, and other information.
- `tags`: Tags associated with the club. Designates the tags used to label the club
in terms of its audience, areas of academic study, club type, and other traits.
- `favorites`: List of users who have favorite the club. Designates the users who have favorited the club through the system, which are included in teh 

For the tag model, I decided to give the following attributes to each tag object:
- `id`: Unique tag ID. Serves as the primary key of the tag.
- `tag_name`: Name of the tag. Serves as a unique identifier of the tag.
- `club_id`: ID of a club that is associated with the tag. Serves as a foreign key.
- `club`: Indicates a club that has been labeled by the tag.

Most of the fields have string data types due to the nature of their data, with some having higher character limits than others due to the possible range of values that they could hold. For instance, both usernames and emails in the User model were given maximum character limits of 80 since individual usernames and email addresses can get
quite long, especially in the latter case. Other fields were given smaller maximum character limits of 50 or 20 since the chances of values being longer in length than those limits are unlikely (e.g. first and last names, student types, club codes, tag names). Only a select few fields were given alternative data types. For the unique ID numbers and student years, the integer data type was chosen since their data was of numerical nature. The club description field has the text data type since values in that field consist of strings with variable lengths, giving dynamic flexibility.

### Routing Features

For the URL routing of the Flask web application, I used a total of five different
routes in addition to the baseline routes provided. I consolidated three of the 7
functionalities under one common route decorator due to their shared route names
and similar features related to club information display and modification. I also
created a few helper functions to streamline the code and modularize it through
the reuse of shared features in common functions.

#### User Profiles

For the fetching of user profile information, I executed specific Flask-SQLAlchemy
queries that filtered out user information from the username string supplied as a
dynamic variable in the URL route. I then concatenated the first, last, and middle
(if it exists) names of the user to form their full name. This was included with
the other fields returned by the initial user query in a JSON object and returned for display on the frontend via a GET request method.

#### Club Management

Three of the features related to club management (i.e. getting the list of all clubs,
searching for clubs, and adding new clubs) were aggregated under the same URL route
but separated in handling through the use of different HTTP request methods and the inclusion of URL query parameters. For the retrieval of all clubs, the helper
function `get_all_clubs()` was used to query all existing clubs in the Club table
relation and build a JSON object dictionary with all club information. The compiling
of this dictionary was in turn handled by another helper function `get_clubs()`, which
took in a list of clubs of interest for which JSON objects must be built and iterated
through each club. For each club, all existing information such as name, code, and description was gathered, along with the number of users who favorited the club. Once finished, the JSON object dictionary was then returned for display.

For the searching of clubs, the query parameter string was parsed from the URL
using `request.args.get()` since all URL query parameters are accessed from
`request.args`. A Flask-SQLAlchemy query was then built and executed
using this URL query parameter to find all clubs that contain the provided query
string in their names (case insensitive) using `.ilike()`. The `get_clubs()` function
was then used to return the information for all the clubs in the returned results. Both of these two features relied on GET request methods.

For the addition of new clubs, information for the new club was supplied through a
JSON object in the body of a POST request. After receiving and parsing this JSON
object (i.e. club code, name, description, and tags), the helper function
`add_new_club()` created a new Club object with the parsed information. In particular,
new club tags were appended into a list attached to the Club object while all other
fields were singular in nature. The new Club object was then inserted into the
Club relation table of the database, with a message was returned indicating success of the new club addition operation.

#### Favorite Clubs

For handling favorites for a club, information for the club being favorited
was supplied via the body payload of a POST request with a singular field that
represented the user who wished to favorite the club. The username was parsed
from the POST request, while the club name string was parsed as a dynamic variable
from the URL route. A Flask-SQLAlchemy query was then executed to access the entry
in the Club relation with information about the specified club. This was done in
order to update its `favorites` attribute by potentially appending the username of
the favoriting user. The actual update was only performed if the favoriting user's
username was not already in the club's `favorite` attribute. This was done to prevent
any given user from trying to favorite a club more than once, thus not skewing the
like count of the club. A message would then be returned to indicate whether the attempt made by the user to favorite the specified club had succeeded or failed.

#### Modifying Clubs

For the modification of clubs, a PATCH request was used to supply new values for
attributes of a given club specified by their club code. The club code string was parsed as a dynamic variable from the URL route, while the PATCH request body had
the keys and values that were to be used in the club information update. For this
operation, a Flask-SQLAlchemy update query was used to update the multiple fields
specified in the PATCH request body JSON dictionary object by passing in the JSON
dictionary as an argument for the `update()` functionality of the query. A final
dynamic message was then returned to indicate success, with the code of the club
that was updated included in the message.

#### Tag Counts

For displaying all tags and the number of clubs associated with each, a
Flask-SQLAlchemy query was first executed to return all entries from the Tag relation
table of the database. For each of these returned results, a secondary query was
executed to retrieve the number of clubs attached to each tag, using the tag name
as a filter while making use of the `count()` query functionality. Each tag name
was placed into a JSON object together with its count, after which the JSON object
was appended to a repository list storing information for all existing tags. After
all tags were processed in this manner, the final list of all tags and their counts
was returned as a JSON object for display through a GET request method.

## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipenv`
   - `pip install --user --upgrade pipenv`
4. Install packages using `pipenv install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Run `pipenv run python bootstrap.py` to create the database and populate it.
2. Use `pipenv run flask run` to run the project.
3. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-Fall-20-31461f3d91ad4f46adb844b1e112b100).
4. Document your work in this `README.md` file.

## Reference frontend

If you want to use the reference frontend to see if your implementation of the
backend is working correctly, follow the below steps

1. `cd reference-frontend` to enter the directory.
2. `yarn install` to download all the dependencies.
3. `yarn start` to start the server.
4. Navigate to `localhost:3000` to see if the website is working correctly.

Feel free to make changes to the reference frontend as necessary. If you want
to work on the reference frontend as a supplementary challenge, the current
implementation doesn't implement _tags_. Modifying the reference frontend to
list club tags while browsing clubs or allow users to include tags while
creating a new club could be a good place to start with improving the frontend.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `pipenv install <package_name>` within the directory. Make sure to document your additions.
