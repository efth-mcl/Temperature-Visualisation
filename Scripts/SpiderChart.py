import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.cm
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.widgets import Slider


################## Read Data START ##################
#####################################################

# Df=pd.read_csv('SeaLandTimeCSV/Sea-Land_Global.csv')
Df=pd.read_csv('GLB.Ts+dSST.csv')
#####################################################
################### Read Data END ###################
                         ###
                         ###
                         ###
######## Data Cleansing & manipulation START ########
#####################################################

Df=Df.set_index('Year')
# in the missing values set the average of last 6 years
Df.at[2017,'Dec'] = pd.to_numeric(Df.loc[2010:2016]['Dec']).mean()
Df.at[2017,'Nov'] = pd.to_numeric(Df.loc[2010:2016]['Nov']).mean()

NP=Df.iloc[:,:12].as_matrix().astype('float') #array flattening
NP=NP.reshape(NP.size)
MAX=max(NP)
MIN=min(NP)
NP+=-MIN # this is necessary becose if we had negative values some line would be hyperbolas

#####################################################
######## Data Cleansing & manipulation END ##########
                         ###
                         ###
                         ###
############## Data Visualization START #############
#####################################################

class PolarPolyline:
    def __init__(self):
        M=12
        self.Qthetta = np.pi*2*np.linspace(0,1-1/M,M) # Quantized thetta
        self.Cthetta = np.pi*2*np.linspace(0,1-1/(M-1),(M-1)*60) # Continuous thetta
        self.R=[]

    def BuildPolyLine(self,r):
        self.R=[]
        Mcnt=0

        P=np.array([ self.Qthetta,r]).T # T means transpose & all points are polar coordinates
        while(True):
            t0=np.pi*2/12*np.linspace(Mcnt,(Mcnt+1),60) # between two points (e.g. Jan - Feb) drawing a line with 60 pieces
            P0=P[Mcnt]
            P1=P[Mcnt+1]

            p0=np.array([np.cos(P0[0]),np.sin(P0[0])])*P0[1]  # P0 to cartesian coordinates
            p1=np.array([np.cos(P1[0]),np.sin(P1[0])])*P1[1] # P1 to cartesian coordinates

            a=(p1[1]-p0[1])/(p1[0]-p0[0])
            b=-a*p0[0]+p0[1]

            # y=a*x+b cartesian line
            # r = b/(sin(t0)-a*cos(t0)  polar line
            self.R.append((b/(np.sin(t0)-a*np.cos(t0))))

            Mcnt+=1
            if Mcnt==12-1:
                break
        self.R=np.array(self.R)
        self.R=self.R.reshape(self.R.size)

        points = np.array([ self.Cthetta,self.R]).T.reshape(-1, 1, 2)

        return points

fig = plt.figure()
ax = fig.add_subplot(111, polar = True)
plt.subplots_adjust(left=0, bottom=0.2,right=0.8,top=0.9) # polar plot position


# Slider build Start
axcolor = 'lightgoldenrodyellow'
s_year_pos = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

S_Year = Slider(s_year_pos, 'Year', 1880, 2017, valinit=1880,valfmt='%i')
# Slider build End


ticks=np.linspace(np.min(NP),np.max(NP),6) # r axis values
tick_label=list(map(str,list(ticks+MIN))) # r axis labels (this fix the issue for negative values )

Months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] # thita axis labels




M=12 # months per year


r=NP[0:12] #first Year

PL=PolarPolyline()
points = PL.BuildPolyLine(r) #all points from poly line

segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments, cmap=plt.get_cmap('coolwarm'),  # create colorized polyline
                    norm=plt.Normalize(np.min(NP),np.max(NP)))
lc.set_array(PL.R) # array for how to colorized the polyline
lc.set_linewidth(3)

ax.scatter(PL.Qthetta,r,s=35,c=r,cmap=plt.cm.coolwarm,vmin=ticks[0],vmax=ticks[-1]) # plot points
ax.add_collection(lc) # plot colorized polyline

ax.set_rticks(ticks)
ax.set_yticklabels(tick_label)
ax.set_xticks(PL.Qthetta)
ax.set_rmax(np.max(NP)+0.06)
ax.set_xticklabels(Months)
ax.set_rlabel_position(-22.5)


# Colorbar build Start
cax = fig.add_axes([0.82,0.15,0.05,0.75])
cbar = fig.colorbar(ax.add_collection(lc), cax=cax, label=r"$d{T}_{s}$", ticks=ticks)
cbar.set_ticklabels(tick_label)
# Colorbar build end



def update(val):
    global scat
    Yeari = int(S_Year.val)-1880
    ax.cla()
    r=NP[M*Yeari:M*(Yeari+1)]

    points = PL.BuildPolyLine(r)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)


    # for same reason, we have faster update time if we create new lc
    # instead of set new segments
    # lc.set_segments(segments) #if you remove the comment add comments at the two next commands
    lc = LineCollection(segments, cmap=plt.get_cmap('coolwarm'),
                        norm=plt.Normalize(np.min(NP),np.max(NP)))

    lc.set_linewidth(3)
    lc.set_array(PL.R) # this is necessary

    ax.scatter(PL.Qthetta,r,s=50,c=r,cmap=plt.cm.coolwarm,vmin=ticks[0],vmax=ticks[-1])
    ax.add_collection(lc)
    ax.set_rticks(ticks)
    ax.set_yticklabels(tick_label)
    ax.set_rmax(np.max(NP)+0.06)
    ax.set_rlabel_position(-22.5)
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 12, endpoint=False))
    ax.set_xticklabels(Months)

    fig.canvas.draw_idle()


S_Year.on_changed(update)

plt.show()
#####################################################
############### Data Visualization END ##############
