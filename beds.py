from pybedtools import BedTool

gqs = BedTool('The_list.gff')
genes = BedTool('TAIR10.gff')

nearby = genes.window(gqs, stream=True)

out = open("window.gff","w")

out.write(str(nearby))
out.close()
