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

range_slider = [int(min_payload), int(max_payload)]

# Create a dash application
app = dash.Dash(__name__)

#


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value':'OPT1'},
                                        {'label': 'CCAFS LC-40', 'value':'OPT2'},
                                        {'label': 'VAFB SLC-4E', 'value':'OPT3'},
                                        {'label': 'KSC LC-39A', 'value':'OPT4'},
                                        {'label': 'CCAFS SLC-40', 'value':'OPT5'}
                                        ],
                                    value = 'OPT1',
                                    style={'width':'80%', 'padding':'3px','font-size':'14px','text-align-last':'center'},
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider', 
                                    min=0, 
                                    max=10000, 
                                    step=1000, 
                                    value=[0,9600],
                                    marks = {
                                        0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

def filter_dfs():
    all_sites = spacex_df
    opt2_df = all_sites[all_sites['Launch Site'] == "CCAFS LC-40"]
    opt3_df = all_sites[all_sites['Launch Site'] == "VAFB SLC-4E"]
    opt4_df = all_sites[all_sites['Launch Site'] == "KSC LC-39A"]
    opt5_df = all_sites[all_sites['Launch Site'] == "CCAFS SLC-40"]

    return all_sites, opt2_df, opt3_df, opt4_df, opt5_df


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)

def build_pie_chart(launch_site):
    
    all_sites, opt2_df, opt3_df, opt4_df, opt5_df = filter_dfs()

    if launch_site == 'OPT1':
        fig = px.pie(all_sites, values='class', names='Launch Site', title="Total Success Launches By Site")
        return fig

    elif launch_site == 'OPT2':
        fig = px.pie(opt2_df, names='class', title="Total Success Launches for site CCAFS LC-40")
        return fig
    
    elif launch_site == 'OPT3':
        fig = px.pie(opt3_df, names='class', title='Total Success Launches for site VAFB SLC-4E')
        return fig
    
    elif launch_site == 'OPT4':
        fig = px.pie(opt4_df, names='class', title="Total Success Launches for site KSC LC-39A")
        return fig
    
    elif launch_site == 'OPT5':
        fig = px.pie(opt5_df, names='class', title="Total Success Launches for site CCAFS SLC-40")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")
)

def build_scatter(launch_site2, range_slide):
    all_sites, opt2_df, opt3_df, opt4_df, opt5_df = filter_dfs()
    if launch_site2 == 'OPT1':
        all_sites = all_sites[(all_sites['Payload Mass (kg)'] >= range_slide[0]) & (all_sites['Payload Mass (kg)'] <= range_slide[1])]
        fig = px.scatter(all_sites, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                title=f'Correlation between Payload and Success for all Sites (Range: {range_slide[0]} - {range_slide[1]} kg)')
        return fig

    if launch_site2 == 'OPT2':
        opt2_df = opt2_df[(opt2_df['Payload Mass (kg)'] >= range_slide[0]) & (opt2_df['Payload Mass (kg)'] <= range_slide[1])]
        fig = px.scatter(opt2_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                title=f'Correlation between Payload and Success for site CCAFS LC-40 (Range: {range_slide[0]} - {range_slide[1]} kg)')
        return fig

    if launch_site2 == 'OPT3':
        opt3_df = opt3_df[(opt3_df['Payload Mass (kg)'] >= range_slide[0]) & (opt3_df['Payload Mass (kg)'] <= range_slide[1])]
        fig = px.scatter(opt3_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                title=f'Correlation between Payload and Success for site VAFB SLC-4E (Range: {range_slide[0]} - {range_slide[1]} kg)')
        return fig

    if launch_site2 == 'OPT4':
        opt4_df = opt4_df[(opt4_df['Payload Mass (kg)'] >= range_slide[0]) & (opt4_df['Payload Mass (kg)'] <= range_slide[1])]
        fig = px.scatter(opt4_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                title=f'Correlation between Payload and Success for site KSC LC-39A (Range: {range_slide[0]} - {range_slide[1]} kg)')
        return fig

    if launch_site2 == 'OPT5':
        opt5_df = opt5_df[(opt5_df['Payload Mass (kg)'] >= range_slide[0]) & (opt5_df['Payload Mass (kg)'] <= range_slide[1])]
        fig = px.scatter(opt5_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                title=f'Correlation between Payload and Success for site CCAFS SLC-40 (Range: {range_slide[0]} - {range_slide[1]} kg)')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
