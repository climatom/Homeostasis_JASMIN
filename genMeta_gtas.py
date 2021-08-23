import os

# output files:
ofile_hist="/home/users/tommatthews/Homeostasis/CMIP6_META/histlist_gtas.txt"
ofile_ssp="/home/users/tommatthews/Homeostasis/CMIP6_META/ssplist_gtas.txt"

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
table_id="Amon"
var1="tas"

# Optional parameters to filter files 
filter_yr=True
earliest_year_hist=1986
screen_size=False

insts=os.listdir(dataroot+"/"+mip_era+"/"+activity_id)
meta={} # Will store all meta info in dictionary of dictionaries {institute.model: {historical_files: list},{ssp: list}}

for i in range(len(insts)): 
   
    # Iterate over the models 
    instdir=dataroot+"/"+mip_era+"/"+activity_id+"/"+insts[i]
    
    for m in os.listdir(instdir):

        moddir="/".join([instdir,m,experiment_id,member_id,table_id,var1])

        # Do we have matching for the historical?

        histdir=moddir.replace("ssp585","historical").replace("ScenarioMIP","CMIP")

        if os.path.isdir(moddir) and os.path.isdir(histdir):
              if os.listdir(moddir) and os.listdir(histdir):
                 grid_mod=os.listdir(moddir)[0]
                 grid_hist=os.listdir(histdir)[0]
                 moddir+="/%s/latest"%grid_mod
                 histdir+="/%s/latest"%grid_hist

             	 # ... write them out, too
                 with open(ofile_ssp,"a+") as of: of.write(moddir+"\n") 
                
                 
                 # ... ditto, too
                 with open(ofile_hist,"a+") as oh: oh.write(histdir+"\n") 
            

