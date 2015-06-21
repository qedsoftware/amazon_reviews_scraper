DESCRIPTION
===============
Collects all reviews for an Amazon product. Uses the amazon_scraper Python module by Griffiths and Rehm.
Throughput rates will vary, but my own benchmark was roughly 4.15 reviews per second. The underlying Simple Product API returns reviews in batches of 10.


INSTALLATION
===============
0. (preferred, but not necessary) Create a virtual environment.
1. pip install -r requirements.txt
2. Register for Amazon's Product Advertising API:

    https://affiliate-program.amazon.com/gp/flex/advertising/api/sign-in.html.'

3. cp amazon.ini.example amazon.ini
4. Modify amazon.ini such that it uses the access keys you obtained after registration in step 2. 


AUTHORS
===============
[William Wu](http://qed.ai)
