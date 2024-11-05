import plotly.express as px
import seaborn as sns
from shiny.express import render, input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset

# ----------------------------------------------------
# Get the Data
# -----------------------------------------------------

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
with ui.sidebar(
