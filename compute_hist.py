"""
This script takes the following command line arguments:

1. Filelist with the location of a netCDF tas tile 
2. The line to lead from that file list
3. The output directory. 

In the output directory, the following is stored for *each* year
in the input netCDF file [file identifier]:

	mdi [mdi] - max mdi 
	tw [tw] - max tw
	tai_mdi [tas_mdi] - tas during time of max mdi
	qi_mdi [huss_mdi] - huss ""
	pi_mdi [ps_mdi] - surface pressure ""
	tai_tw [tas_tw] - tas during time of max tw
	qi_tw [huss_tw] - q ""
	pi_tw [ps_tw] - surface pressure ""

Note that output output files have the following structure: 

	ssp.inst.model.year.[file identifier].nc

"""
# Settings
debug=True
metafin="/home/users/tommatthews/Homeostasis/CMIP6_META/histlist.txt"
odir="/gws/nopw/j04/ncas_generic/users/tmatthews/HOMEOSTASIS/CMIP6/"

# Import modules
import os,sys,utils
import numpy as np, xarray as xa

# Parse command line arguments
fileno=int(sys.argv[1])-1 # Note that we subtract 1 bcos py is zero-based

# Read and open the metafile
with open(metafin,"r") as m:
	fintas=m.readlines()[fileno]
	fintas=fintas.strip("\n")

if debug:
	print("Parsed:\n\t->Meta=%s\n\t->line no.=%.0f\n\t->file=%s\n\t->odir=%s"%\
	(metafin,fileno,fintas,odir))
#assert 1==2	
# Read in the tas file, and the huss/ps
# (using tas name as template to find others)
finhuss=fintas.replace("tas","huss")
finsp=fintas.replace("tas","ps")
dtas=xa.open_dataset(fintas)
dhuss=xa.open_dataset(finhuss)
dsp=xa.open_dataset(finsp)

# Extract meta data
ssp=fintas.split("/")[8]
inst=fintas.split("/")[6]
model=fintas.split("/")[7]

# Assign
ta=dtas["tas"]
q=dhuss["huss"]
p=dsp["ps"]
years=np.unique(ta.time.dt.year)

# Loop over all unique years in here
for y in years:

	# Select only this year
        tai=ta.sel(time=slice("%.0f-01-01 00:00"%y,"%.0f-01-01 00:01"%(y+1))).data[:,:,:]
        qi=q.sel(time=slice("%.0f-01-01 00:00"%y,"%.0f-01-01 00:01"%(y+1))).data[:,:,:]
        pi=p.sel(time=slice("%.0f-01-01 00:00"%y,"%.0f-01-01 00:01"%(y+1))).data[:,:,:]

        # Extract size
        nt,nr,nc=tai.shape

        # Skip if empty (can happen when end time stamp is given next year)
        if nt==1: continue

        # Include a dummy slice so that we can extract time for writing
        dummy=ta.sel(time=slice("%.0f-01-01 00:00"%y,"%.0f-01-01 00:01"%(y+1)))[:1,:,:]

	
	# Compute wetbulb
        tw=utils._TW3d(nt,nr,nc,tai,qi,pi)
	
	# Compute mdi
        mdi=utils._MDI(nt,nr,nc,tw,tai)
	
	# Find maxima for mdi and tw
        idx_mdi=np.nanargmax(mdi,axis=0)
        idx_tw=np.nanargmax(tw,axis=0)
	
	# Pull out based on these indices
        mdi=np.take_along_axis(mdi,idx_mdi[None,:,:],axis=0)
        tw=np.take_along_axis(tw,idx_tw[None,:,:],axis=0)
	
	# Repeat for component variables
	# mdi
        tai_mdi=np.take_along_axis(tai,idx_mdi[None,:,:],axis=0)
        qi_mdi=np.take_along_axis(qi,idx_mdi[None,:,:],axis=0)
        pi_mdi=np.take_along_axis(pi,idx_mdi[None,:,:],axis=0)
	
	# Tw
        tai_tw=np.take_along_axis(tai,idx_tw[None,:,:],axis=0)
        qi_tw=np.take_along_axis(qi,idx_tw[None,:,:],axis=0)
        pi_tw=np.take_along_axis(pi,idx_tw[None,:,:],axis=0)
	
	# Write out
        names=["mdi","tw","tas_mdi","huss_mdi","ps_mdi","tas_tw","huss_tw","ps_tw"]
        units=["Celsius","Kelvin","Kelvin","kg/kg","pa","Kelvin","kg/kg","pa"]
	
	# Iterate over and write
        i=0
        for d in [mdi,tw,tai_mdi,qi_mdi,pi_mdi,tai_tw,qi_tw,pi_tw]:
                oname="%s%s.%s.%s.%.0f.%s.nc"%(odir,ssp,inst,model,y,names[i])
                xa.DataArray(data=d,coords={"time":dummy.time,
                                        "lat":ta.lat,
                                        "lon":ta.lon},
                                        dims=["time","lat","lon"],
                                        name=names[i],
                                        attrs={"units":units[i]}).to_netcdf(oname)
					
                i+=1
	
	
