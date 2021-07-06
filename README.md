# JS Jewelry - Django-powered Ecommerce 
LIVE: http://masteretsam.com/

# Django Features
### User Authentication
Deploys sign in, sign out, and sign up through session-based authentication

### Lazy(Guest) User 
Able to give session tokens to guest users and treat them like normal users. Guest users can complete their bio after they have made purchases (Info Complete WIP)

### Stripe Payment
Using the stripe payment api users will be redirected to a stripe payment page

### Stripe Webhook
Stripe webhook talks to the django server through an active listener. Upon receiving a sucessful payment, server updates the purchase and prints a reciept, which is sent to the customer through their email (Email WIP)

### Easy-to-use Admin Panel
The admin user can make changes to the inventory anytime through the admin panel with good UI.

### Form Authentication
Django backend checks for validity in every single form (sign up form, shipping address form, billing ...)

