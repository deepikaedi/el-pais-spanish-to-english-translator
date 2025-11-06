# El pais spanish to english translator

This Assignment or project automates the process of scraping articles from spanish to english  from the opinion section of the spanish website
It demonstrates skills in "selenium automation, web scraping, API Testing and browser stack testing "

# Tech used are 
--python 3
-- selenium 4
-- google translate API (via google trans of deep-translator)
--requests

# working
1. It launches a remote chrome browser on Browserstack platform using selenium web driver(remote).
2. It opens the "el pais Opinion section" website
3. Then it scrapes the first five valid article titles and content in Spanish language.
4. After that it translates the article titles in to English language.
5. Then it analyzes the titles which are translated for words that appear more than twice
6. Then it prints the results

# Running of the application/code
install the google trans version of 4.0.0-rc1 requests
replace the username and accesskey with your credentials (you can find from the browserstack dash board)


