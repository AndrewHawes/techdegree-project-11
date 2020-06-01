CHANGE URLS BACK, REMOVE LOCALHOST AND PORT
Notes: 
1. Changed anchors to buttons so they would be valid HTML

# Pug or Ugh API

#### Run Script
-[x] Script runs correctly

#### Display Dogs
-[x] The correct dogs are shown
    -[x] (EC) The ability to add and delete dogs from the application 
    has been added.

#### Dog Model
-[x] A `Dog` Model is properly configured and contains the required fields:
    - name
    - image_filename
    - breed
    - age - integer for months
    - gender, "m" for male, "f" for female, "u" for unknown
    - size, "s" for small, "m" for medium, "l" for large, 
    "xl" for extra large, "u" for unknown
    
    -[x] (EC) Other relevant data fields are added to increase 
    the application's functionality.
        -[x] Favorite brand of cat food
        -[x] Likes classy French films
        -[x] Unafraid to express its feelings with high-pitched chicken sounds
        -[x] Is actually a robot
    
    Note: `image_filename` has been changed to a property that returns the filename (basename) from the image field 
#### UserDog Model
-[x] A `UserDog` Model is properly configured and contains the required fields:
    - user
    - dog
    - status, "l" for liked, "d" for disliked
    
    -[x] (EC) Other relevant data fields are added to increase 
    the application's functionality.
        -[x] Hidden - won't show dog again

#### UserPref Model
-[x] A `UserPref` Model is properly configured and contains the required fields:
    - user
    - age, "b" for baby, "y" for young, "a" for adult, "s" for senior
    - gender, "m" for male, "f" for female
    - size, "s" for small, "m" for medium, "l" for large, "xl" for extra large
    
    -[x] (EC) Other relevant data fields are added to increase 
    the application's functionality.
        - type

#### Serializers
-[x] Serializers for the `Dog` and `UserPref` Models are in place and reveal all
fields, except that `UserPref` does not need to reveal the `user`.

#### Routes
-[x] The required routes are in place and function correctly.
    - To get the next liked/disliked/undecided dog:
        - `/api/dog/<pk>/liked/next/`
        - `/api/dog/<pk>/disliked/next/`
        - `/api/dog/<pk>/undecided/next/`
    - To change the dog's status:
        - `/api/dog/<pk>/liked/`
        - `/api/dog/<pk>/disliked/`
        - `/api/dog/<pk>/undecided/`
    - To change or set user preferences:
        - `/api/user/preferences/`
    
    -[x] (EC) Additional routes are added which increase the application's functionality.

#### Authentication
-[x] Uses Token-Based Authentication

#### Unit Test the App
-[x] There are unit tests for all the views, models, and other functions.
The tests must cover 50% of the code.
    -[x] Test coverage above 75%.

#### Python Code Style
-[ ] The code is clean, readable, and well organized. It complies with most
common PEP 8 standards of style.


#### Extras
-[x] Fix register to show error if username already exists
-[x] Fix favicon
-[x] Redirect to dog page when adding dog
-[x] Make sure errors show up for form
-[-] Enter clicks login/register button
-[x] Move dog images into media directory so it's not in static
-[x] Make sure only added_by user or admin can delete a dog
-[-] Set up custom user that creates userpref automatically on save
-[x] Handle bad login information
-[x] Create converter for status so user can't input random url
-[x] Make sure only user who created a dog or admin can delete it
-[x] Fix headings being used for styling
-[x] Make sure liked, disliked, undecided, new dog links are hidden unless
user is logged in

-[ ] Change React handler names: submitHandler -> handleSubmit
-[x] Use months old to extrapolate age
-[ ] Display message if user is denied permission to delete dog (status 403)


JAVASCRIPT:
-[ ] Use default props to assign undefined in Dog?
-[ ] Fix display of error messages
-[ ] Clear login screen on reload (currently uses last value for username)
