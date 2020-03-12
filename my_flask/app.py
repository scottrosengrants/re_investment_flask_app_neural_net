from flask import Flask, request, render_template, jsonify, Response
import pandas as pd
import numpy as np
from mortgage import Loan
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import load_model
from pickle import load
import requests
import json
from pandas.io.json import json_normalize
import http.client


# For reproducibility
np.random.seed(42)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras import utils


# initialize the flask app
app = Flask('myApp')

# load in HUD 2020 FMR 50 data (median rent by county)
rent_data = pd.read_excel('../data/data.gov/FY2020_50_County.xlsx')
print(len(rent_data))

# load fips data
fips = pd.read_csv('../data/fips.csv',dtype={'county_code':str})

# load model
model = load_model('../models/binary_nn.h5')
# load scaler
ss = load(open('../models/scaler.pkl', 'rb'))

# create a placeholder user df
def make_user():
    user = {
    'county_code': [0],
    'census_tract': [0],
    'preapproval': [0],
    'loan_amount': [0],
    'combined_loan_to_value_ratio': [0],
    'interest_rate': [0],
    'loan_term': [0],
    'interest_only_payment': [0],
    'balloon_payment': [0],
    'property_value': [0],
    'occupancy_type': [0],
    'total_units': [0],
    'income': [0],
    'submission_of_application': [0],
    'tract_population': [0],
    'ffiec_msa_md_median_family_income': [0],
    'tract_to_msa_income_percentage': [0],
    'tract_owner_occupied_units': [0],
    'tract_one_to_four_family_homes': [0],
    'tract_median_age_of_housing_units': [0],
    'state_code_AL': [0],
    'state_code_AR': [0],
    'state_code_AZ': [0],
    'state_code_CA': [0],
    'state_code_CO': [0],
    'state_code_CT': [0],
    'state_code_DC': [0],
    'state_code_DE': [0],
    'state_code_FL': [0],
    'state_code_GA': [0],
    'state_code_GU': [0],
    'state_code_HI': [0],
    'state_code_IA': [0],
    'state_code_ID': [0],
    'state_code_IL': [0],
    'state_code_IN': [0],
    'state_code_KS': [0],
    'state_code_KY': [0],
    'state_code_LA': [0],
    'state_code_MA': [0],
    'state_code_MD': [0],
    'state_code_ME': [0],
    'state_code_MI': [0],
    'state_code_MN': [0],
    'state_code_MO': [0],
    'state_code_MS': [0],
    'state_code_MT': [0],
    'state_code_NC': [0],
    'state_code_ND': [0],
    'state_code_NE': [0],
    'state_code_NH': [0],
    'state_code_NJ': [0],
    'state_code_NM': [0],
    'state_code_NV': [0],
    'state_code_NY': [0],
    'state_code_OH': [0],
    'state_code_OK': [0],
    'state_code_OR': [0],
    'state_code_PA': [0],
    'state_code_PR': [0],
    'state_code_RI': [0],
    'state_code_SC': [0],
    'state_code_SD': [0],
    'state_code_TN': [0],
    'state_code_TX': [0],
    'state_code_UT': [0],
    'state_code_VA': [0],
    'state_code_VT': [0],
    'state_code_WA': [0],
    'state_code_WI': [0],
    'state_code_WV': [0],
    'state_code_WY': [0],
    'loan_type_2': [0],
    'loan_type_3': [0],
    'loan_type_4': [0]
    }
    return pd.DataFrame.from_dict(user)

# call ATTOM API
def call_api_all(bld_num,street,str_type,unit=None,unit_num=None,city=None,state=None):
 
    
    conn = http.client.HTTPSConnection("api.gateway.attomdata.com") 

    headers = { 
        'accept': "application/json", 
        'apikey': "XXX", 
    } 
    address_1 = f"address1={bld_num}%20{street}%20{str_type}%20{unit}%20{unit_num}"
    address_2 = f"&address2={city}%2C%20{state}"
    conn.request("GET", f"/propertyapi/v1.0.0/allevents/detail?{address_1}{address_2}", headers=headers) 

    res = conn.getresponse() 
    data = res.read() 
    

    return data


# create df from ATTOM api
def extract_details(api_data):
    house = json.loads(api_data)
    
    # create new dfs based on dictionary keys

    # df_1 ['obPropId', 'fips', 'apn', 'apnOrig', 'attomId']
    df_1 = pd.DataFrame(house['property'][0]['identifier'],index=[0])

    # df_2 ['depth', 'frontage', 'lotnum', 'lotsize1', 'lotsize2', 'pooltype']
    df_2 = pd.DataFrame(house['property'][0]['lot'],index=[0])

    # df_3 ['blockNum', 'countrysecsubd', 'countyuse1', 'muncode', 'munname',
    #       'srvyRange', 'srvySection', 'srvyTownship', 'subdname', 'subdtractnum','taxcodearea']
    df_3 = pd.DataFrame(house['property'][0]['area'],index=[0])

    # df_4 ['country', 'countrySubd', 'line1', 'line2', 'locality', 'matchCode',
    #       'oneLine', 'postal1', 'postal2', 'postal3']
    df_4 = pd.DataFrame(house['property'][0]['address'],index=[0])

    # df_5 = ['accuracy', 'elevation', 'latitude', 'longitude', 'distance', 'geoid']
    df_5 = pd.DataFrame(house['property'][0]['location'],index=[0])

    # df_6 ['absenteeInd', 'propclass', 'propsubtype', 'proptype', 'yearbuilt',
    #       'propLandUse', 'propIndicator', 'legal1']
    df_6 = pd.DataFrame(house['property'][0]['summary'],index=[0])

    #df_7 ['heatingtype']
    df_7 = pd.DataFrame(house['property'][0]['utilities'],index=[0])

    #df_8 **['size', 'rooms', 'interior', 'construction', 'parking', 'summary']** dict keys
    df_8 = pd.DataFrame(house['property'][0]['building'],index=[0])

    #df_9 ['lastModified', 'pubDate']
    df_9 = pd.DataFrame(house['property'][0]['vintage'],index=[0])
    
    # create new dfs based on df_8 dictionary keys

    # df_b1 ['bldgsize', 'grosssize', 'grosssizeadjusted', 'groundfloorsize',
    #       'livingsize', 'sizeInd', 'universalsize']
    df_b1 = pd.DataFrame(house['property'][0]['building']['size'],index=[0])

    # df_b2 ['bathfixtures', 'baths1qtr', 'baths3qtr', 'bathscalc', 'bathsfull',
    #       'bathshalf', 'bathstotal', 'beds', 'roomsTotal']
    df_b2 = pd.DataFrame(house['property'][0]['building']['rooms'],index=[0])

    #df_b3 ['bsmtsize', 'bsmttype', 'fplccount', 'fplcind', 'fplctype']
    df_b3 = pd.DataFrame(house['property'][0]['building']['interior'],index=[0])

    #df_b4 ['condition', 'wallType']
    df_b4 = pd.DataFrame(house['property'][0]['building']['construction'],index=[0])

    #df_b5 ['garagetype', 'prkgSize', 'prkgSpaces', 'prkgType']
    df_b5 = pd.DataFrame(house['property'][0]['building']['parking'],index=[0])

    #df_b6 ['bldgsNum', 'bldgType', 'imprType', 'levels', 'mobileHomeInd',
    #       'quality', 'storyDesc', 'unitsCount', 'yearbuilteffective']
    df_b6 = pd.DataFrame(house['property'][0]['building']['summary'],index=[0])
    
    ### AVM
    #df_v1 ['scr', 'value', 'high', 'low', 'valueRange']
    df_v1 = pd.DataFrame(house['property'][0]['avm']['amount'],index=[0])
    
    #df_v2 ['avmpoorlow', 'avmpoorhigh', 'avmpoorscore', 'avmgoodlow', 'avmgoodhigh', 
    #      'avmgoodscore', 'avmexcellentlow', 'avmexcellenthigh', 'avmexcellentscore']
    df_v2 = pd.DataFrame(house['property'][0]['avm']['condition'],index=[0])
    
    #df_v3 ['taxamt', 'taxpersizeunit', 'taxyear']
    df_v3 = pd.DataFrame(house['property'][0]['assessment']['tax'],index=[0])
    
    # Build df for property 1
    prop_1 = pd.concat([df_1['fips'],df_2,df_3,df_4,df_5,df_6,df_7,df_9,df_b1,
                        df_b2,df_b3,df_b4,df_b5,df_b6,df_v1,df_v2,df_v3],axis=1)
    
    return prop_1

def get_rent(bed_count,state, county):
    row = rent_data[(rent_data['state_alpha'] == str(state)) & (rent_data['cntyname'] == county)]
    if bed_count < 0:
        return 'Must enter bedroom count greater than zero'
        
    elif bed_count <= 4:
        return int(row['rent50_'+str(bed_count)])
    
    else: 
        extra_beds = bed_count - 4
        rent = row['rent50_4']
        for i in range(extra_beds):
            rent = rent * 1.15
        return int(rent)

def coc(df,principal,cash):
    
    #calculate loan
    loan = Loan(principal, interest=.04, term=30)
    pymt = loan.monthly_payment
    
    #calculate re figures
    mti = float(df['rent'].loc[0])
    vr = float(mti * .05)
    er = float(mti * (.05 + .05))
    me = float((100 + 50)) #water & trash
    mfc = float(pymt)
    mt = float(df['taxamt'].loc[0]/12)
    mi = float(mt)  #(3000/12)
    # Composite
    mcf = mti - vr - er - me - mfc - mt - mi

    # Annual
    acf = np.round((mcf * 12),2)

    # Financial 
    tci = cash
    coc = np.round(((acf / tci) * 100),2)
    
    print(f'Your Annual Cashflow is ${acf} giving you a Cash-On-Cash return of {coc}%!')
    print(f'{mcf} = {mti} - {vr} - {er} - {me} - {mfc} - {mt} - {mi}')
    print(f'Cash Flow = Rent Income - Vacancy - Maint/Cap Exp - Water&Trash - Finance Exp - Tax - Insurance')

    coc_dict = {'mti':mti,
               'vr':vr,
               'er':er,
               'me':me,
               'mfc':mfc,
               'mt':mt,
               'mi':mi,
               'mcf':mcf,
               'acf':acf,
               'tci':tci,
               'coc':coc}
    return coc_dict

def results(principal, cash, bld_num,street,str_type,unit=None,unit_num=None,city=None,state=None):
    prop = extract_details(call_api_all(bld_num,street,str_type,unit,unit_num,city,state))
    prop_sm = prop[['beds','taxamt','countrySubd','countrysecsubd']].copy() 
    prop_sm['rent'] = get_rent(prop_sm['beds'].loc[0],prop_sm['countrySubd'].loc[0],prop_sm['countrysecsubd'].loc[0])
    prop['rent'] = prop_sm['rent']
    coc_dict = coc(prop_sm,principal,cash)
    return prop, coc_dict

# User Inputs
def user_inputs(user_df,price,downpayment_perc,preapproval,interest_rate,
loan_term,interest_only_payment,balloon_payment,occupancy_type,income,submission_of_application,
loan):
                 
    loan_amount = price * (1-downpayment_perc)
    combined_loan_to_value_ratio = loan_amount / price
    income = int(income)/1000
                 
    user_df['preapproval'] = int(preapproval)
    user_df['loan_amount'] = loan_amount
    user_df['combined_loan_to_value_ratio'] = combined_loan_to_value_ratio   
    user_df['interest_rate'] = interest_rate
    user_df['loan_term'] = int(loan_term) 
    user_df['interest_only_payment'] = int(interest_only_payment) 
    user_df['balloon_payment'] = int(balloon_payment)
    user_df['property_value'] = int(price)
    user_df['occupancy_type'] = int(occupancy_type)
    user_df['income'] = int(income)             
    user_df['submission_of_application'] = int(submission_of_application)   
    
    if loan == 2:
        user_df['loan_type_2'] = 1
    elif loan == 3:
        user_df['loan_type_3'] = 1
    elif loan == 4:
        user_df['loan_type_4'] = 1
    return user_df

# census data
def apply_census(fips_num, user_df):
    mask = fips['county_code'] == fips_num
    df = fips[mask]
    user_df['county_code'] = fips_num
    user_df['census_tract'] = int(df['census_tract'])
    user_df['tract_population'] = int(df['tract_population'])
    user_df['ffiec_msa_md_median_family_income'] = float(df['ffiec_msa_md_median_family_income'])
    user_df['tract_to_msa_income_percentage'] = float(df['tract_to_msa_income_percentage'])
    user_df['tract_owner_occupied_units'] = float(df['tract_owner_occupied_units'])
    user_df['tract_one_to_four_family_homes'] = float(df['tract_one_to_four_family_homes'])
    user_df['tract_median_age_of_housing_units'] = float(df['tract_median_age_of_housing_units'])
    return user_df

#add units
def add_units(property_df, user_df):
    user_df['total_units'] = int(property_df['unitsCount'])
    return user_df

# add state
def add_state(property_df, user_df):
    column = 'state_code_' + property_df['countrySubd'].loc[0]
    user_df[column] = 1
    return user_df

########################     ROUTES     ####################
#route 1: Home
@app.route('/')
def home():
    return 'Home'
#route 2: Form
@app.route('/form')
def form():
    return render_template('form.html')

#route 3: api
@app.route('/info')
def info():
    prop_2 = results(400_000,150_000,'1232','Quaker','Street','Golden','CO')
    avm_good = prop_2['avmgoodlow'].iloc[0]	
    return jsonify(avm_good)

#route 4: load in the form data from the incoming request
@app.route('/submit')
def submit():
    user_input = request.args 

   # form fields that were submitted
    p = int(user_input['price'])
    dp_pct = float(user_input['down_payment_pct'])
    pn = user_input['property_number']
    sn = user_input['street_name']
    st = user_input['street_type']
    c = user_input['city']
    s = user_input['state']
#
    preapproval = user_input['preapproval']
    interest_rate = user_input['interest_rate']
    loan_term = user_input['loan_term']
    interest_only_payment = user_input['interest_only_payment']
    loan = user_input['loan']
    balloon_payment = user_input['balloon_payment']
    occupancy_type = user_input['occupancy_type']
    income = user_input['income']
    submission_of_application = user_input['submission_of_application']

# calculated fields
    la = p * (1-dp_pct)
    dp = p * dp_pct
    
    prop, prop_coc_dict = results(la,dp,pn,sn,st,c,s)
    address = prop['oneLine'].iloc[0]
    m_rent = prop['rent'].iloc[0]
    poor = f"${prop['avmpoorlow'].iloc[0]} - ${prop['avmpoorhigh'].iloc[0]}"
    good = f"${prop['avmgoodlow'].iloc[0]} - ${prop['avmgoodhigh'].iloc[0]}"
    excellent = f"${prop['avmexcellentlow'].iloc[0]} - ${prop['avmexcellenthigh'].iloc[0]}"

    # calculate cap rate
    cap = np.round((((prop_coc_dict['acf'] + 12 * prop_coc_dict['mfc']) / p) *100),2)

# build model data
    user_df = make_user()
    user_df = apply_census(prop['fips'].loc[0], user_df)
    user_df = add_units(prop, user_df)
    user_df = add_state(prop, user_df)
    user_inputs(prop,p,dp_pct,preapproval,interest_rate,
        loan_term,interest_only_payment,balloon_payment,occupancy_type,
        submission_of_application,income,loan)

#scale user data
    user_scaled = ss.transform(user_df.drop(columns='county_code'))

# make prediction
    pred = model.predict(user_scaled)
    pred = np.argmax(pred)
    if pred == 1:
        pred = 'likely'
    else: 
        pred = 'unlikely'

#items to pass to results page
    return render_template('results.html', address=address, m_rent=m_rent, cap=cap, 
        vr= np.round(prop_coc_dict['vr'],2),
        er= np.round(prop_coc_dict['er'],2),
        me = np.round(prop_coc_dict['me'],2),
        mfc = np.round(prop_coc_dict['mfc'],2),
        mt = np.round(prop_coc_dict['mt'],2),
        mi = np.round(prop_coc_dict['mi'],2),
        mcf = np.round(prop_coc_dict['mcf'],2),
        acf = np.round(prop_coc_dict['acf'],2),
        coc = np.round(prop_coc_dict['coc'],2),
        poor = poor,
        good = good,
        excellent = excellent,
        pred = pred
    )



# Call app.run(debug=True) when python script is called
if __name__ == "__main__": # if we run the file(app_starter.py) from the trminal
    app.run(debug=True)
