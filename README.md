# Deep-Learning-Project :collision:
![alt text](https://github.com/ggeop/Deep-Learning-Project/blob/master/Images/brain.jpeg)
About the project...to be added soon!

## Code Files Manual

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
