#Foreign Influence

This project is the data-entry and scraping scripts that generate an API and will power a Foreign Influence Explorer website. See the front-facing app [here](https://github.com/sunlightlabs/bulgogi).

Foreign Influence Explorer documents some of the ways foreign entities influence U.S. policy and opinions. The two main datasets are the Department of Justice's Foreign Agent Registration Act(FARA) and press releases from The Defense Security Cooperation Agency(DSCA) records. 

##FARA Records

The management command create_feed, in the fara_feed app, scrapes the PDFs from the DOJ. Web forms in the FaraData app create pages for people to normalize the data according to instructions. The project uses a sql database. The data can be accesses through the API and RSS feeds. 

##DSCA Records

The arms_sales app scrapes press releases from the DSCA for proposed arms sales. These sales are purposed and may not happen, but these documents can add context to some of the lobbying that is visible in the FARA dataset. 

---

This is project is under construction. If you are interested in contributing in some way email Lindsay at lyoung@sunlightfoundation.com