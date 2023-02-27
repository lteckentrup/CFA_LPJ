import pandas as pd
import numpy as np

df_PFT = pd.read_csv('PFT_classes.csv')
df_trait = pd.read_csv('../austraits-4.1.0/traits.csv',low_memory=False)

### Get list of PFTs
def grab_trait(trait_name, PFT_index):
    
    ### Get list of Victorian PFTs
    PFT_list = df_PFT.PFT.drop_duplicates().to_list()
    
    ### Get single PFT
    PFT = PFT_list[PFT_index]
    
    ### Get all taxa within PFT
    PFT_taxa = df_PFT[df_PFT['PFT'] == PFT].taxon.to_list()
    
    ### Get all traits for PFT
    PFT_traits = df_trait[df_trait['taxon_name'].isin(PFT_taxa)]
    
    ### Get specific trait for PFT
    PFT_trait_name = PFT_traits[PFT_traits['trait_name']==trait_name]
    
    ### Print info: Which PFT, are some from manipulation experiments?
    ### How many datapoints?
    
    print(PFT)
    print(PFT_trait_name.treatment_id.drop_duplicates().values)
    print(len(PFT_trait_name))

### Loop through all PFTs and get info on traits
for i in range(0,22):
    grab_trait('leaf_lifespan', i)
    grab_trait('leaf_mass_per_area',i)
