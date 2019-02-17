import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from utils.pre_data import process_whole_class
from grade_calculation import calc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
markdown_text = '''
# Intelligent teaching aid
## Teacher Dashboard
### Presence Dashboard
---
'''
markdown_text2 = '''
---
## Grade Dashboard
'''
df = pd.read_excel('presence/id.xlsx')
available_indicators = df.ID

av_indi = ['Midterm Grade','Final Exam Grade','Total Score']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        dcc.Markdown(children = markdown_text),
        html.Div([
            html.Label('Select the function'),
            dcc.RadioItems(
                id = 'function',
                options = [{'label':i,'value':i} for i in ['whole-class','individual']],
                value = 'whole-class',
                labelStyle = {'display':'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select the ID you want to see below'),
            dcc.Dropdown(
                id = 'student_id',
                options = [{'label':i,'value':i} for i in available_indicators],
                value = 181230039
            )],
        style = {'width': '48%', 'float':'right','display': 'inline-block'}),
        dcc.Graph(id='indicator-graphic'),
        dcc.Markdown(children = markdown_text2),
        html.Div([
            html.Label('Select the function'),
            dcc.Dropdown(
                id = 'func',
                options = [{'label':i,'value':i} for i in av_indi],
                value = 'Total Score'
            )]),
        dcc.Graph(id='grade_graph')
    ]
)

def get_data(student_id,function):
    csv = 'presence/student_data/{}.csv'.format(student_id) if function == 'individual' else 'presence/whole_class/whole-class.csv'
    tempdf = pd.read_csv(csv)
    tempdf.index = tempdf.iloc[:,0]
    x_data = ['.'.join([str(i)[:4],str(i)[4:6],str(i)[6:8]]) for i in tempdf.index]
    y_data = tempdf.iloc[:,-1]
    return x_data,y_data

@app.callback(
    dash.dependencies.Output('indicator-graphic','figure'),
    [dash.dependencies.Input('student_id','value'),
    dash.dependencies.Input('function','value')]
)
def update_figure(student_id,function):
    try:
        x_data,y_data = get_data(student_id,function)
    except FileNotFoundError:
        process_whole_class()
        x_data, y_data = get_data(student_id,function)
    return {
                'data':[go.Bar(
                    x = x_data,
                    y = y_data)],
                'layout':go.Layout(
                    xaxis = {'title':'Date'},
                    yaxis = {'title':'Presence Frequency'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                    hovermode = 'closest'
                )
            }

def get_grade(func):
    with open('config.ini') as cfg:
        lines = cfg.readlines()
        freq = int(lines[1].split('=')[1])
    grade = pd.read_excel('grade.xlsx')
    x = [str(i) for i in grade.iloc[:,0]]
    if func == 'Midterm Grade':
        return (x,list(grade.iloc[:,1]))
    elif func == 'Final Exam Grade':
        return (x,list(grade.iloc[:,2]))
    else:
        return (x,list(grade.iloc[:,-1]))

@app.callback(
    dash.dependencies.Output('grade_graph','figure'),
    [dash.dependencies.Input('func','value')]
)
def update_grade(func):
    calc()
    stu_id,grade = get_grade(func)
    return {
                'data':[go.Bar(
                    x = stu_id,
                    y = grade)],
                'layout':go.Layout(
                    xaxis = {'title':'ID'},
                    yaxis = {'title':'Grade'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                    hovermode = 'closest'
                )
            }

if __name__ == '__main__':
    app.run_server(debug=True)