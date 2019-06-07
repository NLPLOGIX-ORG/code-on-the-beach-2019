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
    buildingtypename: str = None
    buildingstylecode: str = None
    buildingclasscode: str = None
    qualitycode: str = None
    actualyearbuilt: int = None
    effectiveyearbuilt: int = None
    buildingvalue: float = 0.0
    buildingheatedarea: str = None

    #00007
    bedrooms:   int = 0
    bathrooms:  int = 0
    rooms:      int = 0
    stories:    int = 0

    #00009
    condo_bedrooms:   int = 0
    condo_bathrooms:  int = 0

    #00010
    amenityitemcode: str = None

    #00015
    exemptioncode: str = None  

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

            if self.sitezipcode is not None:
                self.sitezipcode = self.sitezipcode.split('-')[0]
                self.sitezipcode = self.sitezipcode.replace(' ', '')

            return

        if rowtype == "00005":
            assert len(colvalues) == 9,"row type of {} should have a length of 9 but has a length of {}".format(rowtype, len(colvalues))

            self.buildingtypecode       = colvalues[0]
            self.buildingtypename       = colvalues[1]
            self.buildingstylecode      = colvalues[2]
            self.buildingclasscode      = colvalues[3]
            self.qualitycode            = colvalues[4]
            self.actualyearbuilt        = int(colvalues[5])
            self.effectiveyearbuilt     = int(colvalues[6])
            self.buildingvalue          = float(colvalues[7])
            self.buildingheatedarea     = colvalues[8]

            return

        if rowtype == "00007":

            #if we are not a condo then get the bedrooms and bethrooms from here
            if self.buildingtypecode != 401:
                code     = colvalues[0]
                colvalue = colvalues[1].strip().replace('\n', '') if colvalues[1] is not None else None
                if code == 'BR':
                    self.bedrooms = int(float(colvalue)) if colvalue is not None else 0

                if code == 'BT':
                    self.bathrooms = int(float(colvalue)) if colvalue is not None else 0
                    if self.bathrooms == 129:
                        print("{} - {} - {}".format(self.parcelnumber, self.buildingtypecode, colvalues))

                if code == 'SH':
                    self.stories = int(float(colvalue)) if colvalue is not None else 0

                if code == 'RM':
                    self.rooms = int(float(colvalue)) if colvalue is not None else 0

        if rowtype == "00009":
            assert len(colvalues) == 2,"row type of {} should have a length of 2 but has a length of {}".format(rowtype, len(colvalues))
            
            self.condo_bedrooms       = int(float(colvalues[0])) if colvalues[0] is not None and colvalues[0].strip() != '' else 0
            self.condo_bathrooms      = int(float(colvalues[1])) if colvalues[1] is not None and colvalues[1].strip() != '' else 0

            return

        if rowtype == "00010":
            assert len(colvalues) == 1,"row type of {} should have a length of 1 but has a length of {}".format(rowtype, len(colvalues))

            self.amenityitemcode    = colvalues[0]
            
            return

        if rowtype == "00015":
            assert colvalues is None or len(colvalues) == 1,"row type of {} should have a length of 1 but has a length of {}".format(rowtype, len(colvalues))

            self.exemptioncode    = colvalues[0] if colvalues is not None else None
            
            return       

    def isreadyforinsert(self):
        supported_building_types = [
            'SFR 1 STORY', 
            #'MH UNASSESSED', 
            #'MH ASSESSED', 
            'SFR 2 STORY',
            'SFR SPLIT-LEVEL', 
            'GARAGE APT', 
            #'WHSE MINI', 
            # 'WHSE PREFAB',
            'SFR CLASS 2', 
            #'SERV GAR / VEH RP', 
            'SFR 3 STORY', 
            #'TRIPLEX',
            #'CONVERTED RESIDENCE', 
            #'CHURCH', 
            # 'UTILITY BLDG', 
            'TOWNHOUSE',
            #'STORE RETAIL', 
            # 'DUPLEX', 
            'CONDOMINIUM', 
            #'WHSE SHELL', nan, 
            # 'MOTEL',
            #'DAY CARE CTR', 
            # 'ROOMING HOUSE', 
            # 'QUADRUPLEX', 
            # 'OFFICE 1-2 STY',
            'SFR CLASS 3', 
            'APTS  1-3 STORY', 
            #'WHSE STORAGE', 
            'COOP APARTMENT',
            #'CONDO GAR/CP'
        ]

        #ignore 3901 Motel
        return self.exemptioncode in  ["HB", "HX"] and self.parcelnumber is not None and self.buildingtypename in supported_building_types

    def toarray(self):
        is_condo = self.buildingtypecode == 401

        num_bedrooms   = self.condo_bedrooms if is_condo else self.bedrooms
        num_bathrooms  = self.condo_bathrooms if is_condo else self.bathrooms

        
        result = [
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
            self.buildingtypename,
            self.buildingstylecode,
            self.buildingclasscode,
            self.qualitycode,
            self.actualyearbuilt,
            self.effectiveyearbuilt,
            self.buildingvalue,
            self.buildingheatedarea,

            #00007
            num_bedrooms,
            num_bathrooms,
            self.rooms,
            self.stories,
            
            #00010
            self.amenityitemcode,

            #00015
            self.exemptioncode                       
        ]

        return result


    def column_to_string(self, x):
        if isinstance(x, str):
            return '"' + x + '"'

        if x is None:
            return ''

        return str(x)

    def to_string(self):
       return '|'.join([self.column_to_string(x) for x in self.toarray()])