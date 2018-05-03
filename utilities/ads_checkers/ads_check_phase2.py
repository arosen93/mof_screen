import pymatgen as pm
from pymatgen.analysis.local_env import MinimumVIRENN
import numpy as np
import os

results_path = '/projects/p30148/vasp_jobs/MOFs/oxidized_oms/results/'
output_name = 'bad_ads_addition.txt'
ads_species = 'O'
NN_file_name = 'NN_list.txt'
nonmetals_list = ['H','He','C','N','O','F','Ne','P','S','Cl','Ar','Se','Br','Kr','I','Xe','Rn']
bad_jobs = []
good_refcodes = []
NN_list_all = []
for refcode in os.listdir(results_path):
	spe_path = results_path+refcode+'/final_spe/'
	if os.path.isdir(spe_path):
		for subdir in os.listdir(spe_path):
			dist = []
			NN_list = []
			full_name = refcode+'_'+subdir
			contcar_path = spe_path+subdir+'/CONTCAR'
			struct = pm.Structure.from_file(contcar_path,primitive=False,sort=False)
			nn_object = MinimumVIRENN()
			ads_idx = [i for i, atom in enumerate(struct) if atom.species_string == ads_species][-1]
			neighbors = nn_object.get_nn_info(struct,ads_idx)
			if neighbors:
				for neighbor in neighbors:
					NN_list.append(neighbor['site'].specie.symbol)
					dist.append(struct.get_distance(ads_idx,neighbor['site_index']))
				if neighbors[np.argmin(dist)]['site'].species_string in nonmetals_list:
					bad_jobs.append(full_name)
					continue
			else:
				bad_jobs.append(full_name)
				continue
			good_refcodes.append(full_name)
			NN_list_all.append(NN_list)

with open(results_path+NN_file_name,'w') as wf:
	for i, NN_list in enumerate(NN_list_all):
		wf.write(good_refcodes[i]+'|'+','.join(NN_list)+'\n')
bad_jobs.sort()
with open(results_path+output_name,'w') as wf:
	for bad_job in bad_jobs:
		wf.write(bad_job+'\n')