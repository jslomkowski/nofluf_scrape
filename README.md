# Nofluf_scrape
Ever wonder what is the most popular skill that recruiters look for in their job descriptions? Ever wonder how much you can get paid? Fear no more because you have noflufjobs scraper only for educational purposes :)

## Installation
```bash
conda env create -f environment.yml
```

## Usage:
go to config.py and set the FIRST_PAGE as the first page of the category you want to scrape. Set NAME to your name of the category.

To get the list of jobs per selected category Run:
```bash
python list_scrape.py
```
to get the job description per the list of jobs Run:
```bash
python job_scrape.py
```
to get the details of each job Run:
```bash
python analyze.py
```
to get the results.

For the whole table with all scraped content go to `data/results/NAME/NAME_output.xlsx`

## todo: 
- [ ] make only 'on top' functionality.
- [ ] fix 'tasks' functionality. They are empty now.
