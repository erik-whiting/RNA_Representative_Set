import requests

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class RNARepresentativeSet:
    def __init__(self, release_id=None, resolution_cutoff="4.0A"):
        self.parser = WebsiteParser
        self.rep_set, self.chain_info = WebsiteParser.get_by_release(release_id=release_id, resolution_cutoff=resolution_cutoff)
        pdb_ids = set()
        for rs in list(self.chain_info.keys()):
            pdb_ids.add(rs[:4])
        self.pdb_ids = list(pdb_ids)

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

    def __getitem__(self, key):
        try:
            return self.chain_info[key]
        except KeyError:
            return False


# Utility class, use `RNARepresentativeSet` if you only need to parse the webpage once
class WebsiteParser:
    base_url = "http://rna.bgsu.edu/rna3dhub/nrlist"
    resolution_cutoffs = ["1.5A", "2.0A", "2.5A", "3.0A", "3.5A", "4.0A", "20.0A", "all"]

    @staticmethod
    def get_latest_release():
        print("Getting latest release number")
        url = WebsiteParser.base_url
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
        if resolution_cutoff not in WebsiteParser.resolution_cutoffs:
            raise Exception(f"Resolution cutoff {resolution_cutoff} must be in {WebsiteParser.resolution_cutoffs}")

        if not release_id:
            release_id = WebsiteParser.get_latest_release()

        release_url = f"{WebsiteParser.base_url}/release/{release_id}/{resolution_cutoff}"
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
        chain_dict = {}
        row_counter = 1
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

            info_box = d[1]
            k = info_box.split()[0]
            info = info_box.split(k)[1].strip()
            pdb_id = info[0:6]
            info = info.split(pdb_id)[1].strip()
            pdb_id = pdb_id[1:5]
            row = str(rows[row_counter])
            info_box = row.split("<td>")[3]
            line_items = info_box.split("<ul>")[1]
            line_items = line_items.split("<li>")
            line_items.remove("")
            chain_info = []
            for li in line_items:
                chain_info.append(li.replace("</li>", "").replace("</ul></td>", ""))
            chain_dict[k] = {"pdb_id": pdb_id, "info": chain_info}
            row_counter += 1
            for c in constituents:
                rep_set[c] = rep_id

        return rep_set, chain_dict
