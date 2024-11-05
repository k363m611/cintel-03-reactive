import plotly.express as px
import seaborn as sns
from shiny.express import render, input, ui
from shinywidgets import render_plotly
import palmerpenguins # This package provides the Palmer Penguins dataset

# ----------------------------------------------------
# Get the Data
#-----------------------------------------------------

# ALWAYS familiarize yourself with the dataset you are working with first.
# Column names for the penguins dataset include:
# - species: penguin species (Chinstrap, Adelie, or Gentoo)
# - island: island name (Dream, Torgersen, or Biscoe) in the Palmer Archipelago
# - bill_length_mm: length of the bill in millimeters
# - bill_depth_mm: depth of the bill in millimeters
# - flipper_length_mm: length of the flipper in millimeters
# - body_mass_g: body mass in grams
# - sex: MALE or FEMALE

# Load the dataset into a pandas DataFrame.
# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# -----------------------------------------------------
# Define User Interface (ui)
# -----------------------------------------------------

ui.page_opts(title="Pinkston's Palmer Penguins PyShiny Plots", fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
# Set the open parameter to "open" to make the sidebar open by default
with ui.sidebar(position="right", open="open", bg="#d5d8dc"):
    # Use the ui.h2() function to add a 2nd level header to the sidebar
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    # pass in three arguments:
    ui.input_selectize(
        "selected_attribute",
        "Select an Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    #   pass in two arguments:
    ui.input_numeric(
        "plotly_bin_count",
        "# of Plotly Histogram Bins",
        value=10)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    #   pass in four arguments:
    ui.input_slider(
        "seaborn_bin_count",
        "# of Seaborn Bins",
        min=1,
        max=100,
        value=10)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    #   pass in five arguments:
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter by Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True)

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    #   pass in two arguments:
    ui.a(
        "My GitHub Repository",
        href="https://github.com/james-0177/cintel-02-data/tree/main",
        target="_blank")

# Main Content

# Display Data Table and Data Grid
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Table of Penguin Species")
        @render.data_frame
        def table():
            return render.DataTable(data=penguins_df)

    with ui.card(full_screen=True):
        ui.card_header("Data Grid of Penguin Species")
        @render.data_frame
        def grid():
             return render.DataGrid(data=penguins_df)

# Display Plotly and Seaborn Histograms
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Distribution of Penguins by Body Mass")
        @render_plotly
        def plot1():
            return px.histogram(penguins_df, x="body_mass_g", color="species", nbins=input.plotly_bin_count())
            
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Distribution of Penguins by Flipper Length")
        @render.plot
        def plot2():
            return sns.histplot(data=penguins_df, x="flipper_length_mm", hue="species", bins=input.seaborn_bin_count())

# Display Plotly Scatterplot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(data_frame=penguins_df, x="bill_length_mm", y="body_mass_g", color="species", hover_name="island", symbol="sex")

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
