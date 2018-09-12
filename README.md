# Deep-Learning-Project :collision:
![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/brain.jpeg)

## Introduction
With so many different IT-related job types in demand nowadays, it is hard for a
 fresh graduate or multi-skilled professional to determine where they would fit best.
 This problem is most apparent in today’s data-driven economy, where the job descriptions 
and roles are closely connected and often overlapping. Inspired by the discussion we had 
in the class about distinguishing the roles of the Data Scientist, Business Analyst, and 
Data Engineer, we are interested in determining what type of IT-related job would be the most 
suitable (in terms of skill-matching and job competence) for an IT professional, based on a text 
description that he might provide in his resume or cover letter. 

Our initial goal was to gather as many IT-related resumes as possible, along with the job title 
that their owners got hired for and use deep learning techniques to develop an artificial neural network 
that, once trained, would propose what kind of job title would be the most suitable given an individual’s 
resume or cover letter. Unfortunately, we were unable to collect resumes that were tagged with their actual
hiring position, so we decided to focus on job descriptions instead. We do this under the assumption that a
job description and a user’s resume/cover letter refer to the same context and should not be fundamentally 
too different, so we could theoretically still achieve our goal. As a result, a side-problem that could be 
answered is how to classify a job description into a specific IT-related category, i.e. how to determine the 
most suitable job type that a specific job posting refers to. This task could be very practical for any hiring 
agency that would be interested in performing automated tagging on a set of job descriptions that they have procured.


### Result Set Checker

Our main scraper is getting the job data by first creating queries for jobs.
These queries include the job title to search for, and the location (a city).
Indeed.com can return a maximum of 50 such results (if available) per result page,
but one issue is not all of the job results returned are available for scraping.

The issue might be because the layout they use is based on a different format
than the ones we look for, or because for some reason they are not able to open
at all (perhaps they were removed by the company).

So what this program does is that once all the queries for the job listings
that we will send are created, it checks if they contain a minimum number of
jobs that will be returned. This is useful because we might want to avoid
querying job titles that will have very few results, either in general or in
a specific city.

If so, it might be preferable to replace such a job with another, so that our
final dataset contains multiple job descriptions for each job title requested.

<b>How to use it</b>:

The main tuning of the program is done under the execution parameters block.
Once we have decided on which job titles will be queried (stored in the csv
under `job_titles_path`), and which cities we will search for, we need to
decide how many jobs we want to have for each job title in our dataset (e.g. 200).

Then, if we divide this number by the length of the `city_list`, we get the
correct `jobs_perQuery_perCity` parameter (e.g. 200 / 8 = 25).

To set the minimum number of jobs that must be received in each query sent,
use the `min_jobs_per_query` parameter. This should be higher than
`jobs_perTitle_perCity` by at least 5, because of the unexpected failures.

Once the checking starts, it might hang due to the server failing to respond
or it might get interrupted by us manually. So, to avoid starting all over, we
can use the `queries_completed` parameter to skip those and move forward faster.

### Scraper v2

The second version of our scraper was created to deal with the change in layout that
Indeed.com uses for many of its jobs. We can now capture two such HTML layouts, covering
most of the posted jobs in the site.

The code was also redesigned to allow for resuming the downloading from a saved checkpoint
in case an error has occurred previously and downloading stopped abruptly.

<b>How to use it</b>:

Under the execution parameters block we can tune everything to get the program to
work as required.

First, we specify the paths to the job titles that we will query for, and to the
result file that will be created or appended (in case it exists).

The cities list is critical, since along with the `jobs_perQuery_perCity` parameter
it controls how many jobs we want to have per each job title. For example, if we want
200 jobs for each title, we can set the parameter to 25 and have 8 cities that will
all have at least 25 such jobs in their query results. To check if this might not
hold, we can use the <b>Result Set Checker</b> program.

The `max_jobs_to_get` parameter can make the program stop earlier than it should
and might be useful to quickly test something in the result set. Otherwise, it should
be left as equal to `None`.

The `jobs_stored` and the `append_mode` parameters are the most important
to resuming downloading if required. The first should be set equal to the number of
jobs currently stored in the results .csv, and the second should be set to True if
we want to add more jobs. *It should only be set to False if we are starting a new
query from the beginning or if we want to overwrite the old results, so be careful!*

Finally, the `checkpoint_interval` is used to control how often the results are stored
in the .csv (thus creating a checkpoint for future resuming) and the `allow_duplicates`
is used to enable checking if the same job can be retrieved again (perhaps under a different job
title however) if it has already done so already. It should generally stay to False, unless
we want a slight improvement in performance. Note that if downloading is resumed, the previously
stored jobs are not checked under this condition.

## Datasets
The first step towards solving the aforementioned problem was to find the appropriate dataset. 
This quest was not as simple as one may think, because, even though there is a great abundance of sites that 
collect and present job-related information, they do not allow mass extraction of their datasets easily. However, 
after some research, we ended up using data from the online job-listing company indeed.com that provides unlimited 
and charge-free job-search services all over the world. The service requires simply that a user specify a keyword,
 and a geographic area and optionally other criteria the engine quickly responds with a number of job listings 
referring to openings that match the user’s request. Interestingly enough, Indeed.com follows only a small number 
of distinct HTML formats to display its listings, and so we managed to develop a web-scraper (aka web-crawler) that
 handled the job retrieval in an automated fashion while storing the results in a CSV flat file that we later 
processed for the modelling purposes.

However, even though the format of the job-offers’ data we found in indeed.com was the same at a high level 
(title, company, reviews, main body), the job descriptions themselves do not follow a fixed layout that we could 
further mine in order to retrieve specific semantics from each listing (such as skills, responsibilities, etc.). 
Instead, all of these were described in the main body of the offer according to the job-publishers’ discretion. 
As a result, we have only used the title and main body of the offer we selected. The final table the aforementioned 
scrapper returned had four columns:

* ID: a unique number enumerating the jobs extracted
* Search terms: the terms we have used to find the jobs; in other words, the job titles.
* Actual job titles: the titles of the jobs indeed.com returned. At this point we should note that the latter returns to the user results that either match exactly the given job title or they are close to it. For example, if we look for “Data Analyst” jobs we will also get “Business Analyst” jobs.
* Description: this is the main body of a job offer as it is displayed in indeed.com.

The main dataset consists of 10,000 distinct job postings/listings, from 25 different IT-related job types/categories. 
Those categories are mostly related to roles that we typically observe in the data-driven economy of today, along with a
few additions that will hopefully make the overall classification task more distinguishable (https://github.com/ggeop/Deep-Learning-Project/blob/master/Datasets/job_titles_IT.csv).
For comparison purposes, we also collected 9,900 more job postings from 25 generic (not only IT) job categories and ran our models on both to see how different they behave.

## Challenges in collecting the data
The main technical challenge was that a few months ago (May/June) Indeed was only using one HTML layout to present its job listings,
and thus it was very simple to collect the data using BeautifulSoup’s capabilities. In July however, we noticed that several errors were
occurring during the scraping and noticed that the unique layout had split into multiple ones. Lucky for us, the site still mainly uses 
two distinct layouts, and around 95% of its job listings can be scraped using second version we made of the Job Scraper script. Since the 
other layouts very seldom, we simply ignore any job listings posted under them.
The other main challenge has mainly to do with modelling, and it is more of an assumption. Initially, we had in mind to use the exact job titles 
of the jobs as our class labels (our y variable), but unfortunately we noticed that they are quite unique, and not general descriptions as we 
had hoped for. For example, out of a dataset with 1000 jobs, over 900 of those titles were appearing only once, even though they had all been scraped
from similar keywords. With so many labels, classification would be impossible. To deal with this, we made the assumption that Indeed’s internal 
engine / mechanism truly returns job descriptions that refer to the keyword used, and so we will be using those 25 keywords / job categories as the y labels 
for our classification purposes. In reality, this is not always true, but we chose to disregard it in order to start modelling and not spend more time and 
effort in the data procurement stage. Note: the job titles are actually stored by the scraper in the CSV, but completely ignored by our models. 
The keyword used (after some cleaning to make them meaningful is used instead – see data cleaning description).

## Models
We investigate different models with different parametes + hyper parameters, the following models are our main approaches:

* FFN Model (https://github.com/ggeop/Deep-Learning-Project/blob/master/Code/Keras-Models/FFN%20Model%20Testing.ipynb)
* RNN Model (https://github.com/ggeop/Deep-Learning-Project/blob/master/Code/Keras-Models/Keras%20First%20Go.ipynb)
* RNN Model + Embedding layer (https://github.com/ggeop/Deep-Learning-Project/blob/master/Code/Keras-Models/Second%20Model.ipynb)
* CNN Model (https://github.com/ggeop/Deep-Learning-Project/blob/master/Code/Keras-Models/Testing%20Area-CNN.ipynb)

### Best Model results
Finally, our best result was with simple RNN model (https://github.com/ggeop/Deep-Learning-Project/blob/master/Code/Keras-Models/Keras%20First%20Go.ipynb)
In the following images you can see the performance of the model in test & validation dataset

![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/model_accuracy.PNG)

![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/model_loss.PNG)

## Application
### Few words about it..
This online application gives to the user the ability to write in free text their skills (soft & technical)
and the application will recommend an appropriate job. The web interface is in Python Flask (http://flask.pocoo.org)
and the high-level neural network API is Keras, written in Python.

### Installation
We'll be making the assumption that Keras is already configured and installed on your machine. If not, please ensure you install Keras using the official install instructions.
From there, we'll need to install Flask (http://flask.pocoo.org) a Python web framework, so we can build our API endpoint. 

In our case we preffered to use the Anaconda Python enviroment (you can download it from https://www.anaconda.com/download).

### How to run it
Execute the app.py application and then open the submit page (http://127.0.0.1:5000/) of the application with a browser

### Screenshots
<b>The submit page of the application</b>
![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/insert_skills_1.jpg)

<b>The result page of the application</b>
![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/result_1.jpg)
