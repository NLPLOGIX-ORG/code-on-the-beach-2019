class Features:
   
   def _isAtTheBeach(self, val):
      
      try:
         return 1 if "beach" in val.lower() else 0
      except:
         return 0

   def _computeAdjustedAreaRooms(self, df):
     
      AA_Zscore = lambda x: (x - x.mean())/x.std()
      df['AdjustedArea_Rooms'] = df.groupby(df['Number Of Rooms'])['building heated area'].transform(AA_Zscore)

      return df

   def _computeBedroomToTotalRoomRatio(self, row):
      
      if row["Number Of Bedrooms"] <= 0:
         return 0.0

      if row["Number Of Rooms"] <= 0:
         return 0.0

      return row["Number Of Bedrooms"] / (row["Number Of Rooms"] * 1.0)

   def _computeBathroomToTotalRoomRatio(self, row):
      
      if row["Number Of Bedrooms"] <= 0:
         return 0.0

      if row["Number Of Rooms"] <= 0:
         return 0.0

      return row["Number Of Bathrooms"] / (row["Number Of Rooms"] * 1.0)

   def compute(self, df):
       start_cols = set(df.columns.values)
       df["IsAtTheBeach"]                  = df["Site Address City"].apply(self._isAtTheBeach)
       df["BedroomToTotalRoomRatio"]       = df.apply(self._computeBedroomToTotalRoomRatio, axis=1)
       df["BathroomToTotalRoomRatio"]       = df.apply(self._computeBathroomToTotalRoomRatio, axis=1)
       
       df = self._computeAdjustedAreaRooms(df)

       new_cols = list(set(df.columns.values) - start_cols)
       
       return df, new_cols