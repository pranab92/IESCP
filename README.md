
# Influencer-Engagement-Sponsorship-Coordination-Platform
IESCP is a platform to connect Sponsors and Influencers so that sponsors can get their product/service advertised and influencers can get monetary benefit
-----------------------------------------------------
**Steps To See The Website and Try to explore ->**

Run app.py 
-----------------------------------------
You can register for Sponsor or Influencer .
otherwise you can directly use existing users.

****Sponsor-> User=pk; password=pk**

****Influencer -> User=piu; password=piu**


**Influencer Engagement & Sponsorship Coordination Platform**:
----------------------------------------------------------------
It's a platform to connect Sponsors and Influencers so that sponsors can get their product/service advertised and influencers can get monetary benefit.

**Frameworks used**
--------------------
SQLite for data storage

Flask for API

VueJS for UI

Jinja2 templates

Bootstrap for HTML generation and styling

Redis for caching

Redis and Celery for batch jobs

Steps to run the application

Download zip file or clone the repository


**Roles - The platform will have three roles**;
-----------------------------------------------
Admin - root access
An admin can monitor all the users/campaigns, see all the statistics Ability to flag inappropriate campaigns/users
Sponsors - a company/individual who wants to advertise their product/service
Sponsors will create campaigns, search for influencers and send ad requests for a particular campaign.
Sponsors can create multiple campaigns and track each individual campaign.
They can accept ad requests by influencers for public campaigns.
Each Sponsor have:
Company Name / Individual Name
Industry
Budget
Influencers - an individual who has significant social media following
An influencer will receive ad requests, accept or reject ad requests, negotiate terms and resend modified ad requests back to sponsors.
They can search for ongoing campaigns (which are public), according to category, budget etc. and accept the request.
An influencer can update their profile page, which is publicly visible.
Each Influencer profile may have:
Name
Category
Niche

**Terminologies Used**
----------------------------
Ad request :
A contract between campaign and influencer, stating the requirements of the particular advertisement (E.g. show Samsung s23 in 3 videos for 10 seconds each), the amount to be paid etc.
Ad request have:
campaign_id (Foreign Key to Campaign table)
influencer_id (Foreign Key to Influencer/user table)
messages
requirements
payment_amount
status (Pending, Accepted, Rejected, Negotiating)
Campaign :
A container for ads requests for a particular goal (E.g. advertisement for Samsung s23). It can have multiple Ad requests, a campaign description, budget, ability to set public or private
Campaigns have:
name
description
start_date
end_date
budget
visibility (public, private)
goals

**Core Functionalities**
--------------------------
1. Admin login and user login (RBAC)
A login/register form with fields like username, password etc. for sponsor, influencer and admin login.
The application have only one admin identified by its role.
Used Flask security to implement role based access control.
2. Admin Dashboard - for the Admin
The admin will be added automatically whenever a new database is created.
Every new sponsor signup should be approved by the admin.
The request automatically go to the admin’s dashboard for approval.
The application have an admin dashboard which displays all the relevant statistics of the application, e.g. active users, campaigns (public/private), ad requests and their status, flagged sponsors/influencers etc.
3. Campaign Management - for the sponsors
Create a new campaign and categorize it into various niches.
Update an existing campaign - e.g. start_date, end_date, budget and/or other fields.
Delete an existing campaign.
4. Ad request Management - for the sponsors
Create ad requests based on the goals on the campaign
Edit an existing ad request - e.g. influencer_id, requirements, payment_amount, status
Delete an existing ad request.
5. Search for influencers, public campaigns
The sponsors is able to search for relevant influencers based on their niche, reach, followers etc.
The Influencers is able to search for public campaigns based on their niche, relevance etc.
6. Take action on a particular ad request - for the Influencers
Ability to view all the ad requests from all the campaigns.
Ability to accept/reject a particular ad request.
Ability to negotiate the “payment_amount” for a particular ad.
7. Backend Jobs
Scheduled Job - Daily reminders - The application should send daily reminders to influencers on g-chat using Google Chat Webhooks or SMS or mail
Check if an influencer has not visited/has pending ad request.
If yes, then send the alert asking them to visit/accept the ad request or checkout the public ad requests.
The reminder can be sent in the evening, every day (students can choose the time).
Scheduled Job - Monthly Activity Report - Device a monthly report for the sponsors created using HTML and sent via mail.
The activity report consist of campaign details, how many advertisements done, growth in sales of products due to campaigns, budget used/remaining etc.
For monthly report is sent, start a job on first day of every month → create a report using above parameters → send it as email
User Triggered Async Job - Export as CSV - Devise a CSV format details for the campaigns (public/private) created by the sponsor.
This export is meant to download the campaign details (description, start_date, end_date, budget, visibility (public, private), goals etc.
Have a dashboard from where the sponsor can trigger the export.
This should trigger a batch job, send an alert once done.
8. Performance and Caching
Added caching where required to increase the performance.
Added cache expiry.
API Performance.
Additonal Functionalities
Well designed HTML reports for Monthly activity report
Single Responsive UI for both Mobile and Desktop
Add to desktop feature
Implemented frontend validation on all the form fields using HTML5 form validation or JavaScript
Implemented backend validation within your APIs
Incorporated a proper login system to prevent unauthorized access to the app.
