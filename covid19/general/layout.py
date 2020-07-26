import plotly.express as px
import numpy as np

COLOR_SCALE = px.colors.sequential.PuBu
COLOR_SCALE_GREYS = px.colors.sequential.Greys
COLOR_SCALE_GREEN = px.colors.sequential.PuBuGn


BASIC_LAYOUT = {
    'plot_bgcolor': 'white',
    'autosize': True,
    'xaxis': {
        'linecolor': COLOR_SCALE_GREYS[2],
        'showticklabels': True,
        'linewidth': 2,
        'ticks': 'outside',
        'gridcolor': COLOR_SCALE_GREYS[1]
        
        
    },
    'yaxis': {
        'linecolor': COLOR_SCALE_GREYS[2],
        'showticklabels': True,
        'linewidth': 2,
        'ticks': 'outside',
        'gridcolor': COLOR_SCALE_GREYS[1]
        
    },
}


CONFIG_SUBTITLE = {
   "font": {
        "size": 12,
        "color": COLOR_SCALE_GREYS[5],
    },
    "showarrow": False,
    "align": 'left',
    "x": -0.2,
    'xshift': 200,
    "y": 1.15,
    "xref": 'paper',
    "yref": 'paper', 
}

CONFIG_FOOTNOTE = {
   "font": {
        "size": 10,
        "color": COLOR_SCALE_GREYS[4],
    },
    "showarrow": False,
    "align": 'right',
    "xanchor": 'right',
    "yanchor": 'top',
    "x": 1,
    "y": -0.30,
    "xref": 'paper',
    "yref": 'paper', 
}

CONFIG_ANNOTATIONS_PLOT = {
    'arrowwidth': 1,
    'ax': -50,
    'showarrow': True, 
    'font': {
        'color': COLOR_SCALE[8], 
        'size': 10,
    },
    'bgcolor': '#ffffff', 
    'bordercolor': '#000000',
    'borderpad': 3, 
    'opacity': 0.6,
    'align': 'left'
}

CONFIG_ANNOTATIONS_PAPER = {
    'showarrow': False, 
    'font': {
        'color': COLOR_SCALE[8], 
        'size': 10,
    },
    'bgcolor': '#ffffff', 
    'borderpad': 3, 
    'opacity': 1,
    'xref': 'paper',
    'yref': 'paper',
    'xanchor': 'left',
    'align': 'left'
}

CONFIG_ANNOTATIONS_TIMELINE = {
   'arrowwidth': 2.5,
    'arrowhead': 6,
    'arrowcolor': COLOR_SCALE_GREYS[3],
    'ax': 0,
    'showarrow': True, 
    'font': {
        'color': COLOR_SCALE_GREYS[6], 
        'size': 12,
    },
    'bgcolor': "#FFFFFF", 
    'align': 'left',
    'xref': 'x',
    'yref': 'y',
    'xanchor': 'left',
    'yanchor': 'top',
    'width': 200,
    'borderpad': 4,
    'arrowsize': 0.8,
}



def change_color_bar(fig, graph_number, bar_info):
    
    index_ = np.where(fig['data'][graph_number].x == bar_info['x'])
    
    colors_ = list(fig['data'][graph_number].marker.color)
    
    
    for i in index_[0]:
        colors_[i] = bar_info['color']
    
    fig['data'][graph_number].marker.color = colors_   
    
    return fig
    
    

def update(fig, default_config, extra_config=None):

    # Apply default layout
    fig.update_layout(BASIC_LAYOUT)
    fig.update_layout(default_config)
    
    if extra_config is not None:
    
        annotations = []

        # Apply subtitle
        if 'subtitle' in extra_config.keys():
            temp_annotation = CONFIG_SUBTITLE.copy()
            temp_annotation.update({"text": extra_config['subtitle']})
            annotations.append(temp_annotation)

        # Apply footnote
        if 'footnote' in extra_config.keys():
            temp_annotation = CONFIG_FOOTNOTE.copy()
            temp_annotation.update({"text": extra_config['footnote']})
            annotations.append(temp_annotation)

        if 'annotations_plot' in extra_config.keys():
            for annotation in extra_config['annotations_plot']:
                temp_annotation = CONFIG_ANNOTATIONS_PLOT.copy()
                temp_annotation.update(annotation)

                annotations.append(temp_annotation)

        if 'annotations_paper' in extra_config.keys():
            for annotation in extra_config['annotations_paper']:
                temp_annotation = CONFIG_ANNOTATIONS_PAPER.copy()
                temp_annotation.update(annotation)

                annotations.append(temp_annotation)

        if 'annotations_paper' in extra_config.keys() or 'annotations_plot' in extra_config.keys():
            fig['layout']['annotations'] = annotations
    
    return fig

def create_annotation(config_annotation, type_annotation):
    
    if type_annotation == 'plot':
        temp_annotation = CONFIG_ANNOTATIONS_PLOT.copy()
        temp_annotation.update(config_annotation)
    elif type_annotation == 'paper':
        temp_annotation = CONFIG_ANNOTATIONS_PAPER.copy()
        temp_annotation.update(config_annotation)
    else:
        raise Exception("Escolha um tipo de anotação: plot ou paper")
    
    return temp_annotation

    
def insert_dropdown_restyle(fig, list_dropdown):

    menus = []
    
    for drop in list_dropdown:
        temp_dict = {
            'method': 'restyle',
            'label': drop['label'],
            'args': drop['args']
        }
        
        menus.append(temp_dict)
    
    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=menus,
                direction="up",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=0.03,
                yanchor="bottom"
            ),
        ]
    )
    
    return fig


def insert_dropdown_update(fig, list_dropdown):
    
    menus = []
    
    for drop in list_dropdown:
        temp_dict = {
            'method': 'update',
            'label': drop['label'],
            'args': drop['args']
        }
        
        menus.append(temp_dict)
    
    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=menus,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.3,
                yanchor="top"
            ),
        ]
    )
    
    return fig