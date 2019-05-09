from dataclasses import dataclass

@dataclass
class Record:
    '''Class for inserting a row into a file'''
    #00001
    parcelnumber: str = None
    section: str = None
    township: str = None
    totalmarketvalue: float = 0.0
    assessedvalue: float = 0.0
    totaljustvalue: float = 0.0
    docacres: str = None

    #00004
    siteaddressnumber: str = None
    siteaddressstreetname: str = None
    siteaddressstreettype: str = None
    siteaddressunitnumber: str = None
    siteaddresscity: str = None
    sitezipcode: str = None
    buildingnumber: str = None

    #00005
    buildingtypecode: str = None
    buildingstylecode: str = None
    buildingclasscode: str = None
    qualitycode: str = None
    actualyearbuilt: int = None
    effectiveyearbuilt: int = None
    buildingvalue: float = 0.0
    buildingheatedarea: str = None

    #00007
    bedrooms:   int = -1
    bathrooms:  int = -1
    rooms:      int = -1
    stories:    int = -1

    #00010
    amenityitemcode: str = None

    #00015
    exemptioncode: str = None

    #00017
    dateofsale: str = None
    saleprice: float = 0.0

    def update(self, rowtype, colvalues):
        if rowtype == "00001":
            assert len(colvalues) == 7,"row type of {} should have a length of 7 but has a length of {}".format(rowtype, len(colvalues))
            self.parcelnumber       = colvalues[0]
            self.section            = colvalues[1]
            self.township           = colvalues[2]
            self.totalmarketvalue   = float(colvalues[3])
            self.assessedvalue      = float(colvalues[4])
            self.totaljustvalue     = float(colvalues[5])
            self.docacres           = colvalues[6]

            return

        if rowtype == "00004":
            assert len(colvalues) == 7,"row type of {} should have a length of 7 but has a length of {}".format(rowtype, len(colvalues))

            self.siteaddressnumber      = colvalues[0]
            self.siteaddressstreetname  = colvalues[1]
            self.siteaddressstreettype  = colvalues[2]
            self.siteaddressunitnumber  = colvalues[3]
            self.siteaddresscity        = colvalues[4]
            self.sitezipcode            = colvalues[5]
            self.buildingnumber         = colvalues[6]

            return

        if rowtype == "00005":
            assert len(colvalues) == 8,"row type of {} should have a length of 8 but has a length of {}".format(rowtype, len(colvalues))

            self.buildingtypecode       = colvalues[0]
            self.buildingstylecode      = colvalues[1]
            self.buildingclasscode      = colvalues[2]
            self.qualitycode            = colvalues[3]
            self.actualyearbuilt        = int(colvalues[4])
            self.effectiveyearbuilt     = int(colvalues[5])
            self.buildingvalue          = float(colvalues[6])
            self.buildingheatedarea     = colvalues[7]

            return

        if rowtype == "00007":

            code     = colvalues[0]
            colvalue = colvalues[1].strip().replace('\\n', '') if colvalues[1] is not None else None
            if self.bedrooms < 1 and code == 'BR':
                self.bedrooms = int(float(colvalue)) if colvalue is not None else 0

            if self.bathrooms < 1 and code == 'BT':
                self.bathrooms = int(float(colvalue)) if colvalue is not None else 0

            if self.stories < 1 and code == 'SH':
                self.stories = int(float(colvalue)) if colvalue is not None else 0

            if self.rooms < 1 and code == 'RM':
                self.rooms = int(float(colvalue)) if colvalue is not None else 0

        if rowtype == "00009":
            assert len(colvalues) == 3,"row type of {} should have a length of 3 but has a length of {}".format(rowtype, len(colvalues))
            
            self.area       = int(colvalues[2]) if colvalues[2] is not None and colvalues[2].strip() != '' else 0

            return

        if rowtype == "00010":
            assert len(colvalues) == 1,"row type of {} should have a length of 1 but has a length of {}".format(rowtype, len(colvalues))

            self.amenityitemcode    = colvalues[0]
            
            return

        if rowtype == "00015":
            assert colvalues is None or len(colvalues) == 1,"row type of {} should have a length of 1 but has a length of {}".format(rowtype, len(colvalues))

            self.exemptioncode    = colvalues[0] if colvalues is not None else None
            
            return

        if rowtype == "00017":
            assert len(colvalues) == 2,"row type of {} should have a length of 2 but has a length of {}".format(rowtype, len(colvalues))

            self.dateofsale = colvalues[0]
            self.saleprice  = float(colvalues[1])
            
            return

    def isreadyforinsert(self):
        return self.dateofsale is not None and self.saleprice is not None

    def toarray(self):
        return [
            #00001
            self.parcelnumber,
            self.section,
            self.township,
            self.totalmarketvalue,
            self.assessedvalue,
            self.totaljustvalue,
            self.docacres,

            #00004
            self.siteaddressnumber,
            self.siteaddressstreetname,
            self.siteaddressstreettype,
            self.siteaddressunitnumber,
            self.siteaddresscity,
            self.sitezipcode,
            self.buildingnumber,

            #00005
            self.buildingtypecode,
            self.buildingstylecode,
            self.buildingclasscode,
            self.qualitycode,
            self.actualyearbuilt,
            self.effectiveyearbuilt,
            self.buildingvalue,
            self.buildingheatedarea,

            #00007
            self.bedrooms,
            self.bathrooms,
            self.rooms,
            self.stories,
            
            #00010
            self.amenityitemcode,

            #00015
            self.exemptioncode,
            
            #00017
            self.dateofsale,
            self.saleprice
        ]