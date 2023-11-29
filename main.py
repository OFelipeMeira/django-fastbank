from dateutil.relativedelta import relativedelta
from datetime import date

if __name__ == "__main__":
    value = 5000
    fees = 1.025
    install = 3

    a = round( (value/install * fees) ,2) 
    print( a )
