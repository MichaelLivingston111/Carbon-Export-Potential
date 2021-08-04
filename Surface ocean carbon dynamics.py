# Import packages:

import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.geoaxes
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Upload all the data
data = pd.read_csv("Carbon.csv")
data = data.drop([42, ])  # drop rows with zero as a value
data = data.drop([43, ])

x = np.log(data["Carbon_uptake"])  # Log the carbon uptake data
w = np.log(data["NP"])  # Log the carbon uptake data
y = data["TEP"]

# Set the theme
sns.set()

# Compute the R2 and p value for a regression between both variables:
r, p = stats.pearsonr(x, y)
r2, p2 = stats.pearsonr(x, w)

g = sns.jointplot(x=x, y=y, kind='reg')  # Create the relationship plot between carbon uptake and carbon gels:
phantom, = g.ax_joint.plot([], [], linestyle="", alpha=0)  # Plot the stats as a 'legend'
g.ax_joint.legend([phantom], ['R2={:f}, p={:f}'.format(r, p)])

# Make another plot, but for new production and carbon gels:
g2 = sns.jointplot(x=w, y=y, kind='reg')  # Create the relationship plot between carbon uptake and carbon gels:
phantom, = g2.ax_joint.plot([], [], linestyle="", alpha=0)  # Plot the stats as a 'legend'
g2.ax_joint.legend([phantom], ['R2={:f}, p={:f}'.format(r2, p2)])


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Now, we can plot these relationships on a map of the study area in order to better visualize them.
# Here, carbon uptake is represented by the size of the circle, new production is the outlined
# smaller circles, and carbon gel concentration is indicated by the colour.

# Set the max/min latitude/longitude boundaries in which to plot these relationships
min_lat_shelf = 47.55
max_lat_shelf = 49.53
min_lon_shelf = -128
max_lon_shelf = -124

min_lat = 45
max_lat = 55
min_lon = -150
max_lon = -122

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Upload and organize all the data in groups by season, with the relevant variables:

df = pd.DataFrame(data, columns=['Surface_uptake_layered', 'TEPC_5', 'Carbon_uptake', 'Small_carbon_uptake', 'Season',
                                 'longitude', 'latitude', 'Nitrate',
                                 'Nitrate_5', 'Carbon_layered', 'NP_5', 'Percent_TEP', 'TEP_5'])

Groups = df.groupby("Season")

Spring_group = Groups.get_group("Spring")
Summer_group = Groups.get_group("Summer")
Winter_group = Groups.get_group("Winter")

# The 'surface uptake layered' data is organized in a different fashion. It does NOT have the appropriate depths -
# all data is from 5m. It is total carbon uptake and small cell carbon uptake 'stacked' in a data frame.

# Make data available for a colour bar numpy array:
x_Sp = np.array(Spring_group["TEP_5"])
w_Sp = np.array(Spring_group["Surface_uptake_layered"])
y_Sp = np.array(Spring_group["Nitrate_5"])
q_Sp = np.array(Spring_group["Carbon_layered"])
n_Sp = np.array(Spring_group['NP_5'])

x_Su = np.array(Summer_group["TEP_5"])
w_Su = np.array(Summer_group["Surface_uptake_layered"])
y_Su = np.array(Summer_group["Nitrate_5"])
q_Su = np.array(Summer_group["Carbon_layered"])
n_Su = np.array(Summer_group['NP_5'])

x_Wi = np.array(Winter_group["TEP_5"])
w_Wi = np.array(Winter_group["Surface_uptake_layered"])
y_Wi = np.array(Winter_group["Nitrate_5"])
q_Wi = np.array(Winter_group["Carbon_layered"])
n_Wi = np.array(Winter_group['NP_5'])

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

fig = plt.figure(figsize=(8, 4))

grid = plt.GridSpec(3, 3, wspace=0.1, hspace=0.3)

# Spring 5m
ax = fig.add_subplot(grid[0, :2], projection=ccrs.PlateCarree())
# ax = fig.add_subplot(projection=ccrs.PlateCarree())  # Single plot
ax.scatter(Spring_group["longitude"], Spring_group["latitude"], c=x_Sp, s=q_Sp, edgecolors='none',
           cmap="cool", vmin=0, vmax=100, alpha=0.9,
           transform=ccrs.PlateCarree())
ax.scatter(Spring_group["longitude"], Spring_group["latitude"], c=x_Sp, s=n_Sp, edgecolors='k',
           cmap="cool", vmin=0, vmax=100, alpha=0.9,
           transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k', facecolor='silver')
ax.add_feature(cfeature.BORDERS)
ax.set_extent([min_lon, max_lon, min_lat, max_lat],
              crs=ccrs.PlateCarree())

# Spring 5m Zoom
ax = fig.add_subplot(grid[0, 2], projection=ccrs.PlateCarree())
# ax = fig.add_subplot(projection=ccrs.PlateCarree())  # Single plot
ax.scatter(Spring_group["longitude"], Spring_group["latitude"], c=x_Sp, s=q_Sp, edgecolors='none',
           cmap="cool", vmin=0, vmax=100, alpha=0.9,
           transform=ccrs.PlateCarree())
ax.scatter(Spring_group["longitude"], Spring_group["latitude"], c=x_Sp, s=n_Sp, edgecolors='k',
           cmap="cool", vmin=0, vmax=100, alpha=0.9,
           transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k', facecolor='silver')
ax.add_feature(cfeature.BORDERS)
ax.set_extent([min_lon_shelf, max_lon_shelf, min_lat_shelf, max_lat_shelf],
              crs=ccrs.PlateCarree())

# Summer 5m
ax = fig.add_subplot(grid[1, :2], projection=ccrs.PlateCarree())
# ax = fig.add_subplot(projection=ccrs.PlateCarree())  # Single plot
ax.scatter(Summer_group["longitude"], Summer_group["latitude"], s=q_Su, edgecolors='none',
           c=x_Su, vmin=0, vmax=100, cmap='cool', alpha=1,  # Set the color points and upper/lower limits
           transform=ccrs.PlateCarree())
ax.scatter(Summer_group["longitude"], Summer_group["latitude"], c=x_Su, s=n_Su, edgecolors='k',
           cmap="cool", vmin=0, vmax=100, alpha=1,
           transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k', facecolor='silver')
ax.add_feature(cfeature.BORDERS)
ax.set_extent([min_lon, max_lon, min_lat, max_lat],
              crs=ccrs.PlateCarree())

# Summer 5m Zoom
ax = fig.add_subplot(grid[1, 2], projection=ccrs.PlateCarree())
# ax = fig.add_subplot(projection=ccrs.PlateCarree())  # Single plot
ax.scatter(Summer_group["longitude"], Summer_group["latitude"], s=q_Su, edgecolors='none',
           c=x_Su, vmin=0, vmax=120, cmap='cool', alpha=1,  # Set the color points and upper/lower limits
           transform=ccrs.PlateCarree())
ax.scatter(Summer_group["longitude"], Summer_group["latitude"], c=x_Su, s=n_Su, edgecolors='k',
           cmap="cool", vmin=0, vmax=100, alpha=1,
           transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k', facecolor='silver')
ax.add_feature(cfeature.BORDERS)
ax.set_extent([min_lon_shelf, max_lon_shelf, min_lat_shelf, max_lat_shelf],
              crs=ccrs.PlateCarree())


# Winter 5m
ax = fig.add_subplot(grid[2, :2], projection=ccrs.PlateCarree())
# ax = fig.add_subplot(projection=ccrs.PlateCarree())  # Single plot
ax.scatter(Winter_group["longitude"], Winter_group["latitude"], s=q_Wi, edgecolors='none',
           c=x_Wi, vmin=0, vmax=100, cmap='cool', alpha=1,  # Set the color points and upper/lower limits
           transform=ccrs.PlateCarree())
ax.scatter(Winter_group["longitude"], Winter_group["latitude"], c=x_Wi, s=n_Wi, edgecolors='k',
           cmap="cool", vmin=0, vmax=100, alpha=1,
           transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cartopy.feature.LAND, zorder=100, edgecolor='k', facecolor='silver')
ax.add_feature(cfeature.BORDERS)
ax.set_extent([min_lon, max_lon, min_lat, max_lat],
              crs=ccrs.PlateCarree())
