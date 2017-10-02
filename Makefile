input=input.nc

usurf_levels=0,200,400,600,800,1000,1200,1400,1600,1800,2000,2200,2400,2600
thk_levels=100,200,300,400,500,600,700,800,900
resolution=0.5

colormap=PuBu
max_speed=1000
min_speed=1

all: dem.obj usurf.png velsurf_mag.png mask-thk.png mask-topg.png

usurf.png: ${input}
	./nc2png.py -v usurf ${input} -o $@

velsurf_mag.png: ${input}
	./nc2png.py -v velsurf_mag -c ${colormap} -t ${input} --clip_max ${max_speed} --clip_min ${min_speed} -o $@

mask-thk.png: ${input}
	./nc2png.py -v thk -m 95 ${input} -o $@

mask-topg.png: ${input}
	./nc2png.py -v topg -m 10 ${input} -o $@

%.obj: %.msh
	./msh2obj.py $^ -o $@

%.msh: %.geo
	gmsh -2 $^ -o $@

%.geo: ${input}
	./nc2gmsh.py -m ${resolution} -u ${usurf_levels} -t ${thk_levels} $^ -o $@

clean:
	rm -f dem.{geo,msh,obj} {usurf,velsurf_mag,mask-thk,mask-topg}.png
