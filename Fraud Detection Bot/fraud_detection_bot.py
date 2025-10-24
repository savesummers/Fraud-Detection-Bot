import pandas as pd
from serpapi import GoogleSearch                                          

class Import_Data():
    '''Imports the monthly transactions list of the client'''
    
    def __init__(self, file_name = r'C:\Users\mssam\OneDrive\Desktop\COMPUTER NOTES\PYTHON\PROJECTS\Fraud Detection Bot\Case Study #1(Case Study).csv', file_name_2 = r'C:\Users\mssam\OneDrive\Desktop\COMPUTER NOTES\PYTHON\PROJECTS\Fraud Detection Bot\office-of-foreign-assets-control-(ofac)-countries-2025.csv' ):
        self.df = pd.read_csv(file_name)
        self.da = pd.read_csv(file_name_2)
        print(self.da.head())
        print(self.df.head())
        
        #Dictionaries with flagged countries
        self.Sanctioned_Country = self.da.to_dict(orient='index')
        self.TAFT_High_Risk = ['DPRK', 'IR', 'MM', 'DZ', 'AO', 'BO', 'BG', 'BF', 'CM', 'CI', 'CD', 'HT', 'KE', 'LA', 'LB', 'MC', 'MZ', 'NA', 'NP', 'NG', 'ZA', 'SS', 'SY', 'VE', 'VN', 'VG', 'YE'] #TAFT countries under high monitoring and labelled as high risk
        
        #Dictionaries to store flagged transactions
        self.Large_Transactions = {} #Transactions >= 10000 as i decided to use us and uk reporting threshold
        self.Number_of_Cash_Trasactions =  {} #Cash transactions should not be more than 40% the total days reporting threshold is >= 3 per week
        self.Number_of_Trasactions = {} #If more than 3 transactions per week
        self.Cummulative_Cash_Ammount = {}  #Total cash transactions >= 10000 same as large transaction threshold
        self.Cash_Intensive_or_High_Risk_Sectors = {} #Casinos and gambling, Real estate, Precious metals/jewelry, Crypto exchanges, NGOs or charities (in certain jurisdictions), Money service businesses (MSBs)
        self.Sanctioned_Country_Confirmed ={} #Transactions with countries in  OFAC list
        self.TAFT_High_Risk_Confirmed = {} #TAFT countries under high monitoring and labelled as high risk
        
        
        #Dictionary to store client transaction history
        self.Raw_transaction_data = {}
        column_names = ['Datestart','Charge','Debit/Credit','TransactionCode','Name_Counterparty','Counterparty_Country']
        self.Raw_transaction_data = {idx+1: row.tolist() for idx, row in self.df[column_names].iterrows()}
        print(self.Raw_transaction_data)
        self.data_to_delete = list(range(66,80))
        for key in self.data_to_delete:
            self.Raw_transaction_data.pop(key, None)
            print(self.Raw_transaction_data)
        
class Red_Flags(Import_Data):
    '''Identify Red Flags from Transacfion list of client'''
    
    def Sort_Large_Transactions(self):
        
        for self.key, self.value in self.Raw_transaction_data.items():
            
            try:
                charge_str = str(self.value[1]).replace(',', '')
                charge = float(charge_str)
                if abs(charge) >= 10000:
                    self.Large_Transactions[self.key] = self.value
            except (ValueError, IndexError) as e:
                print(f"Error processing transaction {self.key}: {e}")
                continue
        
        print('\nList of Large Transactions found:')    
        print(self.Large_Transactions)
        
    def Sort_TAFT_High_Risk(self):
        
        
        for key, value in self.Raw_transaction_data.items():
            country_code = value[-1]
            if country_code in self.TAFT_High_Risk:
                self.TAFT_High_Risk_Confirmed[key] = value
        
        print('\nList of TAFT_High_Risk_Confirmed Countries:')    
        print(self.TAFT_High_Risk_Confirmed)
        
    def Sort_Sanctioned_Country(self):
        
        print('\n List of Sanctioned_Country:')
        print(self.Sanctioned_Country)
        
        self.sanctioned_country_codes = {entry['flagCode'] for entry in self.Sanctioned_Country.values()}
        
        for key, value in self.Raw_transaction_data.items():
            self.transaction_country_code = value[-1].strip().upper() 
            if self.transaction_country_code in self.sanctioned_country_codes:
                self.Sanctioned_Country_Confirmed[key] = value
                
        print('\nList of Sanctioned Country Confirmed:')
        print(self.Sanctioned_Country_Confirmed)
                
    def web_scrapping(self, query):
        
        API_KEY = 'ENTER YOUR API KEY' 
        params = {'engine':'google', 'q':query, 'api_key': API_KEY}   
        search = GoogleSearch(params)
        results = search.get_dict()
        snippets = [r['snippet'] for r in results.get('organic_results', []) if 'snippet' in r]   
        if snippets:
            print(f"\n🔍 Search results for query: '{query}'")
            print(f"📝 Top snippet: {snippets[0]}\n")
        else:
            print(f"\n❌ No snippet found for query: '{query}'\n")
        return' '.join(snippets).lower()
    
    def Sort_Cash_Intensive_or_High_Risk_Sectors(self):
        
        keywords = ['casino', 'gambling', 'real estate', 'precious metals', 'jewelry','crypto exchange', 'ngo', 'charity', 'charities', 'money service business', 'msb']
        
        for key, value in self.Raw_transaction_data.items():
            
            counterparty_name = value[4]
            query = f'{counterparty_name}'
            
            try:
                text = self.web_scrapping(query)
                if any(keyword in text for keyword in keywords):
                    self.Cash_Intensive_or_High_Risk_Sectors[key] = value
            except Exception as e:
                print(f"Web scraping error for transaction {key}: {e}")
                continue

        print('\nCash Intensive or High-Risk Sector Transactions:')
        print(self.Cash_Intensive_or_High_Risk_Sectors)
        
    def Sort_Number_of_Trasactions(self):
        
        months = {'January': 0,'February': 0,'March': 0,'April': 0, 'May': 0,'June': 0,'July': 0,'August': 0,'September': 0,'October': 0,'November': 0,'December': 0}
        
        for key, value in self.Raw_transaction_data.items():
            
            dates = value[0]

            if str(dates).startswith('11'):
                months['November']  +=  1
            elif str(dates).startswith('12'):
                months['December']  +=   1  
            elif str(dates).startswith('10'):
                months['October']  +=   1          
            elif str(dates).startswith('1'):
                months['January'] += 1
            elif str(dates).startswith('2'):
                months['February'] +=  1
            elif str(dates).startswith('3'):
                months['March'] +=  1
            elif str(dates).startswith('4'):
                months['April'] +=  1
            elif str(dates).startswith('5'):
                months['May'] +=   1
            elif str(dates).startswith('6'):
                months['June'] +=   1
            elif str(dates).startswith('7'):
                months['July'] +=   1
            elif str(dates).startswith('8'):
                months['August']  +=   1
            elif str(dates).startswith('9'):
                months['September']  +=  1
        
        print('\nNumber of transactions per month')
        print(months)



        
        for key, value in months.items():
            if int(value)/4.345 >= 3:
                self.Number_of_Trasactions[key] = value
            else:
                continue
            
        print(f'\nMonths with 3 or more Transactions Per Week:\n {self.Number_of_Trasactions}')
        return len(self.Number_of_Trasactions)>0
        
    def Sort_Cummulative_Cash_Ammount(self):
        
        total_amount = 0
    
        for key, value in self.Raw_transaction_data.items():
            transaction_code = value[3]
            amount = str(value[1]).replace(',','')
            amount_f = amount.replace('-','')
            
            if transaction_code == 'SCRDT':
                self.Cummulative_Cash_Ammount[key]= value
                total_amount += float(amount_f)
            elif transaction_code == 'SDR':
                self.Cummulative_Cash_Ammount[key]= value
                total_amount += float(amount_f)
            elif transaction_code == 'DR':
                self.Cummulative_Cash_Ammount[key]= value
                total_amount += float(amount_f)
            elif transaction_code == 'SCDR':
                self.Cummulative_Cash_Ammount[key]= value
                total_amount += float(amount_f)
            else: 
                continue
        
        print(f'Total sum of cash transaction amounts: {total_amount}') 
        return total_amount>10000
        
    def Sort_Number_of_Cash_Trasactions(self):
        
        self.Number_of_Cash_Trasactions = self.Cummulative_Cash_Ammount
        self.result_of_cash = len(self.Number_of_Cash_Trasactions)
        print(f'Total Sum of Cash Transactions: {self.result_of_cash}')
        
        return self.result_of_cash >= 3
            
class Detection_Results(Red_Flags):
    '''Output Results of Fraud Detection Process'''
    def __init__(self, TAFT_High_Risk_Confirmed, Number_of_Trasactions, Cash_Intensive_or_High_Risk_Sectors,Sanctioned_Country_Confirmed, Cummulative_Cash_Ammount,Number_of_Cash_Trasactions, Large_Transactions):
        self.Large_Transactions = Large_Transactions
        self.Number_of_Cash_Trasactions =  Number_of_Cash_Trasactions
        self.Cummulative_Cash_Ammount =  Cummulative_Cash_Ammount
        self.Cash_Intensive_or_High_Risk_Sectors = Cash_Intensive_or_High_Risk_Sectors
        self.TAFT_High_Risk_Confirmed = TAFT_High_Risk_Confirmed
        self.Sanctioned_Country_Confirmed = Sanctioned_Country_Confirmed
        self.Number_of_Trasactions = Number_of_Trasactions
        
    def create_sheet(self, new_file='Fraud_Detection_Results.txt'):
        
        lines=[]
        lines.append('===Red Flags Detected===\n')
        lines.append('\nLarge Transactions Detected\n')
        for name, value in self.Large_Transactions.items():
            lines.append(f'{name} - ${value}')
        lines.append('\nTAFT High Risk Countries Detected\n')
        for name, value in self.TAFT_High_Risk_Confirmed.items():
            lines.append(f'{name} - ${value}')
        lines.append('\nSanctioned Countries Detected\n')
        for name, value in self.Sanctioned_Country_Confirmed.items():
            lines.append(f'{name} - ${value}')
        lines.append('\nCash_Intensive_or_High_Risk_Sectors Transactions Detected\n')
        for name, value in self.Cash_Intensive_or_High_Risk_Sectors.items():
            lines.append(f'{name} - ${value}')         
        lines.append(f'\nCummulative Amount of Cash Greater than 10000:  {cummulative}\n')
        lines.append(f'\nNumber of Trasactions is more than 3 a week:  {trans_number}\n')
        lines.append(f'\nNumber of Cash Trasactions is more than 3 a week:  {cash_number}\n')

        with open(new_file, "w") as f:
            for line in lines:
                f.write(line + "\n")

        print(f"\nFraud Detection Results'{new_file}'")        

        
        
        
                                                   
        
data = Import_Data()
data_detection = Red_Flags()
data_detection.Sort_Large_Transactions()
data_detection.Sort_TAFT_High_Risk()
data_detection.Sort_Sanctioned_Country()
data_detection.Sort_Cash_Intensive_or_High_Risk_Sectors()
data_detection.Sort_Number_of_Trasactions()
data_detection.Sort_Cummulative_Cash_Ammount()
data_detection.Sort_Number_of_Cash_Trasactions()
cummulative = data_detection.Sort_Cummulative_Cash_Ammount()
trans_number = data_detection.Sort_Number_of_Trasactions()
cash_number = data_detection.Sort_Number_of_Cash_Trasactions()
f_results = Detection_Results(
    TAFT_High_Risk_Confirmed = data_detection.TAFT_High_Risk_Confirmed,
    Number_of_Trasactions = data_detection.Number_of_Trasactions,
    Cash_Intensive_or_High_Risk_Sectors = data_detection.Cash_Intensive_or_High_Risk_Sectors,
    Sanctioned_Country_Confirmed = data_detection.Sanctioned_Country_Confirmed,
    Cummulative_Cash_Ammount = data_detection.Cummulative_Cash_Ammount,
    Number_of_Cash_Trasactions = data_detection.Number_of_Cash_Trasactions,
    Large_Transactions = data_detection.Large_Transactions
)
f_results.create_sheet() 
