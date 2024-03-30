import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    "Seller ID": ["S447", "S126", "S873", "S563", "S416", "S148", "S329", "S848", "S302", "S321","S420","S478","S370"],
    "Seller Name": ["Seller S447", "Seller S126", "Seller S873", "Seller S563", "Seller S416", "Seller S148", "Seller S329", "Seller S848", "Seller S302", "Seller S321","Seller 420","Seller 478","Seller 370"],
    "City, State": ["Chennai, Tamil Nadu", "Bengaluru, Karnataka", "Chennai, Tamil Nadu", "Mumbai, Maharashtra", "Mumbai, Maharashtra", "Srinagar, J&K", "Mumbai, Maharashtra", "Delhi, NCR", "Bengaluru, Karnataka", "Srinagar, J&K","Indore,Madhya Pradesh","Hyderabad,Telangana","Patna,Bihar"],
    "Brands Offered": [['Home Center','Fabindia','Good Earth','Gantri'],['Prada','Biba'],['Samsung India Electronics','LG Electronics India','Whirlpool India'],['Pigeon', 'boAt', 'Mysore Silk Sarees', 'Bajaj'], ['Bajaj', 'Havells', 'Zebronics'], ['Mysore Silk Sarees', 'Pigeon', 'boAt', 'Kanchipuram Saris'], ['Manyavar', 'Zebronics', 'Havells', 'Usha'], ['Pigeon', 'Lava Mobiles', 'Kanchipuram Saris'], ['Kanchipuram Saris', 'Manyavar', 'Lava Mobiles'], ['Pigeon'], ['Bajaj', 'Lava Mobiles', 'Usha', 'Havells'], ['boAt', 'Pigeon', 'Usha', 'Flipkart (in-house)'], ['Kanchipuram Saris', 'Usha']],
    "Product Categories": [['Home Decor'],['Clothing'],['Home Appliances'],['Accessories'], ['Home Decor', 'Appliances', 'Electronics', 'Accessories'], ['Mobiles', 'Home Decor', 'Clothing', 'Appliances'], ['Bakeware', 'Mobiles', 'Handicrafts'], ['Bakeware'], ['Accessories', 'Clothing', 'Home Decor', 'Handicrafts'], ['Clothing', 'Kitchenware'], ['Ethnic Wear', 'Home Decor', 'Mobiles', 'Clothing'], ['Kitchenware', 'Handicrafts'], ['Ethnic Wear', 'Mobiles', 'Electronics', 'Kitchenware']],
    "Average Rating": [4.5,4.4,4.8,4.1,4.9, 4.2, 5.0, 4.7, 4.7, 4.5, 4.2, 4.8, 4.4],
    "Number of Reviews": [13.0, 19.5, 16.6, 6.7, 15.9, 18.8, 12.8, 12.4, 17.2, 15.6,13.6,15.5,16.9],
    "Total Sales": [25.4, 44.5, 11.8, 36.6, 35.8, 20.0, 24.9, 29.3, 9.1, 10.1,31.2,11.1,9.3],
    "Average Order Value (₹)": [3054, 1912, 4283, 4109, 4242, 3075, 4306, 2923, 4115, 4281,3245,2135,1890],
    "Response Time (hrs)": [9, 13, 1, 5, 1, 14, 1, 9, 6, 16,10,8,19]# Total No: 13
}

df = pd.DataFrame(data)

# Streamlit app
st.title("Seller, Brand, and Tags Visualization")

# Display the data
st.subheader("Seller Data")
st.dataframe(df)

# Create a mapping engine
class CatalogMappingEngine:
    def __init__(self, data):
        self.data = data

    def get_brand_info(self, brand_name):
        return self.data[self.data["Brands Offered"].apply(lambda x: brand_name in x)]

    def get_seller_info(self, seller_id):
        return self.data[self.data["Seller ID"] == seller_id]

# Instantiate the mapping engine
mapping_engine = CatalogMappingEngine(df)

# Visualize Brand Information
st.subheader("Visualize Brand Information")

selected_brand = st.selectbox("Select Brand", df["Brands Offered"].explode().unique())
brand_info = mapping_engine.get_brand_info(selected_brand)

if not brand_info.empty:
    st.write(f"Information for Brand: {selected_brand}")
    st.dataframe(brand_info)

    # Plot the distribution of average ratings
    st.write(f"Average Rating Distribution for {selected_brand}")
    fig, ax = plt.subplots()
    ax.hist(brand_info["Average Rating"], bins=10, edgecolor="black")
    st.pyplot(fig)

# Visualize Seller Information
st.subheader("Visualize Seller Information")

selected_seller = st.selectbox("Select Seller", df["Seller ID"].unique())
seller_info = mapping_engine.get_seller_info(selected_seller)

if not seller_info.empty:
    st.write(f"Information for Seller: {selected_seller}")
    st.dataframe(seller_info)

# Visualize Tags Mapping
st.subheader("Visualize Tags Mapping")

# Plot the number of sellers in each product category
tags_mapping = {}
for categories in df["Product Categories"]:
    for category in categories:
        if category not in tags_mapping:
            tags_mapping[category] = 1
        else:
            tags_mapping[category] += 1

st.bar_chart(tags_mapping)
st.write("Number of Sellers in Each Product Category")

# Display the Streamlit app
st.show()
