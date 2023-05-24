# Nofluf_scrape
Ever wonder what is the mos popular skill that recruiters look for in their job descriptions? Ever wander how much you can get paid? Fear no more because you have noflufjobs scraper only for ducation purposes :)

## Instalation
```bash
conda env create -f environment.yml
```

## Usage:
go to config.py and set the FIRST_PAGE as first page of category you want to scrape. Set NAME to your own name  of the category.

Run list_scrape.py to get the list of all jobs in that category. Run job_scrape.py to get the details of each job. Run analyze.py to get the results.

## todo: 
- [] make only 'on top' functionality.
- [] fix 'tasks' functionality. They are empty now.
