# RNA Representative Set

This package is a utility tool for the releases found in the [Representative Sets of RNA 3D Structures](http://rna.bgsu.edu/rna3dhub/nrlist).

There is one file, `representative_set.py`, with two classes:
* `Representatives`
* `RepresentativeSet`

For the most part, you should only use `Representatives`. The `RepresentativeSet` methods parse the live web page, which isn't very fast. The `Representatives` class persists the data parsed from the webpage so the website doesn't have to be scraped more than once.

## How to use it

First, create an instance of the `Representatives` class:
```python
reps = Representatives()
```

The default instantation (i.e., creating an instance with no input parameters to the constructor) will parse the webpage's latest release and the 4.0A resolution cutoff. You can get whatever release and cutoff you want though. Here are some examples:

```python
# Get latest data
reps = Representatives()

# Get latest data at 20.0A resolution cutoff
reps = Representatives(resolution_cutoff="20.0A")

# Get release 3.292 with default 4.0A resolution cutoff
reps = Representatives(relase_id="3.292")

# Get release 3.292 with 20.0A resolution cutoff
reps = Representatives(relase_id="3.292", resolution_cutoff="20.0A")
```

After creating a `Representatives` object, you now have access to two methods:
* `get_rep_for`
* `get_unique_reps_from_list`

The `get_rep_for` method takes an entry and returns the representative PDB ID for it. For example:

```python
reps = Representatives()
constituent = "7P8Q|1|B"
rep = reps.get_rep_for(constituent)
print(rep) # Outputs "6E0O"
```

The method `get_unique_reps_from_list` takes in a list of entries and returns a unique set of PDB IDs. For example:

```python
reps = Representatives()

list_of_constituents = [
    "1VQ6|1|4", # Repped by 1VQ6
    "6OY5|1|I", # Repped by 6N6I
    "7MQC|1|B" # Repped by 6N6I
]

rep_set = reps.get_unique_reps_from_list(list_of_constituents)

print(rep_set) # Outputs {1VQ6, 6N61}
```

Note that even though the method was passed three entries, it only returns two IDs because two of the entries are represented by the same PDB ID.

## How it works

The classes here parse the data on the linked page. Basically, it creates a huge dictionary. The keys for this dictionary are all of the individual entries in the "Class members" column. The value for each of those keys is whatever the PDB ID in the "Representative" column is.

## Warnings!!!!

### Release Versions

The default behavior of this package is to grab the most recent data published on the RNA3DHub list here: http://rna.bgsu.edu/rna3dhub/nrlist

They try to release a new version every week, so the data you grabbed a few weeks ago may be different from the data you grab today! Please keep this in mind and save the release ID and cutoff (default is 4.0A) that you used.

### Testing

I have only tested a few combinations of release IDs and cutoffs. There may be issues with older versions of releases. There is some error-handling and fault-detection baked into the package, but it's not perfect.
