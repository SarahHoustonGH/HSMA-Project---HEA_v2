# HSMA 5 Health Equity Audit

Please note as of December 2023, this project and code is still under development. There is an ongoing issue with a large JSON file currently not uploading to Github. For access to this file, please contact the team at sarah.houston.16@ucl.ac.uk

You can watch a short presentation on the project from the HSMA5 Open Day [here.](https://www.youtube.com/watch?v=tavZS5MmwOA)

## Introduction to CDCs

Community diagnostic centres (CDCs) have been launched across England to tackle the diagnostic backlog and address healthcare inequalities. 
CDCs and commissioners struggle to identify their baseline of healthcare inequalities and monitor their impact going forwards. 
This leads to resourcing constraints on teams in the short term and risks minimising the CDC’s impact on healthcare inequalities in the long term. 
As these are emerging services, the quality of data collected by them to understand their impact is unclear. 
This product is designed to automate much of this process for a generic CDC to support CDCs in understanding their impact on a specific local authority.

## Introduction to project

This code was developed as part of the [Health Service Modelling Associates Programme](https://sites.google.com/nihr.ac.uk/hsma) by Sarah Houston and Deborah Newton.
There are two steps to this process, culminating in a Streamlit app which allows you to visualize results produced by Health Equity Audit for CDCs. Details on how to use the code are included below.

## User guide

### Data required

Dummy data is included in the Github repository for demo purposes. This data has been generated randomly and bears no relation to real referral data but may refer to a local authroity which has a CDC.

To use this code, the following is required:
-	Referral level data from the CDC
-	Referral level data from a matched baseline diagnostic service 
-	Both data must at a minimum contain fields as described below

The matched baseline service could be a local acute diagnostic service operating in the year before the introduction of the CDC.

The following fields are required in the baseline and CDC referral data:
-	Referral Source: Name of GP practice
-	Modality: Diagnostic modality. This version of the code supports X (x ray) and U (ultrasound)
-	Patient GP: GP registration code
-	Age: Age in years
-	Patient_Gender: Male, Female or Unknown
-	Ethnicity_Code: [NHS Ethnic Category](https://www.datadictionary.nhs.uk/data_elements/ethnic_category.html) (e.g. A)
-	Ethnicity Description: Full description of code (e.g. White British)
-	Postcode: GP location postcode

### Structure of code

This analysis is performed in two steps: Processing and Display.
    
#### Step 1: Processing

- Download the Github folder
- Replace the dummy data files with
- Run the AutomatedHEA_MasterFile: This will run all the modules required to generate outputs for the Streamlit application.
    
At this stage, the user also inputs the local authority of interest. This will be used as the base population which referral rates will be compared to. The CDC of interest should be within this local authority.

#### Step 2: Display

- Run the HEA_Streamlit_Home file
- The summary outputs from Step 1 will be used to build content for display in Streamlit

Due to the unique nature of CDCs which would be expected to host multiple diagnostic modalities, 
provisional modalities of X ray and ultrasound have been included for disaggregation of results, however these could be adapted for future versions.

### Limitations of analysis

1.	Gender is equated with sex in the analysis due to disparities in definition between NHS and Census data, potentially overlooking nuanced gender-related disparities.
2.	Index of Multiple Deprivation data based on GP location (GP_IMD) assumes patients are exclusively from that Lower Super Output Area (LSOA). Population weighted IMD (Pop_IMD) has been extracted from Fingertips (ONS).
3.	GP location data has been extracted from a [publication](https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice) by NHS Digital from July 2023. This may not reflect current practice location.
4.	GP location was based on registered practice location, which does not reflect branch practices.
5.	Data from other diagnostic services in the region is not included in the analysis. This means we are unable to determine if the CDC is effectively addressing health inequalities or merely shifting care between services in the region.
6.	This analysis does not attempt to quantify "unmet need", patients who should access diagnostics but do not, due to the non-specific nature of CDCs.
7.	This analysis assumes that the CDC should be a general service equally accessed by all demographic groups due to the diverse modalities and conditions it serves, however some services may be weighted towards specific groups, e.g. older patients.
8.	Potential barriers to access, such as language and disability, are not explored due to lack of data availability, limiting the understanding of disparities related to these factors.
9.	Intersectional analysis is not included in this analysis but may be beneficial due to the nuanced interactions between multiple factors that contribute to healthcare inequalities.
10.	Equity audits should also consider not just quantitative analysis such as presented here but also include qualitative engagement with local communities to understand potential barriers in referral and access.
11.	Broad ethnic categories are used to describe populations in this project, however ethnic and cultural diversity cannot be described by broad ethnic categories alone. Broad ethnic categories were chosen for accurate mapping between the NHS Ethnic Category to Ethnic Group as recorded by the ONS in the Census, but the code is still under development with aspiration to expand to granular ethnicity data.
12.	This project focusses on equity of referrals, however increasing referrals to diagnostics is only the first step to improving health outcomes in the region. Similar analysis should be performed to explore access (i.e. attendances), experience and outcomes across different demographic cohorts.

### Next steps

This project is still under development as of December 2023. Potential next steps are described below.

-	Flexible modality selection
-	Combine Step 1 (Processing, Python) with Step 2 (Display, Streamlit) to one user interface
-	Expand “base population” to include more than one local authority
-	Include data to highlight rural/urban disparities of referral
-	Expand analysis to more ethnic categories and granular ethnicities
-	Include more intersectional analysis (e.g. age vs gender, ethnicity vs deprivation)

### Data sources

Please see a list of data sources used in this code below.

| Data source             | Date accessed (if not accessed via code) | Link                                                          | Copyright                                   | Metrics used                                      |
|-------------------------|-----------------------------------------|---------------------------------------------------------------|----------------------------------------------|---------------------------------------------------|
| Census 2021             | Via code                                | [Census 2021](https://www.nomisweb.co.uk/sources/census_2021) | National Statistics data © Crown copyright and database rights 2023 | Age / Sex / Ethnicity                              |
| IMD 2019                | Via code                                | [IMD 2019](https://www.fscbiodiversity.uk/imd/)               | Copyright © 2023 Charles Roper                 | Calculated via the Field Studies Council "English IMD Postcode Checker" |
| Open Geography Portal, ONS | Aug-23                               | [Geography Portal](https://geoportal.statistics.gov.uk/datasets/766da1380a3544c5a7ca9131dfd4acb6/explore) | © Crown copyright                           | LSOA (Dec 2021) Boundaries Generalised Clipped EW (BGC) |
| Fingertips GP IMD       | Via code                                | [Fingertips GP IMD](https://fingertips.phe.org.uk/profile/general-practice/data#page/6/gid/2000005/pat/167/ati/7/are/H85026/iid/93553/age/1/sex/4/cat/-1/ctp/-1/yrr/1/cid/4/tbm/1) | © Crown copyright                           | GP weighted IMD                                    |
| Ideal Postcodes         | Via code                                | [Ideal Postcodes](https://postcodes.io/)                        | Postcodes.io                                | Postcode location                                  |
| NHS Data dictionary     | Aug-23                                  | [NHS Data dictionary](https://www.datadictionary.nhs.uk/data_elements/ethnic_category.html) | © NHS England                           | NHS Ethnic Category look up                          |

### 
### Contact us
    
If you would like to learn more about the project or contact the team for further details, please email sarah.houston.16@ucl.ac.uk
