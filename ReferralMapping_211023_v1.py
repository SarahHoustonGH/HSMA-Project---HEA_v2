import os
import pandas as pd
import pgeocode

class ReferralMapping:
    def __init__(self):
        self.data_folder = "Stage1Outputs/"  # Hardcoded data folder
        self.nomi = pgeocode.Nominatim('gb')
        self.fulldata_subset = None

    def read_mapping_data(self):
        mapping_data = pd.read_csv("Data/x-boundary-mapping-2023-24-v1.csv")
        return mapping_data
    
    def read_IMD_data(self):
        IMD_data = pd.read_csv("Data/IMD_LSOA_Lookup.csv")
        return IMD_data

    def read_registration_data(self):
        registration_data = pd.read_csv(os.path.join(self.data_folder, "GPdata.csv"))
        return registration_data

    def merge_mapping_and_registration(self, mapping_data, registration_data, IMD_data):
        mapping_data = mapping_data.rename(columns={'Practice': 'CODE'})
        fulldata = pd.merge(mapping_data, registration_data, on='CODE')
        fulldata = pd.merge(fulldata, IMD_data, on='LSOA11')
        return fulldata

    def generate_subset(self, fulldata):
        self.fulldata_subset = fulldata[['CODE', 'GP practice name', 'Postcode', 'ICB23ons', 'LAD21', 'LAD21name',
                                    'ICB23', 'ICB23name', 'LSOA11', 'MSOA11', 'POSTCODE', 'NUMBER_OF_PATIENTS', 'IMD2019 Decile']]
        self.fulldata_subset.to_csv(os.path.join(self.data_folder, 'GP_Data_Map_summary.csv'))

    def process_referral_and_location_data(self, referral_modalities):
        for modality in referral_modalities:
            ref_data = pd.read_csv(os.path.join(self.data_folder, f"ReferralDummy_{modality}_GPCode_summary.csv"))
            cdc_data = pd.read_csv(os.path.join(self.data_folder, f"CDCReferralDummy_{modality}_GPCode_summary.csv"))
            
            self.fulldata_subset = self.fulldata_subset.rename(columns={'CODE': 'Patient GP'})
            
            gpsummary_referral_data = pd.merge(self.fulldata_subset, ref_data, on='Patient GP')
            gpsummary_referral_data = pd.merge(gpsummary_referral_data, cdc_data, on='Patient GP', suffixes=('_Referrals_Baseline','_Referrals_CDC'))
            
            # Add location info to the merged data
            postcodes = gpsummary_referral_data["Postcode"]
            gpsummary_referral_data["Latitude"] = None
            gpsummary_referral_data["Longitude"] = None
            
            for i, postcode in enumerate(postcodes):
                location_info = self.nomi.query_postal_code(postcode)
                if not location_info.empty:
                    gpsummary_referral_data.at[i, "Latitude"] = location_info.latitude
                    gpsummary_referral_data.at[i, "Longitude"] = location_info.longitude
            
            # Write the final CSV
            output_file = os.path.join(self.data_folder, f'GPSummaryReferralData_{modality}_Map.csv')
            gpsummary_referral_data.to_csv(output_file, index=False)


if __name__ == "__main__":
    referral_mapping = ReferralMapping()
    
    mapping_data = referral_mapping.read_mapping_data()
    IMD_data = referral_mapping.read_IMD_data()
    registration_data = referral_mapping.read_registration_data()
    fulldata = referral_mapping.merge_mapping_and_registration(mapping_data, registration_data, IMD_data)
    referral_mapping.generate_subset(fulldata)
    
    referral_modalities = ["X", "U"]
    referral_mapping.process_referral_and_location_data(referral_modalities)
