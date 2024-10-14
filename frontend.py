from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.io import curdoc
from bokeh.io import show
from bokeh.layouts import gridplot, column, row
from bokeh.models import (Slider, ColumnDataSource, Select,)

#TODO: Add widget settings as arguments
def create_splom(source, numeric_columns, colors, clusters):
    """
    This function creates all elements within the scatterplotmatrix with default settings. Refer to update_splom for
    changes after interactions
    :param source: data originating from the data loader, clustering according to widget inputs
    :param numeric_columns: numeric columns of the
    :param colors:
    :param clusters:
    :return:
    """

    x_ranges = {col: None for col in numeric_columns}
    y_ranges = {col: None for col in numeric_columns}

    scatter_plots = []
    plot_size = 250
    y_max = len(numeric_columns) - 1
    for i, y_col in enumerate(numeric_columns):
        for j, x_col in enumerate(numeric_columns):
            # Create figure and link axis ranges
            p = figure(width=plot_size, height=plot_size, x_axis_label=x_col, y_axis_label=y_col,
                       tools="pan,wheel_zoom,box_select,lasso_select,reset")

            # Link x and y ranges
            if x_ranges[x_col] is None:
                x_ranges[x_col] = p.x_range
            else:
                p.x_range = x_ranges[x_col]

            if y_ranges[y_col] is None:
                y_ranges[y_col] = p.y_range
            else:
                p.y_range = y_ranges[y_col]

            # Add circles, color by cluster
            p.scatter(source=source, x=x_col, y=y_col, fill_alpha=0.6, size=6,
                      fill_color=factor_cmap('cluster', palette=colors, factors=clusters),
                      line_color=factor_cmap('cluster', palette=colors, factors=clusters),
                      selection_color="red",
                      nonselection_fill_alpha=0.1,
                      nonselection_line_alpha=0.1)

            if j > 0:
                p.yaxis.axis_label = ""
                p.yaxis.visible = False

            if i < y_max:
                p.xaxis.axis_label = ""
                p.xaxis.visible = False

            scatter_plots.append(p)

    grid = gridplot(scatter_plots, ncols=len(numeric_columns))
    return grid

#TODO: Implement function which updates the interface according to specifications. Includes data_transformer if needed
def update_splom():
    pass


#TODO: Implement function to create Interface with all required elements (Maybe move into main)
def create_interface():
    pass