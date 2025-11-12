import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import numpy as np

db=mysql.connector.connect(
    host="localhost",
    username="root",
    password="root",
    database="ecommerce"
)

cur=db.cursor()

# 1. List all unique cities where customers are located.
query=""" select distinct customer_city from customers """
cur.execute(query)
data=cur.fetchall()
# print(data)


# 2. Count the number of orders placed in 2017.
query=""" select count(*) from orders where YEAR(order_purchase_timestamp)=2017 """
cur.execute(query)
data=cur.fetchall()
# print(data)


# 3. Find the total sales per category.
query=""" select products.product_category category, 
            round (sum(payments.payment_value),2) sales
            from products join order_items on
            products.product_id = order_items.product_id
            join payments on
            order_items.order_id = payments.order_id
            group by category
        """
cur.execute(query)
data=cur.fetchall() 
df=pd.DataFrame(data,columns=["Category","sales"])  #to frame the data
# print(df)


# 4. Calculate the percentage of orders that were paid in installments.
query=""" select 
            (sum(
                case when payment_installments >= 1 then 1 else 0 end
                ))/count(*)*100 from payments
        """
cur.execute(query)
data=cur.fetchall()
# print(data)


# 5. Count the number of customers from each state. 
query=""" select customer_state, count(customer_id) from customers
            group by customer_state
        """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data,columns=["State","Number of Customers"])
# print(df)
# plt.bar(df["State"],df["Number of Customers"])
# plt.xlabel("States")
# plt.ylabel("Number of Customers")
# plt.xticks(rotation=90)  #name at the bottom of bar table will be rotated by 90 degree
# plt.show()



# 6. Calculate the number of orders per month in 2018.
query=""" select MONTHNAME(order_purchase_timestamp) month, count(order_id) orders
            from orders
            where YEAR(order_purchase_timestamp)=2018
            group by month
        """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data,columns=["Month","Number of Orders"])
# print(df)
# o=["January","February","March","April","May","June","July","August","September","October","November","December"]
# ax=sns.barplot(x=df["Month"],y=df["Number of Orders"],data=df, order=o)
# ax.bar_label(ax.containers[0])  #to show the number on top of bar
# plt.show()


# 7. Find the average number of products per order, grouped by customer city.
query=""" with count_per_order as (
            select orders.order_id, orders.customer_id,
            count(order_items.order_id) as oc
            from orders
            join order_items on
            orders.order_id = order_items.order_id
            group by orders.order_id, orders.customer_id)

            select customers.customer_city,
            round(avg(count_per_order.oc),2) 
            from customers
            join count_per_order on
            customers.customer_id = count_per_order.customer_id
            group by customers.customer_city
        """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data,columns=["Customer City","Avg Products per Order"])
# print(df)



# 8. Calculate the percentage of total revenue contributed by each product category.
query="""  select upper(products.product_category) category,
            round(sum(payments.payment_value)/(select sum(payment_value) from payments)*100,2)
            as category_sales
            from products
            join order_items on
            products.product_id = order_items.product_id
            join payments on
            order_items.order_id = payments.order_id
            group by category order by category_sales desc

        """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data,columns=["Product Category","Percentage of Total Revenue"])
# print(df)


# 9. Identify the correlation between product price and the number of times a product has been purchased.
query="""  select products.product_category, 
            count(order_items.product_id),
            round(avg(order_items.price),2)
            from products
            join order_items on
            products.product_id = order_items.product_id
            group by products.product_category
        """
cur.execute(query)
data=cur.fetchall()
df=pd.DataFrame(data,columns=["Product category","Purchase Count","Average Price"])
print(df)

arr1=df["Purchase Count"]
arr2=df["Average Price"]
correlation=np.corrcoef(arr1,arr2)
# corelation exists between -1 to 1
print("Correlation between product price and number of times a product has been purchased:\n", correlation)  # there is no empact of price on purchase count