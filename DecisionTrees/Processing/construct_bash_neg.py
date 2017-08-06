import os

folder = "/dfs/scratch0/bosch/"
subfolders = ["BG-Data_Part11","BG-Data_Part12","BG_Data_Part2","BG_Data_Part3","BG_Data_Part5"]

with open("/lfs/local/camelo/DecisionTrees/Processing/process_negatives.sh", "w+") as f:
	for foldername in subfolders:
		for filename in os.listdir(folder+foldername+"/"):
			f.write("python /lfs/local/camelo/DecisionTrees/Processing/NegativeEach.py "+folder+foldername+"/ " +filename+"\n")

			

