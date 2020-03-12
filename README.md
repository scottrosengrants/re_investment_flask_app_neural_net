# RE Investment Application with Neural Net

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

The target of the model was to accurately predict whether an applicant would be approved or denied for a mortgage loan. The data set originally provided the below denial reasons:

1 - Debt-to-income ratio
2 - Employment history
3 - Credit history
4 - Collateral
5 - Insufficient cash (downpayment, closing costs)
6 - Unverifiable information
7 - Credit application incomplete
8 - Mortgage insurance denied
9 - Other
10 - Not applicable

"Not applicable" is the status given for an approved loan.

After further analysis of the targets a binomial target was created. All denial reasons were categorized together into simpy a "denied" category. This helped simplify the model predictions.

This decision also made logical sense as many of the denial reasons were questionable as to whether a model can accurately predict that particular outcome given it's limited inputs. Take for example "Credit application incomplete" or "Unverifiable information" denial reasons. While these are valid denial reasons they may not be as relevant to the information the model is provided. Each instance of the model is provided a complete dataset so it is tough to have it predict an "incomplete application". By combining these denial reasons into simply one denial classification this helps generalize the model predictions to the data and helps alliviate this shortcoming of the model design.

The targets were converted to a binary classification:

0 = Loan Not Approved
1 = Loan Approved

## Real Estate Calculations
  
## Application

  <img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_inputs_1.jpeg" style="width: 500px"><img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_inputs_2.jpeg" style="width: 500px">

  <img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_results.jpeg" style="width: 500px">
  
## Limitations

The rental data is only based on County, this limits the accuracy of this information. 

The model is a “black-box” model resulting more accurate predictions but unfortunately little to no insight to the user as to why they may be denied for a loan. 

The data used to train the model was limited and may not be indicative to actual approval odds.
Debt - to - Income ratio
Credit Score
The model likely picked up on a trend that is unseen in the data. Limiting the ability to replicate results.


## Continued Work & Ideas for Improvement

This analysis could be continued and improved upon with the following items/elements:

#### Credit Score and Debt-to-Income
The data set used to predict whether a mortgage loan would be approved or not did not contain credit scores. This element is a large factor a lender will take into consideration when deciding to approve or deny a loan application. For improved model performance and overall for a more realistic modeling situation an applicants credit score should be considered.

The dataset also contained more than 50% null values in the debt-to-income category. Much like credit score, this factor has a huge impact on whether or not an applicant is approved for a mortgage loan. Lending standards limit the maximum debt-to-income limit at 50%. This factor would be nice to include in a future model and likeliy improve the model's accuracy.

#### Neighborhood Specific Rental Figures
The data provided by the Fair Market Rents FY 2020 dataset was limited to a general county rental figure. With many counties, especially those located in an urban center, they often contain many neighborhoods and differing regions. These neighborhoods oftentimes fetch higher or lower rental amounts based on many local factors. To improve the effectivness of this application the more specific and acurate the rental figure is the more accurate the whole application becomes.

#### Multiple Unit Analysis
Many of the properties contained in the datasets contain multiple units such as a duplex containing two income producing units. The application is currently limited to only single units. To improve the overall usefullness of the application, calculations for multiple units within one address could be added.
  
