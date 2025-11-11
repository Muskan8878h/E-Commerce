import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

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
o=["January","February","March","April","May","June","July","August","September","October","November","December"]
ax=sns.barplot(x=df["Month"],y=df["Number of Orders"],data=df, order=o)
ax.bar_label(ax.containers[0])  #to show the number on top of bar
plt.show()


# 7. Find the average number of products per order, grouped by customer city.
query=""" select c.customer_city, 
            round (avg(oi_count.product_count),2) avg_products_per_order
            from customers c join orders o on
            c.customer_id = o.customer_id
            join (
                select order_id, count(product_id) product_count
                from order_items
                group by order_id
            ) oi_count on
            o.order_id = oi_count.order_id
            group by c.customer_city
        """