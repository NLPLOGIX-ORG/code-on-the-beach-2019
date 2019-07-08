class Features:

   def _isTownhouse(self, val):
      return 1 if val == "TOWNHOUSE" else 0

   def _isCondo(self, val):
      return 1 if val == "CONDOMINIMUM" else 0

   def _isSingleFamily(self, val):
      singlefamilytypes = [
          "SFR 1 STORY",
          "SFR 2 STORY",
          "SFR 3 STORY",
          "SFR CLASS 2",
          "SFR CLASS 3",
          "SFR SPLIT-LEVEL"
        ]

      return 1 if val in singlefamilytypes else 0

   def _isJacksonville(self, val):
      jacksonvillelocations = [
          "JACKSONVILLE",
          "JACKSONVILLE        ",
          "JACKOSNVILLE"
      ]

      return 1 if val in jacksonvillelocations else 0

   def _isAtTheBeach(self, val):
      
      return 1 if "beach" in val.lower() else 0

   def _isPontevedra(self, val):
      
      return 1 if val == "PONTE VEDRA" in val else 0

   def _computeZone(self, df):
      
      zone1 = [32202, 32206,32204,32254, 32209, 32208]
      zone2 = [32207, 32216, 32246, 32224, 32225,32211,32277]
      zone3 = [32217, 32257, 32223, 32258, 32256]
      zone4 = [32205, 32210, 32212, 32244, 32222, 32221, 32215]
      zone5 = [32234, 32009, 32220, 32219, 32218,32226]

      df["HZ1"] = df["Site Zip Code"].apply(lambda x: 1 if x in zone1 else 0)
      df["HZ2"] = df["Site Zip Code"].apply(lambda x: 1 if x in zone2 else 0)
      df["HZ3"] = df["Site Zip Code"].apply(lambda x: 1 if x in zone3 else 0)
      df["HZ4"] = df["Site Zip Code"].apply(lambda x: 1 if x in zone4 else 0)
      df["HZ5"] = df["Site Zip Code"].apply(lambda x: 1 if x in zone5 else 0)

      return df

   def _computeAdjustedAreaZip(self, df):

      AA_Zscore = lambda x: (x - x.mean())/x.std()
      df['AdjustedArea_ZIP'] = df.groupby(df['Site Zip Code'])['building heated area'].transform(AA_Zscore)

      return df

   def _computeAdjustedAreRooms(self, df):
     
      AA_Zscore = lambda x: (x - x.mean())/x.std()
      df['AdjustedArea_Rooms'] = df.groupby(df['Number Of Rooms'])['building heated area'].transform(AA_Zscore)

      return df

   def compute(self, df):

       df["LastReno"]           = df['effective year built'] - df['actual year built']
       df["IsTownhouse"]        = df["building type name"].apply(lambda x: self._isTownhouse(x))
       df["IsCondo"]            = df["building type name"].apply(lambda x: self._isCondo(x))
       df["IsSingleFamily"]     = df["building type name"].apply(lambda x: self._isSingleFamily(x))
       df["IsJacksonville"]     = df["Site Address City"].apply(lambda x: self._isJacksonville(x))
       df["IsAtTheBeach"]       = df["Site Address City"].apply(lambda x: self._isAtTheBeach(x))
       df["IsPonteVedra"]       = df["Site Address City"].apply(lambda x: self._isPontevedra(x))

       #compute the zones
       df = self._computeZone(df)
       df = self._computeAdjustedAreaZip(df)
       df = self._computeAdjustedAreRooms(df)

       return df