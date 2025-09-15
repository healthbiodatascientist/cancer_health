#!/usr/bin/env python
# coding: utf-8

# Import packages/libraries

# In[1]:


import pandas as pd
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc


# Import data and create tables

# In[2]:


def no_geometry():
    df_cancer_prev_mapped = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/cancer_health/refs/heads/main/cancer_prev_mapped.csv')
    df_cancer_prev_mapped = df_cancer_prev_mapped.set_index('HBCode')
    df_hb_table = df_cancer_prev_mapped.drop('geometry', axis=1)
    return df_hb_table

df_hb_table = no_geometry()
df_numeric_columns = df_hb_table.select_dtypes('number')


# Create app layout

# In[3]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
app.layout = dbc.Container([
    html.H1("Cancer Related Prevalence in Scotland's General Practices by Regional Health Board 2024/25", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays open source cancer data from Public Health Scotland (PHS) for each of the Scottish Health Board Regions. Click on or hover over your Health Board for an insight into the factors affecting cancer detection and treatment in your area:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
    dbc.Row([dbc.Col(html.Iframe(id='my_output', height=600, width=1000, srcDoc=open('cancerprevmap.html', 'r').read()))], style={'text-align':'center'}),
    html.Figcaption("Figure 1: Map of the latest cancer open data for the Scottish Health Board Regions", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    html.H4("Potential Data Relationships", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Prevalence is how common a disease is in a population. If in a GP practice with 10,000 patients 1,000 meet the conditions for the cancer indicator, then this practice has a cancer prevalence of 10 per 100. In other words, prevalence rates represent how many people out of every 100 are recorded as having a particular disease.", className='mb-2'),
    html.Summary("SIMD quintiles divide Scotland's data zones into five equal groups, with Quintile 1 representing the 20% most deprived areas and Quintile 5 representing the 20% least deprived areas. This allows for the identification and targeting of resources to the areas of greatest need based on overall deprivation or specific factors like income, education, or health", className='mb-2'),
    html.Summary("Breast screening in Scotland uses mammograms (low dose X-rays) to detect breast cancer early in women aged 50-70, with appointments offered every three years and can be booked by women over 70 by contacting their local unit. Early detection significantly improves survival rates", className='mb-2'),
    html.Summary("The Scottish Bowel Screening Programme offers everyone aged 50 to 74 a free, at-home test kit every two years to check for signs of bowel cancer, specifically hidden blood in their poo. The faecal immunochemical test (FIT) can detect bowel cancer early, even before symptoms appear, when treatment is more effective and successful", className='mb-2'),
    html.Summary("In Scotland, cervical screening is a routine HPV (Human Papillomavirus) test for women and people with a cervix aged 25 to 64, offered every 5 years, that checks for virus and cell changes to prevent cancer. The quick, 5-minute test involves taking a sample of cells from the cervix and is the best way to detect and treat potential cervical cancer before symptoms appear", className='mb-2'),
    html.Summary("The Scottish 31-day standard for cancer care requires that 95% of eligible patients start their first cancer treatment within 31 days of the decision to treat, regardless of how they were referred. This standard applies to all cancer types and ensures that diagnosis to treatment timelines are equitable for everyone", className='mb-2'),
    html.Summary("In Scotland, Systemic Anti-Cancer Therapy (SACT) refers to drug-based treatments that travel throughout the body to fight cancer cells, unlike localized treatments like surgery or radiotherapy. SACT includes various drug types, such as chemotherapy, immunotherapy, targeted therapy, and hormone therapy", className='mb-2'),
    html.Summary("Deprivation is linked to worse cancer outcomes, with people in the most deprived areas facing higher cancer incidence, mortality, and more advanced diagnoses, partly due to higher rates of preventable risk factors like smoking and lower participation in cancer screening programs", className='mb-2'),
    html.Summary("Scotland's population is ageing. With cancer risk increasing as we age, a larger older population naturally means more cancer cases overall", className='mb-2'),
    html.Figcaption("Table 1: Latest open cancer data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark orange", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_hb_table.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_hb_table.columns],
    style_cell={'textAlign': 'center'},
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_data_conditional=
    [
            {
                'if': {
                    'filter_query': '{{{}}} > {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#ff8000',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.1).items()
        ] +       
        [
            {
                'if': {
                    'filter_query': '{{{}}} <= {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#ffbf00',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.5).items()
        ]
    ))
    ]),
    html.H4("Open Data References", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Public Health Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/general-practice-disease-prevalence-data-visualisation/general-practice-disease-prevalence-visualisation-8-july-2025/")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/34174/diseaseprevalence_methodology_and_metadata_2025-for-publication.pdf")),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/systemic-anti-cancer-therapy-sact-activity/systemic-anti-cancer-therapy-activity-11-september-2025/dashboard/")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/34170/kpi_1_coverage_uptake_2324.xlsx")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/32270/2025_04_01_breast_cancer_qpi_summary_table.xlsx")),
    html.Li(html.Cite("https://publichealthscotland.scot/media/31821/2025-03-04-bowel-screening-kpi-report.xlsx")),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/11c61a02-205b-43f6-9297-243679103617/resource/58527343-a930-4058-bf9e-3c6e5cb04010/download/cwt_31_day_standard.csv")),
    html.Summary("National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.nrscotland.gov.uk/media/c0qjtpgc/age-standard-death-rates-2023-tables.xlsx")),
    html.Summary("Scotland's Census 2022 - National Records of Scotland", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.scotlandscensus.gov.uk/webapi/jsf/tableView/tableView.xhtml")),
    html.Summary("Scottish Surveys Core Questions 2023 - Scottish Government", style={'list-style': 'none'}),
    html.Li(html.Cite("https://www.gov.scot/publications/scottish-surveys-core-questions-2023/documents/")),
    ])


# Run app

# In[4]:


if __name__ == "__main__":
    app.run()

