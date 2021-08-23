import os

# output files:
ofile_hist="/home/users/tommatthews/Homeostasis/CMIP6_META/histlist.txt"
ofile_ssp="/home/users/tommatthews/Homeostasis/CMIP6_META/ssplist.txt"

# If exist, purge
for i in [ofile_hist,ofile_ssp]: 
	if os.path.isfile(i): os.remove(i)


# Format is: 
#<mip_era>/
 #     <activity_id>/
  #        <institution_id>/
   #           <source_id>/
    #              <experiment_id>/
     #                 <member_id>/
      #                    <table_id>/
       #                       <variable_id>/
        #                          <grid_label>/
         #                             <version>/
          #                              <CMOR filename>.nc

# Must haves: 
dataroot="/badc/cmip6/data"
mip_era="CMIP6"
activity_id="ScenarioMIP"#CMIP
experiment_id="ssp585"
member_id="r1i1p1f1"# Could try not restricting here
table_id="3hr"
var1="tas"
var2="huss"
var3="ps"

# Optional parameters to filter files 
filter_yr=True
earliest_year_hist=1985
screen_size=False

insts=os.listdir(dataroot+"/"+mip_era+"/"+activity_id)
meta={} # Will store all meta info in dictionary of dictionaries {institute.model: {historical_files: list},{ssp: list}}

for i in range(len(insts)): 
   
    # Iterate over the models 
    instdir=dataroot+"/"+mip_era+"/"+activity_id+"/"+insts[i]
    
    for m in os.listdir(instdir):

        moddir="/".join([instdir,m,experiment_id,member_id,table_id,var1])

        # Do we have all variables present?

        if os.path.isdir(moddir) and os.path.isdir(moddir.replace(var1,var2)) and os.path.isdir(moddir.replace(var1,var3)):

            # Do we have matching for the historical?

            histdir=moddir.replace("ssp585","historical").replace("ScenarioMIP","CMIP")

            if os.path.isdir(histdir):

                # ... And all variables present?               

                if os.path.isdir(histdir.replace(var1,var2)) and os.path.isdir(histdir.replace(var1,var3)):

                    if len(os.listdir(moddir))< 1 or len(os.listdir(histdir))<1: continue

                    grid_mod=os.listdir(moddir)[0]

                    grid_hist=os.listdir(histdir)[0]

                    moddir+="/%s/latest"%grid_mod

                    histdir+="/%s/latest"%grid_hist

                    ssp_files=[moddir+"/"+ii for ii in os.listdir(moddir)]
                    # ... write them out, too
                    with open(ofile_ssp,"a+") as of: 
                        for f in ssp_files:
                                of.write(f+"\n")
                

                    hist_files=[histdir+"/"+ii for ii in os.listdir(histdir)]
                    if filter_yr:
                        hist_files=[ii for ii in hist_files if int(ii.split("_")[-1].split("-")[-1][:4])>=earliest_year_hist]
                    # ... ditto, too
                    with open(ofile_hist,"a+") as oh: 
                        for f in hist_files:
                                oh.write(f+"\n")            
            
            	    # Store in dictionary in case it's helpful later. 

                    meta[insts[i]+"."+m]={

                                          experiment_id:ssp_files,\

                                         "historical": hist_files,

                                         }

                    # Preview file sizes if requested

                    if screen_size:

                        for h in hist_files: 

                            print("File %s is %.2f gb" % (h,os.path.getsize(h)/1e9))

                        for s in ssp_files: 

                            print("File %s is %.2f gb" % (s,os.path.getsize(s)/1e9))
