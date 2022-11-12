# BMS
A digital Bike Management System to borrow and manage our school bikes.
Developed with the Django frameworks for web applications in Python.
Eventually supposed to be hosted locally in the school network on a raspberry pi.

## (current) Functionaltities
    *Todo: better website design*
### User registration, login and logout
In `/register`, users can register a new account using a school email. It uses Django-inbuilt functionality, so there's a fair amount of security and checks in place.
    *Todo: more checks for a valid school email, restrict registering to the unauthenticated*
In '/login', users can logout and login depending on if they're already authenticated.

### Profile
`/profile` is a placeholder site to display all available account info.

## Hardware
In the final version, there is a cabinet in H6 featuring holes for each bike key and sensors to detect the presence of keys. The cabinet has an electronically locked door. An arduino communicates with the server about the presence of keys and opens the door when a borrowing request is made (and vice versa when bike keys are returned).

# Resources used
Here I try to keep track of tutorials and references used throughout the development process to improve understandability and long-term maintenance of the code.

-[W3 schools](https://www.w3schools.com/)
*Used as reference for Django, HTML, CSS and many other things*

-[How to write a readme document](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
-[Login System](https://rahmanfadhil.com/django-login-with-email/)
-[Class-based views](https://docs.djangoproject.com/en/4.1/topics/class-based-views/)
-[Collapsible Sidebar with CSS](https://stackoverflow.com/questions/30574902/collapsible-flexible-width-sidebar-using-only-css)

