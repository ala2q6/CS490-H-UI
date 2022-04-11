# import <
from requests import get
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from backend.utility import application, jsonLoad

# >


# global <
layoutStyle = jsonLoad(file = '/frontend/layoutStyle.json')
layoutData = 'https://raw.githubusercontent.com/ala2q6/CS490H-UI/main/frontend/layoutData.json'

# >


# layout <
application.layout = dbc.Container(

    fluid = True,
    style = layoutStyle['containerStyle'],
    children = [

        dbc.Row(

            id = 'rowId',
            justify = 'center',
            style = layoutStyle['rowStyle'],
            children = dbc.Col(id = 'colId')

        )

    ]

)

# >


# callback <
@application.callback(Output('colId', 'children'),
                      Input('rowId', 'children'))
def layoutCallback(arg: list):
    '''  '''

    # local <
    colChildren = []
    data = get(layoutData).json()
    print(data) # remove

    # >

    # iterate (headline, lead) in data <
    for headline, lead in data.items():

        # if (element is title) <
        if ('TITLE' in headline):

            colChildren.append(

                # title <
                html.H1(

                    children = lead[0],
                    style = layoutStyle['h1Style']

                )

                # >

            )

            colChildren.append(

                # subtitle <
                html.P(

                    children = lead[1],
                    style = layoutStyle['pStyle']

                )

                # >

            )

        # >

        # elif (element is image) <
        elif ('IMAGE' in headline):

            colChildren.append(

                dbc.CardImg(

                    src = lead,
                    style = layoutStyle['cardImgStyle']

                )

            )

        # >

        # elif (element is spacer) <
        elif ('SPACER' in headline):

            colChildren.append(

                html.Hr(style = layoutStyle['hrStyle'])

            )

        # >

        # else (element is text) <
        else:

            colChildren.append(

                dbc.CardBody(

                    style = layoutStyle['cardBodyStyle'],
                    children = [

                        # headline <
                        html.H3(

                            style = layoutStyle['h3Style'],
                            children = headline

                        ),

                        # >

                        # lead <
                        html.Small(

                            style = layoutStyle['smallStyle'],
                            children = dcc.Markdown('\n\n'.join(lead))

                        )

                        # >

                    ]

                )

            )

        # >

    # >

    # output <
    return colChildren

    # >

# >


# main <
if (__name__ == '__main__'): application.run_server()

# >
