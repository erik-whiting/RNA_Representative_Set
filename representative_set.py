import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# Make an instance of this class if you're going to do many operations. The
# static class in this file will query and parse the BGSU page for pretty much
# every operation. Parsing takes ~30 seconds, so this class persists the data
# from the first call to make subsequent calls faster.
class Representatives:
    def __init__(self, release_id=None, resolution_cutoff="4.0A"):
        self.rs = RepresentativeSet
        self.rep_set = RepresentativeSet.get_by_release(release_id=release_id, resolution_cutoff=resolution_cutoff)

    def get_unique_reps_from_list(self, list_of_etnries):
        unique_reps = set()
        for entry in list_of_etnries:
            rep = self.get_rep_for(entry)
            if rep:
                unique_reps.add(rep)

        return unique_reps

    def get_rep_for(self, entry):
        rep = ""
        try:
            rep = self.rep_set[entry]
        except KeyError:
            # No representative, return false
            rep = False
        return rep


# Utility Class, use `Representatives` if you're going to parse the release data many times
class RepresentativeSet:
    base_url = "http://rna.bgsu.edu/rna3dhub/nrlist"
    resolution_cutoffs = ["1.5A", "2.0A", "2.5A", "3.0A", "3.5A", "4.0A", "20.0A", "all"]

    @staticmethod
    def get_latest_release():
        print("Getting latest relase number")
        url = RepresentativeSet.base_url
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.table
        tds = table.find_all("td")
        latest_release_url = tds[0].find("a").get("href")
        latest_release = latest_release_url.split("/")[-1]
        return latest_release


    @staticmethod
    def get_by_release(release_id=None, resolution_cutoff="4.0A"):
        # Clean and validate parameters
        if type(resolution_cutoff) == int:
            resolution_cutoff = f"{resolution_cutoff}.0A"
        if type(resolution_cutoff) == float:
            resolution_cutoff = f"{resolution_cutoff}A"

        if resolution_cutoff.lower() == "all":
            resolution_cutoff = resolution_cutoff.lower() # The URL ends with "/all"
        else:
            resolution_cutoff = resolution_cutoff.upper()
        if resolution_cutoff not in RepresentativeSet.resolution_cutoffs:
            raise Exception(f"Resolution cutoff {resolution_cutoff} must be in {RepresentativeSet.resolution_cutoffs}")

        if not release_id:
            release_id = RepresentativeSet.get_latest_release()

        release_url = f"{RepresentativeSet.base_url}/release/{release_id}/{resolution_cutoff}"
        print(f"Getting data from URL: {release_url}, this will take a minute or so ...")
        html = requests.get(release_url).content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.table
        rows = table.find_all("tr")
        data = []
        # Clean HTML tags from data
        print("Cleaning HTML data")
        for i in range(1, len(rows)):
            row = rows[i]
            cols = row.find_all("td")
            cols.pop(0) # Get rid of row-number column, because who cares?
            cols = [el.text.strip() for el in cols]

            data.append([el for el in cols if el])

        # Get list of representative PDB IDs
        data_size = len(data)
        print(f"Building representative set from {data_size} represntatives")
        rep_set = {}
        for d in data:
            rep_id = d[1].split("(")[1].split(")")[0]
            spl = d[4].split(",")
            spl2 = spl[0].split(" ")
            count_of_constituents = int(spl2[0][1:-1])
            spl[0] = spl2[1]
            constituents = []
            for s in spl:
                constituents.append(s.strip())
            if len(constituents) != count_of_constituents:
                message = f"Constituents: {len(constituents)}, count: {count_of_constituents}\n"
                message += f"On Representative ID {rep_id}\n"
                message += f"{constituents}\n"
                raise Exception(f"Bad split, the developer did something wrong.\n{message}")

            for c in constituents:
                rep_set[c] = rep_id

        return rep_set


# Testing
reps = Representatives()
constituent = "7P8Q|1|B"
expected = "6E0O"
print(f"Get unique representative for {constituent}. It should be {expected}")
rep = reps.get_rep_for(constituent)
print(f"Representative is {rep}")


list_of_constituents = [
    "1VQ6|1|4", # Repped by 1VQ6
    "6OY5|1|I", # Repped by 6N61
    "7MQC|1|B", # Repped by 6N61
    "1PVO|1|L", # Repped by 1PV0
    "4NIA|1|7"  # Repped by 6D30
]
print("Get a set of unique representatives given a list of constituents")
print(f"List: {list_of_constituents}")
rep_set = reps.get_unique_reps_from_list(list_of_constituents)
print(f"Unique list: {rep_set}")
print(f"We expect 1VQ6, 6N61, 1PV0, 6D30 (in any order)")
