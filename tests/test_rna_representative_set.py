from RNARepresentativeSet import RNARepresentativeSet

class TestRNARepresentativeSet:
    reps = RNARepresentativeSet()

    def test_get_item(self):
        representative = self.reps["5XXB|1|1+5XXB|1|4"]
        pdb_id = representative["pdb_id"]
        assert(pdb_id == "5XXB")
        expected_info = [
            '25S RNA, 5.8S RNA',
            'Electron microscopy',
            'Release Date: 2017-08-30',
            'Standardized name:  LSU rRNA +  5.8S rRNA',
            'Source: Eukarya',
            'Rfam: RF02543 + RF00002'
        ]
        info = representative["info"]
        assert(info == expected_info)
