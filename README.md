# re_investment

## Overview:

Many real estate applications on the market do not service the real estate investor. An investor needs to know relevant property information AND rental information. The goal of this application is to pair real estate property data with the rental market information and loan terms. Given these three elements a real estate investor can make a more educated decision on which properties to purchase.

## Problem Statement - Application Objective:

Given a property address can relevant rental amounts be found for the propety? Can standard real estate metrics be automated?

According to the location of the property and user provided financial information can a model be developed for predicting the approval of a potential mortgage loan?

### What Real Estate Investors Currently Do:

Currently real estate investors must manually search for potential properties. This searching process is done through local real estate agents and online sites like Zillow.com. 

Once they have identified a property of interest they then must evaluate what it produces in rental income. This is not a straight forward process and it is often difficult to find relient rental figures especially in certain markets. Often this process requires visiting several website such as craigslist.com and call local real estate agents. 

Once the rental amount has been established they then need to calculate several common calculations such as Cash-on-Cash return, Capitalization Rate and Cash Flow. These calculations are not overly complicated but are time intensive and redundant. 

Finally they have to decide if the calculations look appealling and whether they are interested in pursuing the property. If they decide to persue the property they then have to call their mortgage lender to check on wheter they qualify for a mortgage loan on the property. This is not something that can be assumed because each state and county can have their own unique requirements. 

All these steps add up to a lot of time for the investors and many of these processes become redundant.

### The Proposed Solution - MVP:

One possible solution to improve this process is to automate much of the investors' search process. 

The application developed does the following:

1) Collects the property address from the user.
2) The address information is collected from the ATTOM api.
3) The aproximate rental amount is collected from the 2020 HUD Fair Market Rent Report based on the county.
4) The cost of the property and the potential rental income is calculated and a several real estate investment metrics are calculated.
5) The property information and the user's financial information are fed into a Nueral Network.
6) The Nueral Network provides the likelihood that the investor will be approved or denied for the mortgage loan of that particular property.
7) The real estate investment calculations, the likelihood for loan approval, and the ATTOM property valuation ranges are provided to the investor all in one convenient page within the application.  

### Data

#### Property Record & Attributes
The ATTOM Data "All Records" api call is utilized to collect the public information and property feature information.

https://api.developer.attomdata.com/

#### Fair-Market-Rental Values
The County Level Fair Market Rents FY 2020 dataset was used for rental figures. This dataset provides FMR figures for 0-4 bedroom homes per county.

https://www.huduser.gov/portal/datasets/fmr.html#2020_data

#### Mortgage Records
The 2018 Loan/Applications Records dataset from the FFIEC was used for mortgage approval history. The Home Mortgage Disclosure Act requires every lending institution to report applications for home mortgages and whether the application was approved. This dataset also contained census tract information for every loan application.

https://ffiec.cfpb.gov/data-publication/dynamic-national-loan-level-dataset/2018

The data fields collected from these APIs and datasets are listed in the data dictionary included in this repository.

### The Data Flow
These three datasets each work together to provide the database for the application to run.

--> From ATTOM the proprty profile is built.

----> From the property profile, the county and bedroom count is pulled.

------> Using the county and bedroom values, the Fair Market Rent is pulled from the Fair Market Rents FY 2020 dataset and added to the property profile

--------> The 2018 Loan/Applications Records dataset was used to train the mortgage loan approval predictive model

----------> From the 2018 Loan/Applications Records dataset the census tract data fields are applied to the property profile

------------> User fields are provided and added to the property profile

--------------> The complete property profile is run through the mortgage approval model and a prediction is generated

----------------> The real estate calculations are made from the property profile and displayed.
     

## Modeling

## Real Estate Calculations
  
## Application
  
## Limitations

## Future Work & Improvements
  
