from GroupsResults import GroupsResults

def main():

    years = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    for year in years:
        url_to_scrape = f"https://en.wikipedia.org/wiki/{year}%E2%80%93{str((year + 1))[-2:]}_UEFA_Champions_League_group_stage?fbclid=IwAR1e5VgehDiy3rmX4QJAWOpNecrLKPgOIt-NCgrCEuV0zclPVTyqZh706Ro#External_links"
        scraper = GroupsResults(url_to_scrape)
        scraper.scrape(year)

if __name__ == "__main__":
    main()
