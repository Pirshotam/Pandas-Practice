import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

january_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_January_2019.csv")
february_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_February_2019.csv")
march_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_March_2019.csv")
april_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_April_2019.csv")
may_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_May_2019.csv")
june_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_June_2019.csv")
july_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_July_2019.csv")
august_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_August_2019.csv")
september_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_September_2019.csv")
october_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_October_2019.csv")
november_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_November_2019.csv")
december_data = pd.read_csv("C:/codes/Python/Pandas Practice/Sales_Data/Sales_December_2019.csv")

monthly_dataset= [january_data, february_data, march_data, april_data, may_data, june_data, july_data, august_data, september_data, october_data, november_data, december_data,]
yearly_data = pd.concat(monthly_dataset, ignore_index=True)
all_data = yearly_data.to_csv("all_data.csv", index=False)

#What is the best month for sales and what was the revenue for that month?
#We first clean the dataset and then convert "Order Date" to datetime object
#1. Filter out the literal header text rows
yearly_data = yearly_data[yearly_data["Order Date"] != "Order Date"]
#2. Filter out any completely blank/empty text strings
yearly_data = yearly_data[yearly_data["Order Date"].str.strip() != ""]
#3. Drop existing true NaN rows
yearly_data.dropna(inplace=True)
#4. Now convert safely (the count will remain perfectly stable!)
yearly_data["Order Date"] = pd.to_datetime(yearly_data["Order Date"], format="mixed")
#Extract Month and Create a Month Column
yearly_data["Month"] = yearly_data["Order Date"].dt.month_name()
#Convert Quantity Ordered to int16 and Price Each to float
yearly_data["Quantity Ordered"] = yearly_data["Quantity Ordered"].astype("int16")
yearly_data["Price Each"] = pd.to_numeric(yearly_data["Price Each"])
yearly_data["Sales"]= yearly_data["Quantity Ordered"] * yearly_data["Price Each"]
monthly_sales = yearly_data.groupby("Month")["Sales"].sum()
best_month = monthly_sales.idxmax()
highest_revenue = monthly_sales.max()
print(f"The best month for sales: {best_month}, Revenue was {highest_revenue}")
print()
#Extract keys (months) and values (sales) directly from your monthly_sales series
months = monthly_sales.index
sales_totals = monthly_sales.values
#Creates a bar graph
plt.bar(months, sales_totals)
#rotates the months by 45 degree to avoid text overlapping
plt.xticks(months, rotation=45)
#labels y axis
plt.ylabel('Sales in USD ($)')
#labels x-axis
plt.xlabel('Month')
#Names what the plot is for
plt.title('Total Sales per Month')
#Shows the plot
plt.show()


#What city has the most sales?
#Creating a city, State column
#Method 1
# yearly_data["City"] = yearly_data["Purchase Address"].apply(lambda x: x.split(", ")[1] +", "+ x.split(", ")[2].split()[0])
#Method 2
yearly_data["City"] = yearly_data["Purchase Address"].str.split(",").str[1].str.strip() +", "+yearly_data["Purchase Address"].str.split(",").str[2].str.split().str[0].str.strip()

highest_sales_city = yearly_data.groupby("City")["Sales"].sum()
best_city = highest_sales_city.idxmax()
best_city_sales = highest_sales_city.max()
print(f"The city with highest number of sales: {best_city}. It sold: {best_city_sales}")
print()
city = highest_sales_city.index
sales = highest_sales_city.values
#Create a Bar Graph
plt.bar(city, sales)
#rotates the months by 45 degree to avoid text overlapping
plt.xticks(city, rotation=45)
#labels y axis
plt.ylabel('Sales in USD ($)')
#labels x-axis
plt.xlabel('City')
#Names what the plot is for
plt.title('Total Sales per City')
#Shows the plot
plt.show()


#What time should we display advertisements to maximize likelihood of customer's buying product?
yearly_data["Hour"] = yearly_data["Order Date"].dt.hour
yearly_data["Minute"] = yearly_data["Order Date"].dt.minute
best_time = yearly_data.groupby("Hour")["Sales"].count()
most_frequent_time = best_time.idxmax()
second_frequent_time = best_time.nlargest(2).index[1]
print(f"We should display advertisements at: {most_frequent_time}th or {second_frequent_time}th hour of the day")
print()
sales_time= best_time.index
sales_count= best_time.values
#Create a line graph
plt.plot(sales_time, sales_count)
#Shows all x-axis hours
plt.xticks(sales_time)
#labels y axis
plt.ylabel('Sales count')
#labels x-axis
plt.xlabel('Hour')
#Names what the plot is for
plt.title('Sales Count At Specific Time')
#Show grid lines
plt.grid()
#Shows the plot
plt.show()


#What products are most often sold together?
df = yearly_data[yearly_data["Order ID"].duplicated(keep=False)].copy()
df["Grouped Product"] = df.groupby("Order ID")["Product"].transform(lambda x: ", ".join(sorted(x)))
df = df[["Order ID", "Grouped Product"]].drop_duplicates()
most_sold_together = df.groupby("Grouped Product")["Order ID"].count()
most_often_sold_together = most_sold_together.idxmax()
second_most_often_sold_together = most_sold_together.nlargest(2).index[1]
print(f"The most often sold together products are: {most_often_sold_together}.\nThe second most are: {second_most_often_sold_together}")
print()
sold_together= most_sold_together.sort_values(ascending=False).head(10).index
frequency= most_sold_together.sort_values(ascending=False).head(10).values
#Create a Bar Graph
plt.bar(sold_together, frequency)
#rotates the Grouped products by 45 degree to avoid text overlapping
plt.xticks(sold_together, rotation="vertical")
#labels y axis
plt.ylabel('Frequency')
#labels x-axis
plt.xlabel('Grouped Products')
#Names what the plot is for
plt.title('Products Often Sold Together')
#Shows the plot
plt.show()


#What product sold the most?
most_sold_product = yearly_data.groupby("Product")["Quantity Ordered"].sum()
prices = yearly_data.groupby("Product")["Price Each"].mean()
most_sold = most_sold_product.idxmax()
print(f"The most sold product is: {most_sold}")
print()
product_names= most_sold_product.index
quantity= most_sold_product.values
#Creating an overlaying graph
#1. Create the base figure and the first axis (ax1)
fig, ax1 = plt.subplots()
#2. Plot the Bar Chart on the first axis
ax1.bar(product_names, quantity, color='g') # Made it green for contrast
ax1.set_xlabel('Product')
ax1.set_ylabel('Quantity Ordered', color='g')
ax1.set_title('Most Product Sold vs Price')
ax1.set_xticks(range(len(product_names))) #maps out an equal spacing marker for every item in your product list
ax1.set_xticklabels(product_names, rotation="vertical")
#3. Create a second y-axis (ax2) sharing the same x-axis
ax2 = ax1.twinx()
#4. Plot your secondary data (e.g., prices) as a Line Chart on ax2
ax2.plot(product_names, prices, color='b') 
ax2.set_ylabel('Price ($)', color='b')
#5. Prevent label clipping and display
plt.tight_layout()
plt.show()


