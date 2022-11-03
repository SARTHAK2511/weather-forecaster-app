# Importing necessary libraries
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime,date
import pyowm
from pyowm import OWM
from matplotlib import rcParams
from pytz import timezone
from pyowm.utils import timestamps
st.set_option('deprecation.showPyplotGlobalUse', False)
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/jpeg;base64,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");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url() 

# initiating pyowm with the api key .
owm=pyowm.OWM('9bc2fd7057d82be5eec22e5c31c5c7b2')


st.title("Weather Forecast ☁️🌡️")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type :")
st.write("Dont use the same city consecutively , if you want to do so keep a minimum interval of 10 min :")
place=st.text_input("NAME OF THE CITY :", "")
unit=st.selectbox("Select Temperature Unit",("Celsius","Fahrenheit"))

g_type=st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))
b=st.button("SUBMIT")



def plot_line(days,min_t,max_t):        
        days=dates.date2num(days)
        rcParams['figure.figsize']=6,4
        plt.plot(days,max_t,color='blue',linestyle='dashdot',linewidth = 1,marker='o',markerfacecolor='black',markersize=7) 
        plt.plot(days,min_t,color='red',linestyle='dashdot',linewidth = 1,marker='o',markerfacecolor='green',markersize=7)     
        plt.ylim(min(min_t)-4,max(max_t)+4)
        plt.xticks(days)
        x_y_axis=plt.gca()
        xaxis_format=dates.DateFormatter('%m/%d')
        
        
        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.grid(True,color='brown')
        plt.legend(["Maximum Temperaure","Minimum Temperature"],loc=1) 
        plt.xlabel('Dates(mm/dd)') 
        plt.ylabel('Temperature') 
        plt.title('5-Days Forecast')   
        
        for i in range(5):
            plt.text(days[i], min_t[i]-1.5,min_t[i],
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='black')
        for i in range(5):
            plt.text(days[i], max_t[i]+0.5,max_t[i],
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='black')
        #plt.show()
        #plt.savefig('figure_line.png')
        st.pyplot()
        plt.clf()
        

def plot_bars(days,min_t,max_t):  
        #print(days)      
        rcParams['figure.figsize']=6,4
        days=dates.date2num(days)
        #print(days) 
        min_temp_bar=plt.bar(days-0.2, min_t, width=0.4, color='r')
        max_temp_bar=plt.bar(days+0.2, max_t, width=0.4, color='b')        
        plt.xticks(days)
        x_y_axis=plt.gca()
        xaxis_format=dates.DateFormatter('%m/%d')
        
        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.xlabel('Dates(mm/dd)') 
        plt.ylabel('Temperature') 
        plt.title('5-Day Weather Forecast')
        
        for bar_chart in [min_temp_bar,max_temp_bar]:
            for index,bar in enumerate(bar_chart):
                height=bar.get_height()
                xpos=bar.get_x()+bar.get_width()/2.0
                ypos=height 
                label_text=str(int(height))
                plt.text(xpos, ypos,label_text,
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='black')
        
        
        st.pyplot()
        plt.clf()
        
        

def find_min_max(place,unit,g_type):
    mgr=owm.weather_manager()
    days=[]
    dates_2=[]
    min_t=[]
    max_t=[]
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast = forecaster.forecast
    if unit=='Celsius':
        unit_c='celsius'
    else:
        unit_c='fahrenheit'
    
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
        if date not in dates_2:
            dates_2.append(date)
            min_t.append(None)
            max_t.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1]=temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1]=temperature
    if g_type=="Line Graph":
        plot_line(days,min_t,max_t)
    elif g_type=="Bar Graph":
        plot_bars(days,min_t,max_t)
    i=0
    st.write(f"#    Date :  Max - Min  ({unit})")
    for obj in days:
        d=(obj.strftime("%d/%m"))
        st.write(f"### \v {d} :\t  ({max_t[i]} - {min_t[i]})")
        i+=1
      
    
        
if b:
    if not place=="":    
        find_min_max(place,unit,g_type)
    
    
    
st.title("TOMORROW'S WEATHER FORECAST")
place1=st.text_input("NAME OF THE CITY FOR TOMORROW'S FORECAST:", "")
unit1=st.selectbox("Select Temperature Unit for tomorrow's forecast",("celsius","fahrenheit"))

hr1=st.slider("Hour :",min_value=0,max_value=23,step=1)
m1=st.slider("Minute :",min_value=0,max_value=59,step=5)
st.write(" ⚠️ Refresh page if results not obtained")
c=st.button("SUBMIT INFO ")    
    




def weather_detail(place,unit,hr,m):
    mgr=owm.weather_manager()
    forecaster = mgr.forecast_at_place(place, '3h')
    time=timestamps.tomorrow(hr,m)
    weather=forecaster.get_weather_at(time)
    
    t=weather.temperature(unit)['temp']
    st.write(f"## Temperature at {place} for the selected time in {unit} is {t}")
 
    st.title(f"Expected Temperature Changes/Alerts at {hr}:{m}")
    if forecaster.will_be_foggy_at(time):
        st.write("### FOG ALERT!!")
    if forecaster.will_be_rainy_at(time):
        st.write("### RAIN ALERT!!")
    if forecaster.will_be_stormy_at(time):
        st.write("### STORM ALERT!!")
    if forecaster.will_be_snowy_at(time):
        st.write("### SNOW ALERT!!")
    if forecaster.will_be_tornado_at(time):
        st.write("### TORNADO ALERT!!")
    if forecaster.will_be_hurricane_at(time):
        st.write("### HURRICANE ALERT")
    if forecaster.will_be_clear_at(time):
        st.write("### CLEAR WEATHER PREDICTED!!")
    if forecaster.will_be_cloudy_at(time):
        st.write("### CLOUDY SKIES")


if c:
    if not place:
        weather_detail(place1,unit1,hr1,m1)

st.write('## Created  by - Sarthak Bhatore ✨')
st.info('My passion lies in drawing insights from data and putting them to use.')
column1, column2 = st.columns(2)
Linkedin='[My Linkedin](https://www.linkedin.com/in/sarthak-bhatore-004aaa1ba/)'
Github='[My Github](https://github.com/SARTHAK2511)'
column1.markdown(Linkedin,unsafe_allow_html=True)
column2.markdown(Github,unsafe_allow_html=True)
