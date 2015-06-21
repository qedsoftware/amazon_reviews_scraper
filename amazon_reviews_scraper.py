#-*- coding: utf-8 -*-
#!/usr/bin/env python
from configparser import ConfigParser, ExtendedInterpolation
import sys
import amazon_scraper
import time
import datetime
import logging.config
import os.path


class AmazonReviewScraper:

    def __init__(
            self, access_key, secret_key, assoc_tag, logger=None, debug=False):
        self.amzn = amazon_scraper.AmazonScraper(
            access_key,
            secret_key,
            assoc_tag)
        self.logger = logger or logging.getLogger(__name__)
        logging.config.fileConfig(
            os.path.join(
                os.path.dirname(__file__),
                "logging.ini"))
        self.debug = debug

    def _encode_safe(self, s):
        if s:
            return s.encode('utf-8')
        else:
            return ""

    def process_reviews(self, rs, fh):
        """
        Inputs: Amazon Reviews object, and a filehandle.
        Output: Returns number of reviews processed. Writes reviews to file.
        """
        for r in rs.all_reviews:
            if self.debug:
                try:
                    logging.debug(
                        "{} | {} | {} | {}".format(
                            r.id, r.date, self._encode_safe(
                                r.author), self._encode_safe(
                                r.text)))
                except:
                    logging.warn(
                        'Encoding problem with review {}'.format(
                            r.id))
            fh.write(r.date.strftime('%Y-%m-%d') + '\n')
        fh.flush()
        return len(rs.all_reviews)

    def fetch_reviews(self, item_id, filename=None):
        """
        Fetches reviews for the Amazon product with the specified ItemId. 
        Writes processed versions of records to file with specified filename.
        """
        if not filename:
            filename = "{}_{}.txt".format(
                item_id,
                datetime.datetime.now().strftime('%Y-%m-%d'))
        start = time.time()
        p = self.amzn.lookup(ItemId=item_id)
        rs = self.amzn.reviews(URL=p.reviews_url)
        count = 0
        with open(filename, "w") as fh:
            while True:
                count += self.process_reviews(rs, fh)
                rs = self.amzn.reviews(URL=rs.next_page_url)
                logging.info(
                    "{}: processed {} reviews ...".format(
                        item_id,
                        count))
                if not rs.next_page_url:
                    self.process_reviews(rs, fh)
                    logging.info(
                        "{}: processed {} reviews ... finished!".format(
                            item_id,
                            count))
                    break
        end = time.time()
        logging.info(
            "Collected {} reviews for item {} in {} seconds".format(
                count,
                item_id,
                end -
                start))


if __name__ == "__main__":

    conf_file = "amazon.ini"
    conf = ConfigParser(interpolation=ExtendedInterpolation())
    try:
        conf.read(conf_file)
    except:
        sys.exit('Cannot read configuration file %s; exiting.' % conf_file)
    try:
        # str() is used to avoid HMAC-related unicode error
        AMAZON_ACCESS_KEY = str(conf.get('amazon', 'AMAZON_ACCESS_KEY'))
        AMAZON_SECRET_KEY = str(conf.get('amazon', 'AMAZON_SECRET_KEY'))
        AMAZON_ASSOC_TAG = str(conf.get('amazon', 'AMAZON_ASSOC_TAG'))
    except:
        sys.exit("Bad configuration file; exiting.")

    a = AmazonReviewScraper(
        AMAZON_ACCESS_KEY,
        AMAZON_SECRET_KEY,
        AMAZON_ASSOC_TAG,
        debug=True)
    # a.fetch_reviews('B001L5TVGW') # >3K reviews
    a.fetch_reviews('B00J5GH3ZK') # <100 reviews
