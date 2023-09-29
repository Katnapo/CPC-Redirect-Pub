# CPC-Redirect
Code for childsplay's redirect service. 

This service was mainly in use from September 2022 to Feburary 2023 and handled 100,000+ requests.

####

Context - Childsplay Clothing sell designer children's clothing. They have a website for each country they sell to.
For example, they have a website for the UK, USA, France, Germany, etc.

This service came about from a dilemma; Childsplay were posting products to their instagram page - some products had
links that sent the user to the product page on the website, however, this wouldn't necessarily be the correct country
website for the user as by default only the UK website was used. This meant that users from the USA, for example, would
be sent to the UK website; this would of lead to a poor user experience where users would of had to manually change
the country website, perhaps after building a cart of items (which wouldn't of been saved when changing country).

This service was created to solve this problem. It was a redirect service that would redirect the user to the correct
country website based on their location. 

####

For the sake of security, certain files have been modified as to not expose keys and other sensitive information.

While the code is technically still live and the domain is still active, a new website
was created for Childsplay Clothing resulting in this service becoming defunct.

Most of the html was generated by one of the website designers at Childsplay and was not created by myself.

It's worth noting that database components from this service are similar and/or identical to components used in
other Childsplay projects at the time. This was just a simple way of reusing code and saving time.

####
