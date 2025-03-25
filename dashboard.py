import pandas as pd

# Create a DataFrame from the provided data
data = {
    "Team/Dashboard": ["USERS"] * 18 + ["DEPOSITS"] * 8 + ["NIP"] * 6 + ["TRANSFER"] * 8 + ["WITHDRAWAL"] * 12 + ["BILLSPAYMENT"] * 8 +
                       ["REFERRALS"] * 3 + ["COMMISSIONS PAYMENT"] * 20 + ["REVENUE"] * 20 + ["ATM CARD"] * 6 + ["PAYMENT REQUEST"] * 14 +
                       ["INVOICING"] * 6 + ["SCAN AND PAY"] * 4 + ["USSD"] * 4 + ["CARD payment gateway"] * 4 + ["POS TERMINALS"] * 3 +
                       ["POS"] * 36 + ["LOAN"] * 6 + ["KYC verification"] * 2 + ["SMS"] * 14 + ["Account creation and login"] * 24 +
                       ["PROFILING"] * 34,
    "SUB": ["Total", "Total", "Total", "Business users", "Business users", "Business users", "Personal users", "Personal users", "Personal users",
            "Aggregators", "Aggregators", "Aggregators", "Agents", "Agents", "Agents", "Each of the business user category (", 
            "Each of the business user category (", "Each of the business user category ("] +
           ["Total deposits", "Total deposits", "Personal deposits", "Personal deposits", "Business deposits", "Business deposits", 
            "Deposits per channel", "Deposits per channel"] +
           ["NIP INWARD", "NIP INWARD", "NIP OUITWARD", "NIP OUITWARD", "NIP OUTWARD 10K AND ABOVE", "NIP OUTWARD 10K AND ABOVE"] +
           ["Own account transfer", "Own account transfer", "transfer to phone number", "transfer to phone number", 
            "transfer to phone email address", "transfer to phone email address", "WITHDRAWAL", "WITHDRAWAL"] +
           ["total withdrawal", "total withdrawal", "Inter withdrawal", "Inter withdrawal", "External withdrawal", "External withdrawal",
            "Billspayment withdrawal", "Billspayment withdrawal", "Billspayment withdrawal - BAXI", "Billspayment withdrawal - BAXI",
            "Billspayment withdrawal - QuickTeller", "Billspayment withdrawal - QuickTeller"] + 
           ["Total value of referrals payment"] * 3 + 
           ["TOTAL commission payment"] * 20 + 
           ["Total Revenue"] * 20 + 
           ["ATM CARD"] * 6 + 
           ["total payment request"] * 14 +
           ["total invoicing"] * 6 +
           ["scan and pay incoming "] * 4 +
           ["USSD incoming "] * 4 +
           ["Card payment gateway incoming "] * 4 +
           ["ISSUED POS TERMINALS"] * 3 +
           ["POS successful transactions"] * 36 +
           ["Total loan issued"] * 6 +
           ["Sucessful KYC"] * 2 +
           ["TOTAL SMS"] * 14 +
           ["Account Creation"] * 24 +
           ["Profiling"] * 34,
    "Description": ["Number of users", "Number of active users", "Number of inactive users"] * 6 + ["Total value of deposits"] * 8 + 
                    ["Total value of NIP"] * 6 + ["Total value of transfer"] * 8 + ["Total value of withdrawals"] * 12 +
                    ["Value of Billspayment"] * 8 + ["Value of referrals"] * 3 + ["Value of commissions"] * 20 +
                    ["Revenue breakdown"] * 20 + ["ATM transactions"] * 6 + ["Payment requests"] * 14 +
                    ["Invoicing details"] * 6 + ["Scan and Pay"] * 4 + ["USSD"] * 4 + ["Card Payment Gateway"] * 4 +
                    ["POS Terminals"] * 3 + ["POS transactions"] * 36 + ["Loan details"] * 6 + ["KYC verification"] * 2 +
                    ["SMS details"] * 14 + ["Account creation and login"] * 24 + ["Profiling details"] * 34,
    "Account type": ["Business and Personal"] * 262,
    "Info": [None] * 262,
    "Source Data": [None] * 262,
    "Database Table": [None] * 262
}

df = pd.DataFrame(data)

# Display the first few rows for review
import ace_tools as tools; tools.display_dataframe_to_user(name="Wayabank Dashboard Metrics", dataframe=df)
