<h1 align="center">Simple Bug Tracker - Data Centric Development Milestone Project</h1>

[View the live project here.](https://sbug-tracker.herokuapp.com/)

This is a webapp aimed to work as a tool to help to manage Projects and Tickets within a Team. It was designed to be simple and easy to use.

<p align="center"><img src="https://sbug-tracker.herokuapp.com/static/img/SimpleBugTrackermockup.png" height="700px"><br>
<h8>Background vector created by rawpixel.com - <a href="https://www.freepik.com/vectors/background" target="_blank">www.freepik.com</a></h8>

 ## User Experience (UX)

-   ### User stories

    -   #### First Time Visitor Goals

        1. As a First Time Visitor, I want to easily understand how to use and navigate the webapp.
        2. As a First Time Visitor, I want to be able to easily navigate throughout the menus.
        3. As a First Time Visitor, I want to have option to be able to manage projects and tickets.

    -   #### Returning Visitor Goals

        1. As a Returning Visitor, I want to to be able to login and see my tickets on the dashboard.
        2. As a Returning Visitor, I want to edit and close my tickets.
        3. As a Returning Visitor, I want to Archive or Delete the projects.

    -   #### Frequent User Goals
        1. As a Frequent User, I want to be able to change my password.
        2. As a Frequent User, I want to be able to give admin permission to another users.
        3. As a Frequent User, I want to as admin be able to reset another user's password.

-   ### Design

    -   #### General
        -   This Webapp with a simple language keeping the navbar menu on top when on desktop and on the side activated by a hamburguer button style aking the navigation very easy and accessible from anywhere. The Menu is dynamic showing only allowed options to regular or manager (admin) users. The admin has the power to create Projects and assign to users. Also the admin can reset any user's password if necessary or modify the user to be another admin. After logged in the user is presented with the Dashboard that will list all projects and its related tickets.

    -   #### Colour Scheme
        -   The blue colour was chosen as the main tone as it is known to be a calming colour. The contrast ratio was taken in consideration to every person be able to read clearly.

       #### Wireframes

    -   Home Page Wireframe - [Download](https://drive.google.com/file/d/1Kv-Sk2_msZDNv4PUR4pR-ubz8vcapROn/view?usp=sharing)
    -   Logo Icon Design - [Download](https://drive.google.com/file/d/1cUnwxe_87_Z0uGhLj3LODkmWDF6zAkcx/view?usp=sharing)

   

## Features

-   Mobile First approach

-   Responsive on all device sizes

-   Login with encripted password

-   Admin demostration mode

-   Archive Project to be able to review it

-   Weather information on Home page


- ## Database Design

    -   ### General
        - The Database was laid with tables to reflect the need of the app at initial structure. It was taken in consideration that tables should be simple and data must be easy to retrieve and if necessary to expand for future improvements.
        
        <p align="center"><img src="https://sbug-tracker.herokuapp.com/static/img/DBdiagram.PNG" height="700px"></p><br>
        <h8>DB diagram created with <a href="https://app.diagrams.net/" target="_blank">app.diagrams.net</a></h8>

    -   DB Diagram Schema - [Download](https://drive.google.com/file/d/1Pafmj-4oVsDjhE6eaEez1Rj5giXy_S-Q/view?usp=sharing)


## Technologies Used

### Languages Used

-   [HTML5](https://en.wikipedia.org/wiki/HTML5)
-   [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
-   [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
-   [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

### Frameworks, Libraries, APIs & Programs Used

1. [Flask:](https://flask.palletsprojects.com/en/1.1.x/)
    - Flask was used to create the web application with Python.
1. [Jinja:](https://jinja.palletsprojects.com/)
    - Jinja used to create the templates for Python.
1. [Materialize:](https://materializecss.com/)
    - Materialize was used to create components, forms, buttons and the navbar of the application.
1. [Font Awesome:](https://fontawesome.com/)
    - Font Awesome was used on the forms and buttons to add icons for aesthetic and UX purposes.
1. [jQuery:](https://jquery.com/)
    - jQuery was used to initialize the components from Materialize.
1. [MongoDB Atlas:](https://www.mongodb.com/)
    - Mongo DB Atlas is the Database used on this app. All CRUD operations are covered.    
1. [OpenWeather:](https://openweathermap.org/)
    - Open Weather API was used to display the weather on the Home Page.    
1. [Git:](https://git-scm.com/)
    - Git was used for version control by utilizing the Git Bash terminal to commit to Git and Push to GitHub.
1. [GitHub:](https://github.com/)
    - GitHub is used to store the projects code after being pushed from Git.
1. [Heroku:](https://github.com/)
    - Heroku was used to deploy the project and have the app live.
1. [Visual Studio Code:](https://code.visualstudio.com/)
    - Visual Studio Code was used to write the code.
1. [Affinity Designer:](https://affinity.serif.com/en-gb/designer/)
    - Affinity Designer was used to create the wireframes, Logo and Design Mockup for this Readme.

## Testing

The W3C Markup Validator and W3C CSS Validator Services were used to validate the page of the project to ensure there were no syntax errors.

-   [W3C Markup Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)
    -   The validator picked up 2 different errors and 1 warning. The errors and warning were corrected.

-   [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)

### Further Testing

-   The WebApp was tested on Google Chrome, Internet Explorer, Microsoft Edge, Brave and Firefox browsers.
-   The website was viewed on a variety of devices such as Desktop, Laptop, Android and iPhones of different screen resolutions.
-   A large amount of testing was done to ensure that all features were working correctly.
-   Friends and family members were asked to review the site and documentation to point out any bugs and/or user experience issues.

### Testing FeedBack and Improvement

-   User noted that after closing or reopening a ticket, the app was sending him to the Home Page. The routing was refactored to send the user to the Dashboard instead as wished.

-   User noted that when on mobile with a small screen (older iPhone models), the Dashboard and Placeholders on the form was getting cramped, breaking the design and going over each other. The column design on Materialize was redone to display properly on older devices with smaller screens.

-   User complained that he couldn't open a ticket with the system when opening the Webapp on a forked version of Chrome with Adlock. When testing with another mainstream browser like Firefox the Webapp worked correctly to him. I completed doing some tests with Adblock installed on Official Chrome browser and didn't find any problem.


### Known Bugs

-   When creating New Ticket, the error messages for Ticket Category and Project Selection are not being displayed correctly.

-   The search field on Manage User was designed on the same way all other containers from the Webapp, but for some reason it appears wider than other containers.
