import os
import copy
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)  # sample_pagerank function
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)  # iterate_pagerank function
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # create dict where probability distribution will be returned.
    distribution = {}
    
    # check to see if there are links in the current page by measuring the length of the value for the page's key.
    if len(corpus[page]) > 0:
        
        # divide probability of (1-d) among all of the pages in the corpus
        for webpage in corpus:
            distribution[webpage] = (1-damping_factor) / len(corpus)

            # check to see if this page is also a link on the current page
            if webpage in corpus[page]:

                # add the adjusted probability to it's distribution
                distribution[webpage] += damping_factor / len(corpus[page])  # this divides the damping factor among all links on current page.

    #if not choose randomly among all pages in the corpus
    else:
        for webpage in corpus:
            distribution[webpage] = 1 / len(corpus)  # divide prob evenly among all pages in corpus

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # delcare dict that will be returned, set up count trackers
    distribution = {}

    for page in corpus:
        distribution[page] = 0

    # set up the start of the loop with the random page
    current_page = None

    # track the samples
    sample_count = 0

    # loop through and run samples
    while sample_count < n:

        # check if it is the start of the sample, if yes generate random page
        if current_page == None:

            current_page = random.choice(list(corpus.keys()))  # generate random page
            distribution[current_page] += 1  # update the distribution count for this page
            sample_count += 1  # track the sample count

        else:
            # get the transition model for the current page
            tm = transition_model(corpus, current_page, damping_factor)

            # pull out values from model and cach it in a list, will be passed into next line of code
            sequence = list(tm.keys())
            weights = list(tm.values())
            
            # make a weighted random choice among the transition model. 
            weighted_choice = random.choices(sequence, weights, k=1)  # k is the length of the return value. We only want one value. 
            current_page = weighted_choice.pop()  # the line above returns a list with one item. Which is no bueno for indexing into the dict

            # update the counts
            distribution[current_page] += 1
            sample_count += 1
    

    # do some math to convert counts to percentages
    for page in corpus:
        distribution[page] = distribution[page] / n

    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # STEP 1: The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.

    distribution = {}  # dict to store the rank distributions
    changes = {}  # dict to log changes as the distributions update

    # set initial page ranks and set change values to a value higher than .001
    for page in corpus:
        distribution[page] = 1 / len(corpus)
        changes[page] = 1

    # STEP 2: The function should then repeatedly calculate new rank values based on all of the current rank values    

    # continuos loop until changes are less than .001
    while any(change > .001 for change in changes.values()):

        # loop through each page
        for page in corpus.keys():

            # set variable for added probability taken from all webpages linking to current page
            probability = 0

            # run a second loop to identify which webpages are linking to current page
            for webpage, links in corpus.items():

                # check if the webpage has any links. If not then it links to every page in the corpus.
                if not links:
                    links = corpus.keys()

                # check to see if the current page is being linked to
                if page in links:

                    # run the second part of the equation to determine added probability
                    probability += distribution[webpage] / len(links)
                
            # complete the equation, save it in new variable to track changes
            new_distribution = ((1 - damping_factor) / len(corpus)) + (damping_factor * probability)

            # track changes
            changes[page] = abs(new_distribution - distribution[page])
            
            # update the dict
            distribution[page] = new_distribution

            
    return distribution



if __name__ == "__main__":
    main()
