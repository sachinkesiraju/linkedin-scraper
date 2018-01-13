# linkedin-scraper

This script allows you to scrape the employee breakdown from a company's linkedin page.

Simply fill in your linkedin login credentials in the empty fields in the scraper file, add a list of companies to `companies.csv` and run `python linkedin_scraper.py`

Upon running the script, `company_details.csv` should have a record similar to this.

| company_name | num_employees | past_companies                               | past_schools                                                                                                                                  |
|--------------|---------------|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Stripe       | 831           | Google, Twitter, Stripe, Facebook, Microsoft | Stanford University, University of California, Berkeley, Massachusetts Institute of Technology, University College Dublin, Harvard University |


<br>
Available under the MIT License. For more information, see the <a href="https://github.com/sachinkesiraju/linkedin-scraper/LICENSE">LICENSE</a> file.
