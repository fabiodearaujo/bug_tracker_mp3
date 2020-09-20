<h1 align="center">Simple Bug Tracker - Data Centric Development Milestone Project</h1>

[View the live project here.](https://sbug-tracker.herokuapp.com/)

This is a webapp aimed to work as a tool to help to manage Projects and Tickets within a Team. It was designed to be simple and easy to use.

<p align="center"><img src="https://sbug-tracker.herokuapp.com/static/img/SimpleBugTrackermockup.png"><br>
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

    -   #### Typography
        -   The Roboto font is the default font from Materialize CSS that is used throughout the whole website with Sans Serif as the fallback font in case the font isn't being imported into the site correctly. Roboto is a clean font used frequently in Google ecosystem, so it is both attractive, appropriate and memorable.

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
        
        <p align="center"><img src="https://sbug-tracker.herokuapp.com/static/img/DBdiagram.PNG"></p><br>
        <h8>DB diagram created with <a href="https://app.diagrams.net/" target="_blank">app.diagrams.net</a></h8>

    -   DB Diagram Schema - [Download](https://drive.google.com/file/d/1D_Tf52xDYcXgjyKV3o4u3YeFmbN2rxjY/view?usp=sharing)


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

-   [W3C Markup Validator](https://validator.w3.org/)
    -   The validator picked up 2 different errors and 1 warning on the first run. The errors and warning were corrected.
    -   Test passed with no Warnings or Errors.

-   [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input)
    -   The validator found 1 Error and 493 Warnings in the Materialize CSS stylesheet. All other CSS were Valid.

-   [W3C Broken Link Checker](https://validator.w3.org/checklink?uri=https%3A%2F%2Fsbug-tracker.herokuapp.com%2F&hide_type=all&depth=&check=Check)
    -   The validator found 1 redirection link that is now corrected.

-   [PEP8 Checker](http://pep8online.com/) - [Error results](https://drive.google.com/file/d/1bpk_cfYu6r4yHhpD8Dfy_MZ65r4BYKQB/view?usp=sharing)


### Further Testing

-   The WebApp was tested on Google Chrome, Internet Explorer, Microsoft Edge, Brave and Firefox browsers.
-   The website was viewed on a variety of devices such as Desktop, Laptop, Android and iPhones of different screen resolutions.
-   A large amount of testing was done to ensure that all features were working correctly.
-   Friends and family members were asked to review the site and documentation to point out any bugs and/or user experience issues.

### Testing FeedBack and Improvement

-   User noted that after closing or reopening a ticket, the app was sending him to the Home Page. The routing was refactored to send the user to the Dashboard instead as wished.

-   User noted that when on mobile with a small screen (older iPhone models), the Dashboard and Placeholders on the form was getting cramped, breaking the design and going over each other. The column design on Materialize was redone to display properly on older devices with smaller screens.

-   User complained that he couldn't open a ticket with the system when opening the Webapp on a forked version of Chrome with Adlock. When testing with another mainstream browser like Firefox the Webapp worked correctly to him. I completed doing some tests with Adblock installed on Official Chrome browser and didn't find any problem.

-   User complained that when creating a ticket, the Manager also should be already selected from the user selection, as the Manager needs to have access to the project he is managing. It was modified the logic so the Manager user is already selected when creating a project.

-   More than one user complained that after creating a project, the most intuitive way was to return straight to the Dashboard instead of staying on the Create Project page. The Redirection to Dashboard was made to reflect the user wishes.

-   The Flash messages colour were not taking the attention of the user. It was redesigned and the color changed to an Orange to grab the user's attention.


### Known Bugs

-   When creating New Ticket, the validation error messages for Ticket Category and Project Selection are not being displayed correctly.

-   Only on iPhones, the selection element on the form doesn't display properly and it is hard to pick an option.

-   The search field on Manage User was designed on the same way all other containers from the Webapp, but for some reason it appears wider than other containers. Not a major issue, but it will be reviewed in future versions.

### Issues tracker

- Issues encontered during development, testing and after deployed are being registered at [GitHub Projects](https://github.com/fabioaraujo76/bug_tracker_mp3/projects/1).

## Deployment

### Heroku

The project was deployed to Heroku using the following steps...

1.  Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-command-line).
2.  If you haven't already, log in to your Heroku account and follow the prompts to [create a new SSH public key](https://devcenter.heroku.com/articles/keys).
    $ heroku login
3.  Clone the [GitHub Repository](https://github.com/fabioaraujo76/bug_tracker_mp3)
    Use Git to clone sbug-tracker's source code to your local machine.
    $ heroku git:clone -a sbug-tracker
    $ cd sbug-tracker
4.  At the tab Settings, setup all Config Vars necessary for the App to run.
5.  Deploy your changes
    Make some changes to the code you just cloned and deploy them to Heroku using Git.
    $ git add -A
    $ git commit -m "make it better"
    $ git push heroku master

For more information on deploying the App with Git follow this [link](https://devcenter.heroku.com/articles/git#ssh-git-transport).

## Collaboration

### Forking the GitHub Repository

By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps...

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. You should now have a copy of the original repository in your GitHub account.

### Making a Local Clone

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/)
2. Under the repository name, click "Clone or download".
3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

7. Press Enter. Your local clone will be created.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `CI-Clone`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Click [Here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for more informatino about Cloning repositories.

Click [Here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests) for more informatino about Collaboration.

## Credits

### Code

-   [Code Institute](https://codeinstitute.net/) - The course gave me the hability to improve my knowledge and was very important source of knowledge on the technologies user on this project.

-   [Materialize](https://materializecss.com/getting-started.html) - The documentation part was important to understand and use the forms and components of the Framework.

-   [OpenWeather](https://openweathermap.org/current) - It was important to understand how to fetch data from the API and also return the icon to match with the current weather.

-   [Stack Overflow](https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable) - This article helped me to resolve the error when retrieveing data from Mongo DB.

-   Other Sources - Not less important, but also helpful, W3 Schools, Google Search and Python/Flask/Mongo DB documentation.


### Acknowledgements

-   My Mentor for continuous helpful feedback.

-   Tim Nelson for the updated lessons on the task manager mini project, it was very important for my understanding on Flask.

-   All friends and family that helped me to test and gave me valuable feedback.