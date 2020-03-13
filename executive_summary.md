# Executive Summary
### RE Investment Application with Neural Network Model

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

In order to construct the application and train a predictive model several types of data had to be collected. Property info, rental amounts, and past mortgage loan records were all needed. Below is a brief summary of were each of those dataset were found. 

#### Property Record & Attributes
The ATTOM Data "All Records" api call was utilized to collect the public information and property feature information.

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

1 - Debt-to-income ratio <br>
2 - Employment history<br>
3 - Credit history<br>
4 - Collateral<br>
5 - Insufficient cash (downpayment, closing costs)<br>
6 - Unverifiable information<br>
7 - Credit application incomplete<br>
8 - Mortgage insurance denied<br>
9 - Other<br>
10 - Not applicable<br>

"Not applicable" is the status given for an approved loan.

After further analysis of the targets a binomial target was created. All denial reasons were categorized together into simply a "denied" category. This helped simplify the model predictions.

This decision also made logical sense as many of the denial reasons were questionable as to whether a model can accurately predict that particular outcome given it's limited inputs. Take for example "Credit application incomplete" or "Unverifiable information" denial reasons. While these are valid denial reasons they may not be as relevant to the information the model is provided. Each instance of the model is provided a complete dataset so it is tough to have it predict an "incomplete application". By combining these denial reasons into simply one denial classification this helps generalize the model predictions to the data and helps alliviate this shortcoming of the model design.

The targets were converted to a binary classification:

0 = Loan Not Approved<br>
1 = Loan Approved<br>

Both logistic regression models and neural networks were applied to the datset. A neural network was found to perform the best with an overall accuracy of 94.15% of correctly predicting whether a mortgage loan application would be approved. More information is provided on the exact specifications of this neural network in the technical_report provided in this repository. 

This model was stored in the repository and can be called upon the application any time an investor uses the application. This streamlines the process for the investor and allows them to reach out to loan officers and bank less frequently in their property search. 

## Real Estate Calculations

The application calculates several standard real estate investing calculations to provide the user information about the potential returns on investment they can expect from a given property. For a complete breakdown of these calculations, refer to the technical_report included in this repository.


**Monthly Cash Flow**  =       Monthly Income 
                         - Vacancy Expense 
                         - Mainenance Expense
                         - Water & Trash 
                         - Monthly Finance Expense
                         - Monthly Taxes
                         - Monthly Insurance

**Annual Cashflow**    =       Monthly Cashflow * 12 Months

**Cash on Cash Return (COC)** = (Annual Cashflow / Total Cash Invested) * 100

**Capitalization Rate (Cap Rate)** = Annual Cashflow (less Financing Expense) / Property Price

**ATTOM Data Property Valuation**

ATTOM's api provides a general property valuation for three tiers of quality of a given subject Property. They have a proprietary algorithm that will assign a property a valuation based on up to 100 property comparables sold in the last year in the area of the subject property.

Valuation Tiers:

Poor Condition <br>
Average Condition <br>
Good Condition <br>

These valuations are provided to the user to help them get an idea of whether or not the property they are analyzing is priced realistically and fairly.

    
## Application

Below are several screenshots of the application. While basic, the MVP does successfully take user input, retrieve the correct property info, calculate the real estate investment calculations, and make a prediction on the investors loan approval rating from a neural network. 

### User Input Page
  <img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_inputs_1.jpeg" style="width: 500px"><img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_inputs_2.jpeg" style="width: 500px">
  
### Results Page

  <img src="https://github.com/scottrosengrants/re_investment_flask_app_neural_net/blob/master/images/app_results.jpeg" style="width: 500px">
  
## Limitations

The rental data is only based on County, this limits the accuracy of this information. While the rental data is still correct it is somewhat diluted in regions where rental amounts can vary widely.

The model is a “black-box” model resulting more accurate predictions but unfortunately little to no insight to the user as to why they may be denied for a loan. 

The data used to train the model was limited and may not be indicative to actual approval odds. Debt-to-Income ratio and Credit Score are known to be very good indicators to whether a mortgage loan application is approved or not. They were not included in this model. Unfortunately that may result in a model that has a high accuracy rating when testing it but does not translate well to a real world scenario. More analysis is needed to confirm the models true predictive ability. 

## Continued Work & Ideas for Improvement

This analysis could be continued and improved upon with the following items/elements:

#### Credit Score and Debt-to-Income
The data set used to predict whether a mortgage loan would be approved or not did not contain credit scores. This element is a large factor a lender will take into consideration when deciding to approve or deny a loan application. For improved model performance and overall for a more realistic modeling situation an applicants credit score should be considered.

The dataset also contained more than 50% null values in the debt-to-income category. Much like credit score, this factor has a huge impact on whether or not an applicant is approved for a mortgage loan. Lending standards limit the maximum debt-to-income limit at 50%. This factor would be nice to include in a future model and likeliy improve the model's accuracy.

#### Neighborhood Specific Rental Figures
The data provided by the Fair Market Rents FY 2020 dataset was limited to a general county rental figure. With many counties, especially those located in an urban center, they often contain many neighborhoods and differing regions. These neighborhoods oftentimes fetch higher or lower rental amounts based on many local factors. To improve the effectivness of this application the more specific and acurate the rental figure is the more accurate the whole application becomes.

#### Multiple Unit Analysis
Many of the properties contained in the datasets contain multiple units such as a duplex containing two income producing units. The application is currently limited to only single units. To improve the overall usefullness of the application, calculations for multiple units within one address could be added.

## Problem Statement - Application Objectives Revisited: 

After completion of this project/analysis the following statements can be made:

Given a property address a relevant rental amount can be found for the propety.

Standard real estate metrics can be automated.

Given the location of a property and user provided financial information a model can be developed for predicting the approval of a potential mortgage loan, however more testing on real world data will be needed to confirm its accuracy and effectiveness. 
