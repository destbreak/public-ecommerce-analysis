import streamlit as st
from streamlit_folium import folium_static

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

products = pd.read_csv('dashboard/products.csv')
payments = pd.read_csv('dashboard/payments.csv')
geo_customers = pd.read_csv('dashboard/geo_customers_top_10.csv')
geo_sellers = pd.read_csv('dashboard/geo_sellers_top_10.csv')
population_customers = pd.read_csv('dashboard/population_customers.csv')
population_sellers = pd.read_csv('dashboard/population_sellers.csv')
brazil_geo = gpd.read_file('dashboard/brazil_geo.json')

st.title('E-Commerce Public Analysis')
st.header('Visualization & Explanatory Analysis')

tab1, tab2, tab3, tab4 = st.tabs(['Produk', 'Pembayaran', 'Pembeli', 'Penjual'])
with tab1: 
    with st.container(): 
        # Jenis Produk
        product_category = products.product_category_name_english.value_counts()
        colors = ['#329932','#999999','#999999','#999999','#999999','#999999','#999999']

        st.subheader('10 Kategori Produk yang banyak dijual')
        fig_product_category = plt.figure(figsize=(12.8, 9.6))
        sns.barplot(x=product_category[:10], y=product_category.index[:10], palette=colors)
        plt.xlabel('Jenis Produk')
        plt.ylabel('Jumlah')

        st.pyplot(fig_product_category)
        with st.expander('Hasil Analisa'): 
            st.write(
                """
                1. Jenis produk yang dijual di E-Commerce ada 7 macam, yaitu: Cool Stuff, Pet Shop, Consoles Games, Market Place, Audio, DVD Blu-ray, dan La Cuisine.
                2. Produk yang paling banyak dijual adalah barang-barang unik (cool stuff) yaitu sebanyak 789 barang.
                3. Produk yang paling sedikit dijual adalah makanan (la cuisine) yaitu sebanyak 10 barang.
                """
            )

with tab2: 
    with st.container(): 
        # Metode Pembayaran
        payment_type = payments.payment_type.value_counts()
        colors = ['#329932','#999999','#999999','#999999']

        st.subheader('Metode Pembayaran yang sering dipakai')
        fig_payment_type = plt.figure(figsize=(12.8, 9.6))
        sns.barplot(x=payment_type.index[:4], y=payment_type[:4], palette=colors)
        plt.xlabel('Metode Pembayaran')
        plt.ylabel('Jumlah')

        st.pyplot(fig_payment_type)
        with st.expander('Hasil Analisa'): 
            st.write(
                """
                1. Metode pembayaran yang digunakan dalam transaksi di E-Commerce ada 4 macam, yaitu: Credit Card, Boleto, Voucher, dan Debit Card.
                2. Metode yang paling sering digunakan adalah kartu kredit (credit card) yaitu sebanyak 76795 transaksi.
                3. Metode yang paling sedikit digunakan adalah kartu debit (debit card) yaitu sebanyak 1529 transaksi.
                """
            )

        # Skema Cicilan
        payment_installments = payments.payment_installments.value_counts().sort_index()
        colors = ['#329932','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999']

        st.subheader('Skema Cicilan yang sering digunakan\n(kurun waktu 1-12 bulan)')
        fig_payment_installments = plt.figure(figsize=(12.8, 9.6))
        sns.barplot(x=payment_installments.index[1:13], y=payment_installments[1:13], palette=colors)
        plt.xlabel('Skema Cicilan (x bulan)')
        plt.ylabel('Jumlah')

        st.pyplot(fig_payment_installments)
        with st.expander('Hasil Analisa'): 
            st.write(
                """
                0. Aslinya, terdapat 2 skema pembayaran yang digunakan dalam transaksi di E-Commerce, yaitu: Bayar Tuntas (0x) dan Cicilan (1-24x bulan).
                1. Skema cicilan yang sering dipilih ketika transaksi di E-Commerce adalah 1 bulan (1x) yaitu sebanyak 52546 transaksi.
                2. Skema cicilan yang sedikit dipilih ketika transaksi di E-Commerce adalah 11 bulan (11x) yaitu sebanyak 23 transaksi.
                """
            )

with tab3: 
    with st.container(): 
        # 10 Kota Pembeli
        city_customers = geo_customers.customer_city.value_counts()
        colors = ['#329932','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999']

        st.subheader('10 Kota dengan asal Pembeli terbanyak')
        fig_city_customers = plt.figure(figsize=(12.8, 9.6))
        sns.barplot(x=city_customers, y=city_customers.index, palette=colors)
        plt.xlabel('Jumlah')
        plt.ylabel('Kota')
        
        st.pyplot(fig_city_customers)

        # Inisiasi Map Pembeli
        customer_map = folium.Map([-14.2400732, -53.1805017], zoom_start=4)
        folium.TileLayer('cartodbdark_matter').add_to(customer_map)

        # Persebaran 10 Kota Pembeli
        customer_cluster = MarkerCluster().add_to(customer_map)

        for i in range(len(geo_customers.index)):
            lat = geo_customers['rep_lat'][i]
            lng = geo_customers['rep_lng'][i]
            city = geo_customers['customer_city'][i]
            state = geo_customers['customer_state'][i]

            folium.Marker([lat, lng], tooltip=city + ', ' + state).add_to(customer_cluster)

        # Persebaran Pembeli tiap Provinsi
        folium.Choropleth(
            geo_data = brazil_geo,
            name = 'choropleth',
            data = population_customers,
            columns = ['state', 'population'],
            key_on = 'feature.properties.id',
            fill_color = 'YlGn',
            fill_opacity = 0.5,
            line_opacity = 0.2
        ).add_to(customer_map)

        folium_static(customer_map)
        with st.expander('Hasil Analisa'): 
            st.write(
                """
                1. 10 kota pembeli banyak berasal yaitu dari Sao Paulo, Rio de Janeiro, Belo Horizonte, Brasilia, Curitiba, Campinas, Porto Alegre, Salvador, Guarulhos, dan Sao Bernardo do Campo.
                2. Perbandingan antara jumlah pembeli dan penjual di kota Sao Paulo adalah 16231:1.
                3. Dari 10 kota teratas, pembeli dari Sao Paulo sangat mendominasi karena jumlah pembeli yang mencapai puluhan ribu, sangat berbeda dengan kota lain yang hanya ribuan pembeli saja.
                4. Persebaran pembeli didominasi oleh provinsi SP (Sao Paulo), RJ (Rio de Janeiro), dan MG (Minas Gerais).
                5. Persebaran pembeli merata di semua wilayah Brazil. 
                """
            )

with tab4: 
    with st.container(): 
        # 10 Kota Penjual
        city_sellers = geo_sellers.seller_city.value_counts()
        colors = ['#329932','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999','#999999']

        st.subheader('10 Kota dengan asal Penjual terbanyak')
        fig_city_sellers = plt.figure(figsize=(12.8, 9.6))
        sns.barplot(x=city_sellers, y=city_sellers.index, palette=colors)
        plt.xlabel('Jumlah')
        plt.ylabel('Kota')

        st.pyplot(fig_city_sellers)

        # Inisiasi Map Penjual
        seller_map = folium.Map([-14.2400732, -53.1805017], zoom_start=4)
        folium.TileLayer('cartodbdark_matter').add_to(seller_map)

        # Persebaran 10 Kota Penjual
        seller_cluster = MarkerCluster().add_to(seller_map)

        for i in range(len(geo_sellers.index)):
            lat = geo_sellers['rep_lat'][i]
            lng = geo_sellers['rep_lng'][i]
            city = geo_sellers['seller_city'][i]
            state = geo_sellers['seller_state'][i]

            folium.Marker([lat, lng], tooltip=city + ', ' + state).add_to(seller_cluster)

        # Persebaran Penjual tiap Provinsi
        folium.Choropleth(
            geo_data = brazil_geo,
            name = 'choropleth',
            data = population_sellers,
            columns = ['state', 'population'],
            key_on = 'feature.properties.id',
            fill_color = 'YlGn',
            fill_opacity = 0.5,
            line_opacity = 0.2
        ).add_to(seller_map)

        folium_static(seller_map)
        with st.expander('Hasil Analisa'): 
            st.write(
                """
                1. 10 kota penjual banyak berasal yaitu dari Sao Paulo, Curitiba, Rio de Janeiro, Belo Horizonte, Ribeirao Preto, Guarulhos, Ibitinga, Santo Andre, Campinas, dan Maringa.
                2. Perbandingan antara jumlah pembeli dan penjual di kota Rio de Janeiro adalah 71:1.
                3. Penjual dari Sao Paulo tidak terlalu mendominasi seperti pembeli dari Sao Paulo karena jumlah penjual hanya ratusan saja sama seperti penjual di kota lainnya.
                4. Persebaran penjual didominasi oleh provinsi SP (Sao Paulo) dan PR (Parana).
                5. Persebaran penjual tidak merata. Hal ini dibuktikan dengan adanya wilayah yang tidak terdapat penjual sama sekali, yaitu di provinsi Tocantins dan Alagoas.
                """
            )