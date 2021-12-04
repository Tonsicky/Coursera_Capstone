# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# For slider plot
success_or_not = []

for i in spacex_df['Mission Outcome']:
    if i == "Success":
        success_or_not.append('Success')
    else:
        success_or_not.append('Not Success')

spacex_dummy_df = pd.DataFrame({'Payload': spacex_df['Payload Mass (kg)'],
                                'Outcome': success_or_not,
                                'Site': spacex_df['Launch Site']})

spacex_dummy_df = spacex_dummy_df.sort_values(by=['Payload'])

spacex_dummy_df = spacex_dummy_df.reset_index(drop=True)


#pie initialization
#in_att = ['Success']
#in_val = [5]
#figpie0 = px.pie(in_att,values=in_val,names=in_att)
#figpie0.show()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 ],
                                             value='ALL',
                                             placeholder="Select a Launch Site Here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.P("Success Rate per Location Site"),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                dcc.Slider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                marks=[{'0':'Minimum Payload','10000':'Maximum Payload'}]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(
        Output("success-pie-chart", 'figure'), [Input("site-dropdown",'value')])

#function for the pie chart 
def SNS(value):
        LS_x = []
        for k in range(spacex_df['Launch Site'].size):
            mo = spacex_df['Launch Site'][k]
            if mo != value:
                continue
            else:
                LS_x.append(spacex_df['Mission Outcome'][k])

        LSx_comp = []
        LSx_value = []

        for l in LS_x:
            if l not in LSx_comp:
                LSx_comp.append(l)

        for ll in LSx_comp:
            LSx_value.append(LS_x.count(ll))
        
        figpie = px.pie(LSx_comp, values = LSx_value, names = LSx_comp)
        
        return figpie

@app.callback(
        Output("success-payload-scatter-chart", 'figure'), [Input("payload-slider",'value')])

def slider_value(slidervalue):
    for i in range(len(spacex_dummy_df['Payload'])):
        pay_val = spacex_dummy_df['Payload'][i]
        if pay_val < slidervalue and i != (len(spacex_dummy_df['Payload'])-1):
            continue
        else:
            p_value = pay_val
            p_index = i
            break
    
    scatter_data = pd.DataFrame({'Payload_2': spacex_dummy_df['Payload'][0:p_index],
                                'Outcome_2': spacex_dummy_df['Outcome'][0:p_index],
                                'Site_2': spacex_dummy_df['Site'][0:p_index]})
    
    figscatter = px.scatter(data_frame = scatter_data,
                            x = 'Payload_2',
                            y = 'Outcome_2',
                           color='Site_2')
    return figscatter 


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
