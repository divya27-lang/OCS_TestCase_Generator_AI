import pandas as pd
import math
from create_testdata.query_offer import get_offer
from create_testdata.countries_list import eu_countries, edrp_countries, ci_iom, UK_special,b_numbers, b_party_sms
def create_test_data(price_data_path, tc_id, a_party, call_type, duration_bytes, roaming_location, called_country,
                     b_party_type, api_endpoint):
    exp_free_units = '0'
    b_party = ''
    exp_rating = '0'
    roaming_rate = '0'
    idd_rate = '0'

    # Data sessions
    if call_type == 'data' or call_type == '5g-data':
        # Data in UK
        if roaming_location == 'UK':

            exp_free_units = duration_bytes


        # Data in RPP
        elif roaming_location.upper() in eu_countries or roaming_location.upper() in edrp_countries:
            exp_free_units = duration_bytes
        # Data Roaming in RoW
        else:
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    exp_rating = ((country[1].iloc[6] / 1048576) * int(duration_bytes) * 100)


    # MT Voice
    elif call_type == 'n-mt-voice':
        b_party = b_numbers[called_country.upper()]

        if roaming_location == 'UK':
            exp_rating = '0'
        else:
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    p = (round(country[1].iloc[7], 2) * (math.ceil(int(duration_bytes) / 60)))
                    exp_rating = round(p * 100)
    elif call_type == 'n-mo-voice':
        # International Freephone
        if called_country.upper() == 'INTERNATIONAL 00800':
            b_party = b_numbers[called_country.upper()]
            exp_rating = '0'
            exp_free_units = '0'

        # Calling Sky contact centres
        elif b_party_type == 'Sky_Contact_Centres' or b_party_type == 'Sky_Contact_Centres:150':
            b_party = b_numbers[b_party_type.upper()]
            exp_rating = '0'
            exp_free_units = '0'

        # Calling Voicemail
        elif b_party_type == 'Voicemail':
            if roaming_location == 'UK':
                b_party = b_numbers[b_party_type.upper()]
                exp_rating = '0'
                exp_free_units = '0'
            else:
                b_party = b_numbers[b_party_type.upper()]
                exp_free_units = '0'
                df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
                for country in df.iterrows():
                    if country[1].iloc[0] == roaming_location:
                        p = (round(country[1].iloc[11], 2) * (math.ceil(int(duration_bytes) / 60)))
                        exp_rating = round(p * 100)

        # Domestic MO Voice call
        # Assuming UCT on all subs
        elif roaming_location == 'UK' and called_country == 'UK' or (
                roaming_location in ci_iom and called_country in ci_iom):
            b_party = b_numbers[called_country.upper()]
            if get_offer(api_endpoint, a_party):
                exp_rating = '0'
                exp_free_units = '0'
            else:
                exp_rating = '10'
                exp_free_units = '0'



        # IDD MO Voice Call
        elif roaming_location == 'UK' and called_country != 'UK' and called_country.upper() not in ci_iom:
            b_party = b_numbers[called_country.upper()]
            exp_free_units = '0'
            df = pd.ExcelFile(price_data_path).parse('5. International rate')
            for country in df.iterrows():
                if country[1].iloc[0] == called_country:
                    if get_offer(api_endpoint, a_party):
                        exp_rating = 10
                    else:
                        exp_rating = (country[1].iloc[6] * (math.ceil(int(duration_bytes) / 60))) * 100


        # Roaming in RPP calling UK
        elif roaming_location in edrp_countries or roaming_location in eu_countries and called_country == 'UK':
            b_party = b_numbers[called_country.upper()]
            exp_rating = '0'
            exp_free_units = '0'

        # Roaming in RoW calling UK
        elif roaming_location != 'UK' and roaming_location not in [edrp_countries,eu_countries] and called_country == 'UK':
            b_party = b_numbers[called_country.upper()]
            exp_free_units = '0'
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                # Get sub details to determine what saver is present
                # key_dict = get_ak_sk(api_endpoint, a_party)

                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        'No Charge',
                        'If calling CI/IoM 10p if PAYU / free if UL C&T. If calling RoI/RPP/RoW than no Charge',
                        'n/a',
                        '-'
                    ]
                    if str(country[1].iloc[8]) not in invalid_values:
                        try:
                            exp_rating = round(int(country[1].iloc[8] * (math.ceil(int(duration_bytes) / 60))) * 100)
                        except ValueError:
                            exp_rating = 0

                    else:
                        exp_rating = 0
                    if roaming_location in UK_special:
                     if get_offer(api_endpoint, a_party):
                       exp_rating = '10'
                    else:
                       exp_rating = (country[1].iloc[8] * (math.ceil(int(duration_bytes) / 60))) * 100

        elif roaming_location != 'UK' and called_country == 'IRELAND (REPUBLIC OF)':
            b_party = b_numbers[called_country.upper()]
            exp_free_units = '0'
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming rate')
            for country in df.iterrows():
                # Get sub details to determine what saver is present
                # key_dict = get_ak_sk(api_endpoint, a_party)

                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        '-',
                        'Free'
                    ]
                    if str(country[1].iloc[8]) not in invalid_values:
                        try:
                            exp_rating = round(int((country[1].iloc[8]) * (math.ceil(int(duration_bytes) / 60))) * 100)
                        except ValueError:
                            exp_rating = 0

                    else:
                        exp_rating = 0


        # Roaming in RoW calling internationally
        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location not in UK_special and roaming_location != called_country:
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        'No Charge',
                        'If calling CI/IoM 10p if PAYU / free if UL C&T. If calling RoI/RPP/RoW than no Charge',
                        'n/a',
                        '-'
                    ]
                    if str(country[1].iloc[8]) not in invalid_values:
                        try:
                            roaming_rate = round((country[1].iloc[8] * (math.ceil(int(duration_bytes) / 60))) * 100)
                        except ValueError:
                            roaming_rate = 0

                    else:
                        roaming_rate = 0

            df = pd.ExcelFile(price_data_path).parse('6b. IDD Roaming Leg')
            for country in df.iterrows():
                if country[1].iloc[0] == called_country:
                    idd_rate = round((country[1].iloc[6] * (math.ceil(int(duration_bytes) / 60))) * 100)

            b_party = b_numbers[called_country.upper()]
            exp_free_units = '0'
            exp_rating = int(roaming_rate) + int(idd_rate)

            # Roaming in RoW calling internationally roaming in uk special
        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location in UK_special and roaming_location != called_country:
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    if get_offer(api_endpoint, a_party):

                        roaming_rate = 0

                    else:
                        roaming_rate = 10

            df = pd.ExcelFile(price_data_path).parse('6b. IDD Roaming Leg')
            for country in df.iterrows():
                if country[1].iloc[0] == called_country:
                    idd_rate = round((country[1].iloc[6] * (math.ceil(int(duration_bytes) / 60))) * 100)

            b_party = b_numbers[called_country.upper()]
            exp_free_units = '0'
            exp_rating = int(roaming_rate) + int(idd_rate)


        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location not in UK_special and roaming_location == called_country:
            b_party = b_numbers[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        'No Charge',
                        'If calling CI/IoM 10p if PAYU / free if UL C&T. If calling RoI/RPP/RoW than no Charge',
                        'n/a',
                        '-',
                        '10p if PAYU / free if UL C&T'
                    ]
                    if str(country[1].iloc[8]) not in invalid_values:
                        exp_rating = round(int(country[1].iloc[8] * (math.ceil(int(duration_bytes) / 60))) * 100)

        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location in UK_special and roaming_location == called_country:
            b_party = b_numbers[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('5. International Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        'No Charge',
                        'If calling CI/IoM 10p if PAYU / free if UL C&T. If calling RoI/RPP/RoW than no Charge',
                        'n/a',
                        '-',
                        '10p if PAYU / free if UL C&T'
                    ]
                    if str(country[1].iloc[6]) not in invalid_values:
                        exp_rating = round(int(country[1].iloc[6] * (math.ceil(int(duration_bytes) / 60))) * 100)




    # SMS
    elif call_type == 'mo-sms':
        exp_free_units = '0'

        # Domestic SMS
        if roaming_location == 'UK' and called_country == 'UK':
            b_party = b_party_sms[called_country.upper()]
            if get_offer(api_endpoint, a_party):
                exp_free_units = '0'
                exp_rating = '0'
            else:
                exp_free_units = '0'
                exp_rating = '10'


        # IDD SMS
        elif roaming_location == 'UK' and called_country != 'UK':
            b_party = b_party_sms[called_country.upper()]

            if called_country.upper() in ci_iom:
                if get_offer(api_endpoint, a_party):
                    exp_rating = '0'
                else:
                    exp_rating = '10'
            else:
                df = pd.ExcelFile(price_data_path).parse('5. International Rate')
                for country in df.iterrows():
                    if country[1].iloc[0] == called_country:
                        exp_rating = round((country[1].iloc[7]) * 100)

        # Roaming SMS to UK
        elif roaming_location != 'UK' and called_country == 'UK':
            b_party = b_party_sms[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    if roaming_location in UK_special and get_offer(api_endpoint, a_party):
                        exp_rating = 30
                    else:
                        exp_rating = round(country[1].iloc[9] * 100)

        # Roaming SMS calling internationally
        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location.upper() not in UK_special:
            b_party = b_party_sms[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    value = str(country[1].iloc[9]).strip()
                    invalid_values = [
                        'No Charge',
                        ' If texting CI/IoM 30p if PAYU / free if UL C&T. If texting RoI/RPP/RoW than no Charge ',
                        'n/a',
                        '-'
                    ]
                    if value not in invalid_values:
                        try:
                            numeric_value = pd.to_numeric(value, errors="coerce")
                            roaming_rate = round(int(numeric_value * 100))

                        except ValueError:
                            roaming_rate = 0

                    else:
                        roaming_rate = 0
            df = pd.ExcelFile(price_data_path).parse('6b. IDD Roaming Leg')

            for country1 in df.iterrows():
                if country1[1].iloc[0] == called_country:
                    value = str(country1[1].iloc[7]).strip()
                    if country1[1].iloc[7] != 'Disabled':
                        numeric_value = (pd.to_numeric(value, errors="coerce"))

                        idd_rate = round(int(numeric_value * 100))

            exp_rating = int(roaming_rate) + int(idd_rate)

        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location.upper() in UK_special:
            b_party = b_party_sms[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    if get_offer(api_endpoint, a_party):
                        exp_rating = 30
                    else:
                        exp_rating = 0
        elif roaming_location != 'UK' and called_country != 'UK' and roaming_location.upper() in UK_special and roaming_location == called_country:
            b_party = b_party_sms[called_country.upper()]
            df = pd.ExcelFile(price_data_path).parse('5. International Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    exp_rating = round(int((country[1].iloc[7] * 100)))



    # MMS
    elif call_type == 'mms':
        exp_free_units = '0'
        b_party = b_numbers[called_country.upper()]

        # Domestic MMS
        if roaming_location == 'UK' and called_country == 'UK':
            exp_rating = '95'

        # Roaming MMS to UK
        elif roaming_location != 'UK' and called_country == 'UK':
            df = pd.ExcelFile(price_data_path).parse('6a. Roaming Rate')
            for country in df.iterrows():
                if country[1].iloc[0] == roaming_location:
                    invalid_values = [
                        'No Charge',
                        'If calling CI/IoM 30p if PAYU / free if UL C&T. If calling RoI/RPP/RoW than no Charge',
                        'n/a',
                        '-'
                    ]
                    if str(country[1].iloc[10]) not in invalid_values:
                        try:
                            exp_rating = round(country[1].iloc[10] * 100)
                        except ValueError:
                            exp_rating = 0

                    else:
                        exp_rating = 0

    return b_party, int(exp_rating), exp_free_units
