import re
from collections import defaultdict

def parse_drug_entries(database_entries):
    # Dictionary to hold parsed results
    parsed_results = {}

    # Updated regex to accurately capture and process numbers with decimals
    # This pattern aims to avoid duplicating decimal parts in the output
    regex_pattern = r"(?:(\d+)X)?(\d+(\.\d+)?)\s*(K)?\s*([A-Za-z%]+)"

    for entry in database_entries:
        # Finding all matches according to the updated regex pattern
        matches = re.findall(regex_pattern, entry, re.IGNORECASE)

        entry_metrics = defaultdict(list)

        for match in matches:
            quantity, value, decimal_part, thousands, unit = match

            # Check and adjust for 'K' in value, converting to thousands if necessary
            if thousands.upper() == 'K':
                value = f"{float(value) * 1000}"
            # No need to append decimal part explicitly; it's included in 'value'

            unit = unit.upper()  # Normalize the unit to uppercase
            
            # Append the value directly as it includes the decimal part correctly
            entry_metrics[unit].append(value)

        # Extract the drug name, assuming the first word before the first number is the name
        drug_name_match = re.search(r"^[A-Za-z]+", entry)
        if drug_name_match:
            drug_name = drug_name_match.group(0)
        else:
            drug_name = "Unknown Drug"  # Fallback in case no name is found

        # Assign the collected metrics to the drug name in the result dictionary
        parsed_results[drug_name] = dict(entry_metrics)

    return parsed_results

# Sample database entries, including values with decimals
database_entries = [
    "BETAMETHASONE DIP AUG 0.05% GE",
    "HYDROCORTISONE 2.5% CRM 28.35 ",
    "NARATRIPTAN 1 MG TAB 9        ",
    "NARATRIPTAN 2.5 MG TAB 9      ",
    "DIALYVITE 3K MULT VIT TAB 90  ",
    "TIMOLOL O/S 0.25 % DRP 5 ML   ",
    "TIMOLOL 0.5% O/S 5 ML         ",
    "MICARDIS HCT 80-25MG TAB (3X10",
    "MICARDIS HCT 80-12.5 MG TAB 30",
    "MICARDIS 80 MG TAB 30         ",
    "SENNA 528 MG SYR 40X15 ML UD  ",
    "GNP CALAMINE PLAIN LIQ 6 OZ   ",
    "AMOXICILLN-CLAV 250-62.5MG-5ML",
    "NICOTINE GUM 2MG REGULAR 20CT ",
    "AMOXICILLIN-CLAV 250-62.5MG-5M",
    "TIMOLOL 0.25 % O/S 5 ML       ",
    "AMOXICILLN-CLAV 250-62.5MG-5ML",
    "MICARDIS HCT 40-12.5MG TAB 30 ",
]

parsed_drug_info = parse_drug_entries(database_entries)

# Displaying the parsed information accurately, without duplicated decimal parts
for drug, metrics in parsed_drug_info.items():
    print(f"\n Drug: {drug}")
    for unit, values in metrics.items():
        for value in values:
            print(f"  {unit}: {value}")
