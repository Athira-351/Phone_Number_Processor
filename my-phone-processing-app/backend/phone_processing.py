import re
import phonenumbers
import pandas as pd
import os

# Define similar names for the 'Phone_Number' column
POSSIBLE_PHONE_COLUMNS = ['Phone_Number','Mobile_Number','phone number','mobile number', 'Number','number','num', 'Num', 'mobile', 'Phone']

# AI-based method to extract a phone number from mixed data
def extract_phone_number_from_text(text):
    # Regex pattern to find phone numbers
    # for numbers like +1-800-555-1234, (123) 456-7890, +44 20 1234 5678, 555.1234, +91-9876543210
    pattern = re.compile(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}')
    matches = pattern.findall(str(text))
    
    for match in matches:
        try:
            parsed_number = phonenumbers.parse(match, None)
            if phonenumbers.is_possible_number(parsed_number) and phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            continue
    return None

def process_phone_number(raw_number):
    try:
        raw_number = str(raw_number).strip()

        if not raw_number.startswith('+'):
            raw_number = '+' + raw_number

        number = phonenumbers.parse(raw_number, None)

        if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
            return pd.Series([None, None, None])

        formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        dialing_code = f"+{number.country_code}"
        phone_number_without_code = str(number.national_number)

        return pd.Series([formatted_number, dialing_code, phone_number_without_code])
    
    except phonenumbers.NumberParseException:
        return pd.Series([None, None, None])

def process_excel_file(file_path):
    df = pd.read_excel(file_path)

    # Identify the 'Phone_Number' column or similar ones
    phone_col = None
    for col in df.columns:
        if col.lower() in [name.lower() for name in POSSIBLE_PHONE_COLUMNS]:
            phone_col = col
            break
    
    if phone_col:
        df.rename(columns={phone_col: 'Phone_Number'}, inplace=True)
    else:
        # Try to extract phone numbers from mixed data if no suitable column is found
        df['Phone_Number'] = df.apply(lambda row: extract_phone_number_from_text(' '.join(map(str, row.values))), axis=1)

    if 'Phone_Number' not in df.columns:
        raise ValueError("The Excel file does not contain a 'Phone_Number' column.")

    # Apply phone number processing
    df[['Phone Number Formatted', 'Dialing_Code', 'Phone_Number_Without_Code']] = df['Phone_Number'].apply(process_phone_number)

    output_file = os.path.join('processed', f'processed_{os.path.basename(file_path)}')
    df.to_excel(output_file, index=False)  # Save the processed data as an Excel file

    return output_file


# import phonenumbers
# import pandas as pd
# import os

# def process_phone_number(raw_number):
#     try:
#         raw_number = str(raw_number).strip()

#         if not raw_number.startswith('+'):
#             raw_number = '+' + raw_number

#         number = phonenumbers.parse(raw_number, None)

#         if not phonenumbers.is_possible_number(number) or not phonenumbers.is_valid_number(number):
#             return pd.Series([None, None, None])

#         formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
#         dialing_code = f"+{number.country_code}"
#         phone_number_without_code = str(number.national_number)

#         return pd.Series([formatted_number, dialing_code, phone_number_without_code])
    
#     except phonenumbers.NumberParseException:
#         return pd.Series([None, None, None])

# def process_excel_file(file_path):
#     df = pd.read_excel(file_path)

#     if 'Phone_Number' not in df.columns:
#         raise ValueError("The Excel file does not contain a 'Phone_Number' column.")

#     df[['Phone Number Formatted', 'Dialing_Code', 'Phone_Number_Without_Code']] = df['Phone_Number'].apply(process_phone_number)

#     output_file = os.path.join('processed', f'processed_{os.path.basename(file_path)}')
#     df.to_excel(output_file, index=False)  # Save the processed data as an Excel file

#     return output_file
