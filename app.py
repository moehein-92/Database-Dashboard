from tkinter import font
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html

from dash import dash_table
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px

from pymongo import MongoClient
from neo4j import GraphDatabase
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions=True

colors = {
    'title': '#FFFFFF',
    'text': '#AOAABA',
    'background': '#161A1D'
}


#type mysql password here
myusername = 'root'
mypassword = ""   #dsaw2


#neo4j auth
userName = "neo4j"
password = ""

#auth = ([userName], [password])  # this way for mhaung2
auth = (userName, password)   #this way for dsaw2



#Apply Indexing to neo4j
def applying_index_neo4j():

    uri = "bolt://localhost:7687"

    driver = GraphDatabase.driver(uri, auth=auth)
    session = driver.session(database='academicworld')

    query1 = """CREATE INDEX facultyNameIndex IF NOT EXISTS FOR (f:faculty) ON (f.name)"""

    result1 = session.run(query1)

    query2 = """CREATE INDEX pubYearIndex IF NOT EXISTS FOR (p:PUBLICATION) ON (p.year)"""

    result2 = session.run(query2)
 




#facultyfavorite table creation - Using Constraint and prepared Statement
def mysql_creation_query():
    try:
        connection = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')

        cursor = connection.cursor(prepared=True)

        query = """CREATE TABLE IF NOT EXISTS favoritefaculty (
			name varchar(255) PRIMARY KEY NOT NULL,
			email varchar(255) NOT NULL UNIQUE,
			comment varchar(255)
			)
        """
    
        cursor.execute(query)
       
        connection.commit()
        print("Database created")

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



#Adding faculty To facultyfavorite - Using prepared Statement
def mysql_insertion_query(name, email, comment):

    try:
        connection = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')

        cursor = connection.cursor(prepared=True)
        # Parameterized query
        query = """INSERT INTO favoritefaculty (name, email, comment) VALUES (%s, %s, %s)"""

        cursor.execute(query, (name, email, comment))
        

        connection.commit()
        print("Data inserted successfully using Prepared statement")

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



#Deletion faculty from facultyfavorite - Using prepared Statement
def mysql_deletion_query(name):
    
    try:
        connection = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')

        cursor = connection.cursor(prepared=True)
        # Parameterized query
        query = "DELETE FROM favoritefaculty WHERE name = %s;"
        
        cursor.execute(query, (name,))
       
        connection.commit()
        print("Data Deleted successfully using Prepared statement")

    except mysql.connector.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")






#calling function Applying indexing to Neo4j
applying_index_neo4j()


#calling function - Adding favoriteFaculty Table to our DB.  
mysql_creation_query()



app.layout = html.Div([

    # Title
    html.H2(
        children="Faculty Dashboard",
        style={'textAlign':'center', 'color': colors['text']}
    ),
    #HR
    html.Hr(),

    # contains faculty info. and 1st chart
    html.Div( #div2 start
        children=[
            
            html.Div([  #start of primary div
                dbc.Row([
                    html.H6(
                                children="Enter Faculty Name To Get Started:",
                                style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                            )
                        ]),
                dbc.Row([ 
                    dbc.Col([ 

                        dcc.Input(
                            id='faculty-name',
                            type='text',
                            placeholder='Faculty Name',
                            debounce = True,
                            style={
                            'height': '40px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                            }
                        ),
                        html.Button(id='submit-button', type='submit', children='Submit'),
                        ],
                        width = { 'size': 3, 'offset' : 0}
                    ) 
                ]), 
                html.Hr(),

                dbc.Row([     #start of 1st row                
                    dbc.Col([  #start of 1-1 column
                        html.H6(
                            children="Basic Information:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        
                        html.Div(id='fac-info', style={'margin-left': '10px', 'margin-right': '10px'}),
                        
                    ], width = 3),  #end of 1-1 column

                    #Image
                    dbc.Col([  #start of 1-2 column
                        html.Div(id='fac-image', style={'margin-left': '10px', 'margin-right': '10px'}),
                    ], width = 3),  # end of 1-2 column

                    
                    dbc.Col([ #start of 1-3 column
                        html.H6(
                        children="Popular Publications:",
                        style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Div(id='pub-info', style={'margin-left': '10px', 'margin-right': '10px'}),



                    ], width=6)  #end of 1-2 column
                
                ]), # end of 1st row

                html.Hr(),

                 #Testing part - middle row added
                dbc.Row([
                    dbc.Col([
                        html.H6(
                            children="Number of Publications by Year:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Div(id='pub-info2', style={'margin-left': '10px', 'margin-right': '10px'}),
                        #testing code start
                        dcc.Store(id='store-data', data=[], storage_type='memory'), 

                           ], width = 6),
                    dbc.Col([

                            html.H6(
                            children="Filter Publications by Year:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                            ),
                            html.Br(),
                            #more testing code
                            dcc.Dropdown(id='pandas-dropdown-1'),
                            html.Br(),
                            html.Div(id='pandas-output-container-1', style={'margin-left': '10px', 'margin-right': '10px'})
                            ], width = 6)

                ]),

                html.Hr(),


                
                dbc.Row([  #2nd row
                    dbc.Col([  #2-1 column
                        # input widget 3: Keywords related to a professor
                        # relating to keywords in a publication published by this professor with a graph
                        # also include a piechart of this professor's keyword contribution percentage
                        html.H6(
                            children="Top Research Keywords:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Div(id='keyword-info', style={'margin-left': '10px', 'margin-right': '10px'}),
                    

                    ], width = 6),
                   

                    dbc.Col([ #2-2 column
                        html.H6(
                            children="Collaborated Faculty:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
            
                        html.Div(id='rel-info', style={'margin-left': '10px', 'margin-right': '10px'})
                    ], width = 6), #2-2 column end
                    
                ]), #end of 2nd row
                html.Hr(),

               

                dbc.Row([ #start of 3rd row
                    dbc.Col([ #start of 3-1 col
                        html.H6(
                            children="Add Favorite Faculty:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        # widget for adding favorite faculty
                        html.Button("Add Faculty", id='add-faculty-button',
                            style={'textAlign':'center', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Add Favorite Faculty"),
                                dbc.ModalBody(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Enter Name:"),
                                                    dbc.Input(type="text", placeholder="name", id="fav-name")
                                                ]
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Enter Email:"),
                                                    dbc.Input(type="text", placeholder="email",  id="fav-email")
                                                ],
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Enter Comment:"),
                                                    dbc.Input(type="text", placeholder="comment", id="fav-comment")
                                                ],
                                            ),
                                            html.Br(),
                                            dbc.Button("Submit", id='fav-submit', color="primary"),
                                        ],
                                    )
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("Close", color="secondary", id="close-add-faculty", className="ml-auto")
                                ),
                            ],
                            id="fav-modal",
                            is_open=False,
                            size="lg",
                            backdrop=True,
                            scrollable=True,
                            centered=True,
                            fade=True
                        ),
                        html.Div(id='written') # faculty modal output
                    ], width = 6),

                    dbc.Col([  #start of 3-2 col
                        html.H6(
                            children="Remove Favorite Faculty:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Button("Delete Faculty", id='delete-faculty-button',
                            style={'textAlign':'center', 'color': colors['text'], 'margin-left': '20px'}
                        ),

                        #Add the widget code here for removing
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Remove Favorite Faculty"),
                                dbc.ModalBody(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Enter Name:"),
                                                    dbc.Input(type="text", placeholder="name", id="fav-delete-name")
                                                ]
                                            ),
                                            html.Br(),
                                            dbc.Button("Submit", id='fav-delete-submit', color="primary"),
                                        ],
                                    )
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("Close", color="secondary", id="close-delete-faculty", className="ml-auto")
                                ),
                            ],
                            id="fav-delete-modal",
                            is_open=False,
                            size="lg",
                            backdrop=True,
                            scrollable=True,
                            centered=True,
                            fade=True
                        ),
                        html.Div(id='written2') # faculty modal output
                   

                        #end of removing
    

                    ], width = 6)  #end of 3-2 col
                ]), #end of 3rd row,

                html.Hr(),

                dbc.Row([ #start of last row
                    dbc.Col([
                        html.H6(
                            children="Show Favorite Faculty:",
                            style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Button("Show Faculty", id='show-faculty-button',
                            style={'textAlign':'center', 'color': colors['text'], 'margin-left': '20px'}
                        ),
                        html.Div(id = "favorite_table-info", style={'margin-left': '20px', 'margin-right': '20px', 'margin-top': '20px'})
                    ], width = 12)
                ]) #nd of last row
            
            ]),  # end of primary div
            html.Hr(),
        
        
        ]  # end of childrens tab
    ) #div2 end


]) # end of original div



#faculty chart
@app.callback(
    [Output(component_id='fac-info', component_property='children'),
    Output(component_id='fac-image', component_property='children')],
    [Input('submit-button', 'n_clicks')],
    [State('faculty-name', 'value')],
    prevent_initial_call = True
)
def faculty_div(clicks, input_value):
    if clicks is not None:
        cnx = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')


        cursor = cnx.cursor()
        query1 = "SELECT faculty.name AS faculty_name, position, email, phone, faculty.photo_url AS photo_url, university.name AS university FROM faculty JOIN university ON faculty.university_id=university.id WHERE faculty.name = %s"
        input_name = input_value
        
        cursor.execute(query1, (input_name,))

        df = pd.DataFrame(cursor, columns=cursor.column_names)

        name = df['faculty_name'].values[0]
        position = df['position'].values[0]
        email = df['email'].values[0]
        phone  = df['phone'].values[0]
        university  = df['university'].values[0]
        images = df['photo_url'].values[0]
        
        return (html.P(
                    [html.Br(),
                    "Name: {}".format(name),
                    html.Br(),
                    "University: {}".format(university),
                    html.Br(),
                    "Position: {}".format(position),
                    html.Br(),
                    "Email: {}".format(email),
                    html.Br(),
                    "Phone: {}".format(phone)],
                    style={'textAlign':'left', 'color': colors['text'], 'margin-left': '20px', 'font-size': '16px'}
                    )
                ), html.Img(src=images, style={'height':'80%', 'width':'80%'})

#keyword chart
@app.callback(
    Output(component_id='keyword-info', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State('faculty-name', 'value')],
    prevent_initial_call = True
)
def keyword_function(clicks, input_value):
    if clicks is not None:
        URI = "mongodb://localhost:27017"

        client = MongoClient(URI)


        # Get a reference to the "academic world" database:
        db = client["academicworld"]

        y = db.faculty.aggregate([
            {'$match': {'name': input_value}},
            {"$project":{'name': 1, "keywords": 1}},
        ])

        small_df = {}

        for i in y:
            df = pd.DataFrame(i['keywords'])    

            if 'score' in df.columns:
                df.sort_values(by=['score'], ascending=False, inplace=True)

            small_df[i['name']] = df

        
        fig = px.pie(small_df[input_value], values='score', names='name')
        #return fig
        return dcc.Graph(figure=fig)


#faculty relationship chart
@app.callback(
    Output(component_id='rel-info', component_property='children'),
    [Input('faculty-name', 'value')],
    prevent_initial_call = True
)
def find_relationship(input_value):
    if input_value == '' or input_value is None:
        return None

    uri = "bolt://localhost:7687"

    driver = GraphDatabase.driver(uri, auth=auth)
    session = driver.session(database='academicworld')

    input_name = f"'{input_value}'"

    query = """MATCH (f1:FACULTY {name: """ + input_name + """})-[r1:PUBLISH]->(p:PUBLICATION)<-[r2:PUBLISH]-(f2:FACULTY) WHERE f1 <> f2 
                RETURN f2.name, COUNT(DISTINCT p.title) as pcount
                ORDER BY COUNT(DISTINCT p.title) DESC LIMIT 10"""

    result = session.run(query)

    df = pd.DataFrame(result)

    fig = go.Figure(data=[go.Table(
    header=dict(values=['Name', '# Collaborations'],
                fill_color='paleturquoise',
                align='center'),
    cells=dict(values=[df[0], df[1]],
            fill_color='lavender',
            align='center'))
            ])

    return dcc.Graph(figure=fig)



#top 10 publications
@app.callback(
    Output(component_id='pub-info', component_property='children'),
    [Input('submit-button', 'n_clicks')],
    [State('faculty-name', 'value')]
)
def faculty_publication_top10(clicks, input_value):
    if clicks is not None:
        cnx = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')

        cursor = cnx.cursor()

        query = """SELECT p.title, p.year, p.num_citations AS citation_counts from faculty f
                    JOIN faculty_publication fp ON f.id = fp.faculty_id
                    JOIN publication p ON fp.publication_id = p.id
                    WHERE f.name = %s
                    ORDER BY num_citations DESC
                    LIMIT 10;"""

        input_name = input_value
        cursor.execute(query, (input_name,))

        df = pd.DataFrame(cursor, columns=cursor.column_names)

        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], style_table={'height': '300px',' overflowY': 'scroll', 'overflowX': 'scroll'},style_cell={
        'textAlign': 'left' }, style_header={ 'border': '1px solid pink', 'textAlign': 'left'}, style_data={'whiteSpace': 'normal','height': 'auto'})
        



#publication yearly chart and storing data
@app.callback(
    [Output(component_id='pub-info2', component_property='children'),
     Output('store-data', 'data')],
    [Input('submit-button', 'n_clicks')],
    [State('faculty-name', 'value')]
)
def publication_yearly_chart(clicks, input_value):
    if clicks is not None:
        cnx = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')
        cursor = cnx.cursor()

        query = """SELECT year, COUNT(year) AS pub_count FROM faculty f
                JOIN faculty_publication fp ON f.id = fp.faculty_id
                JOIN publication p ON fp.publication_id = p.id
                WHERE f.name = %s
                GROUP BY year;"""

        input_name = input_value
        cursor.execute(query, (input_name,))

        df = pd.DataFrame(cursor, columns=cursor.column_names)

        fig = px.line(df, x='year', y='pub_count', markers=True)

        #storing data
        df_dict = df.to_dict('records')
        df_dict.append({'name': input_name})


        return dcc.Graph(figure=fig), df_dict
    return None, []



#storing data inside of dropdown
@app.callback(
    Output('pandas-dropdown-1', 'options'),
    [Input('store-data', 'data')],
    prevent_initial_call = True
)
def populate_dropdown(data):
    #if type(data) != None:
    if data != []:
        #print(type(data))

        data_parse = []
        if data != None:
            data_parse = data[:-1]

            dff = pd.DataFrame(data_parse)

            df_year = np.sort(dff['year'])

            df_return = [{'label': x, 'value': x} for x in df_year]
            return df_return
        else:
            return []
    return []




# show publication by year for chosen faculty 
@app.callback(
    Output('pandas-output-container-1', 'children'),
    [Input('pandas-dropdown-1', 'value'),
    Input('store-data', 'data')],
    prevent_initial_callback = True
)
def publication_info_by_year(value, data):

    if value is not None:
    
        input_year = str(value)

        input_value = ''
        if data != None:
            input_value = data[-1]['name']


        uri = "bolt://localhost:7687"

        driver = GraphDatabase.driver(uri, auth=auth)
        session = driver.session(database='academicworld')

        input_name = f"'{input_value}'"


        query = """MATCH (f1:FACULTY {name: """ + input_name + """})-[pub: PUBLISH]->(p:PUBLICATION {year: """ + input_year +"""})
                   USING INDEX f1:FACULTY(name) 
                   USING INDEX p:PUBLICATION(year)
                   RETURN p.title AS title, p.year AS year, p.numCitations AS citation_counts"""

        result = session.run(query)

        df = pd.DataFrame(result, columns=result.keys())
    else:
        return []

    
    return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], style_table={'height': '300px',' overflowY':'scroll','overflowX': 'scroll'},style_cell={
        'textAlign': 'left' }, style_header={ 'border': '1px solid pink', 'textAlign': 'left'}, style_data={'whiteSpace': 'normal','height': 'auto',})






## Add Favorite Faculty Widget

# prompt modal
@app.callback(
    Output("fav-modal", "is_open"),
    [
        Input("add-faculty-button", "n_clicks"),
        Input("close-add-faculty", "n_clicks")
    ],
    [State("fav-modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# write to DB
@app.callback(
    Output("written", "children"),
    [
        Input("fav-submit", "n_clicks")
    ],
    [
        State("fav-name", "value"),
        State("fav-email", "value"),
        State("fav-comment", "value")
    ]
)
def write_to_db(n_clicks, name, email, comment):

    if n_clicks is not None:
        print(name)
        print(email)
        print(comment)

        mysql_insertion_query(name, email, comment)              
        
        return 'Added successfully'




# prompt modal - DELETION
@app.callback(
    Output("fav-delete-modal", "is_open"),
    [
        Input("delete-faculty-button", "n_clicks"),
        Input("close-delete-faculty", "n_clicks")
    ],
    [State("fav-delete-modal", "is_open")]
)
def toggle_modal_delete(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open





# write to DB
@app.callback(
    Output("written2", "children"),
    [
        Input("fav-delete-submit", "n_clicks")
    ],
    [
        State("fav-delete-name", "value")
    ]
)
def write_to_db_delete(n_clicks, name):

    if n_clicks is not None:
       
        print(name)
        mysql_deletion_query(name)  
        
        return 'Deleted successfully'




#show favorite Faculty
@app.callback(
    Output(component_id='favorite_table-info', component_property='children'),
    [Input("close-add-faculty", "n_clicks"),
     Input("close-delete-faculty", "n_clicks"),
     Input("show-faculty-button", "n_clicks")],
    prevent_initial_callback = False
)
def show_favorite_faculty(clicks1, clicks2,clicks3):
    
    if (clicks1 or clicks2 or clicks3) is not None:
        cnx = mysql.connector.connect(user=myusername, password=mypassword,
                                host='127.0.0.1',
                                database='academicworld')

        cursor = cnx.cursor()

        query = """SELECT name, email, comment FROM favoritefaculty"""

        cursor.execute(query)

        df = pd.DataFrame(cursor, columns=cursor.column_names)

        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], style_table={'height': '300px',' overflowY': 'scroll', 'overflowX': 'scroll'},style_cell={
        'textAlign': 'left' }, style_header={ 'border': '1px solid pink', 'textAlign': 'left'}, style_data={'whiteSpace': 'normal','height': 'auto'})


if __name__ == '__main__':
    app.run_server(debug=True)
