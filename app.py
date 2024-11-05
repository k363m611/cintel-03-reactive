
import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
from shiny import render 
import palmerpenguins
from shiny import reactive


penguins_df = palmerpenguins.load_penguins()

with ui.layout_columns():
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def penguinstable_df():
            return render.DataTable(penguins_df, filters=False,selection_mode='row')
        

    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(penguins_df, filters=False, selection_mode="row")


with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute",
                       "Penguin Metric",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    ui.input_numeric(
        "plotly_bin_count",
        "Plotly Number of Bins",
        20
    )

    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Number of Bins",
        1,20,10
    )

    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie","Gentoo","Chinstrap"],
        selected=["Adelie","Gentoo","Chinstrap"],
        inline=False
    )

    ui.hr()

    ui.a(
        "GitHub",
        href= "https://github.com/Queensdelight/cintel-02-data/tree/main",
        target="_blank"
    )

ui.page_opts(title="Bukola's Penguin Data Practice", fillable=True)
with ui.layout_columns():

    @render_plotly
    def plot1():

        fig = px.histogram(
            penguins_df,
            x="bill_length_mm",
            title="Penguins Bill Length Histogram",
            color_discrete_sequence=["orange"],
        )
        fig.update_traces(marker_line_color="black", marker_line_width=2)
        return fig

    @render_plotly
   
    def plot2():
        selected_attribute = input.selected_attribute()
        bin_count = input.plotly_bin_count()
        
        fig = px.histogram(
            penguins_df,
            x=selected_attribute,
            nbins=bin_count,
            title=f"Penguins {selected_attribute} Histogram",
            color_discrete_sequence=["black"], 
        )
        fig.update_traces(marker_line_color="white", marker_line_width=2)
        return fig

with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        filtered_penguins = penguins_df[
                penguins_df["species"].isin(input.selected_species_list())
            ]
        fig = px.scatter(
                filtered_penguins,
                x="body_mass_g",
                y="flipper_length_mm",
                color="species",
                title="Penguins Scatterplot: Body Mass vs. Flipper Length",
                labels={
                    "body_mass_g": "Body Mass (g)",
                    "flipper_length_mm": "Flipper Length (mm)",
                },
            )
        return fig
    
    @render_plotly
    def density_plot():
        filtered_penguins = penguins_df[
            penguins_df["species"].isin(input.selected_species_list())
        ]
        fig = px.density_contour(
            filtered_penguins,
            
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            title="Density Plot: Bill Length vs Bill Depth by Species",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "bill_depth_mm": "Bill Depth (mm)"
            }
        )
        return fig

with ui.layout_columns():
    with ui.card():
        @render.plot(alt="Seaborn Histogram")
        def plot():
            ax=sns.histplot(data=penguins_df,x="flipper_length_mm",bins=input.seaborn_bin_count())
            ax.set_title("Seaborn: Palmer Penguins")
            ax.set_xlabel("flipper_length_mm")
            ax.set_ylabel("Count")
            return ax

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df
