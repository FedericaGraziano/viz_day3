import pandas as pd

df_ch = pd.read_csv('./data/raw/renewable_power_plants_CH.csv')

cantons_dict = {
'TG':'Thurgau', 
'GR':'Graubünden', 
'LU':'Luzern', 
'BE':'Bern', 
'VS':'Valais',                
'BL':'Basel-Landschaft', 
'SO':'Solothurn', 
'VD':'Vaud', 
'SH':'Schaffhausen', 
'ZH':'Zürich', 
'AG':'Aargau', 
'UR':'Uri', 
'NE':'Neuchâtel', 
'TI':'Ticino', 
'SG':'St. Gallen', 
'GE':'Genève',
'GL':'Glarus', 
'JU':'Jura', 
'ZG':'Zug', 
'OW':'Obwalden', 
'FR':'Fribourg', 
'SZ':'Schwyz', 
'AR':'Appenzell Ausserrhoden', 
'AI':'Appenzell Innerrhoden', 
'NW':'Nidwalden', 
'BS':'Basel-Stadt'}

df_ch['canton_name']=''
for keys, value in cantons_dict.items():
    for i in range(len(df_ch)):
      if df_ch['canton'].iloc[i]==keys:
       df_ch['canton_name'].iloc[i]=value 

df_ch.to_csv('canton.csv')

