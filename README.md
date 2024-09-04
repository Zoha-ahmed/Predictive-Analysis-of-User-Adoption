Configuring a data science algorithm with data from Asana


There are two data files as described below. 
A user file ("takehome_users") with data on 12,000 users who signed up for the product in
the last two years. This table includes:
1. name: the user's name
2. object_id: the user's id
3. email: email address
4. email_domain: domain of email address, e.g. gmail.com
5. creation_source: how they signed up for the product. This takes on one of 5
values:
6. PERSONAL_PROJECTS: invited to join another user's personal workspace
7. GUEST_INVITE: invited to an organization as a guest (limited permissions)
8. ORG_INVITE: invited to an organization (as a full member)
9. SIGNUP: signed up via asana.com
10. SIGNUP_GOOGLE_AUTH: signed up using Google
11. Authentication (using a Google email account for their login id)
12. creation_time: when they created their account
13. last_session_creation_time: unix timestamp of last login
14. opted_in_to_mailing_list: whether they have opted into receiving marketing
emails
15. enabled_for_marketing_drip: whether they are on the regular marketing email
drip
16. org_id: the organization (group of users) they belong to
17. invited_by_user_id: which user invited them to join (if applicable).
A usage summary file ("takehome_user_engagement") that has a row for each day that a
user logged into the product.

We define an "adopted user" as a user who has logged into the product on three separate days in at least one seven-day period. Because we believe that adopted users are more likely to be successful at using Asana in the long term than those that are not adopted, we want to know what things are likely indicators of future adoption. With this in mind, we'd like
you to identify which factors predict user adoption. I took the approach to use data modeling for my implementation.

I wrote my findings & recommendations as if you are presenting to someone outside of the data science team (i.e. an engineer or product manager) who will be making decisions about the initial experience users receive when they first create their accounts. Their work will focus on improving this experience to increase adoption, so they'd like to know how successful Asana currently is at getting different types of users to adopt.