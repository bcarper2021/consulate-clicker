# consulate-clicker
Script to check the Spanish consulate appointment website for cancellations on specified dates, and book the appointment for the user

Implements Selenium WebDriver and Twilio text message notification API

Requests are intentionally delayed and spaced out as to not add extra strain to the appointment server. The script checks approximately every 30 seconds and is intended for only a single user at a time.
