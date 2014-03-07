all: usurf.png PuBu.png mask.png

usurf.png: 1km_greenland.nc
	./nc2png.py $^ -v usurf -f -o $@

PuBu.png: 1km_greenland.nc
	./nc2png.py $^ -v csurf -f -l -t -o $@ -c PuBu

mask.png: 1km_greenland.nc
	./nc2png.py $^ -v mask -f -m 2 -o $@

clean:
	rm -f PuBu.png mask.png usurf.png

dem.geo: 1km_greenland.nc
	./nc2gmsh.py -m 5.0 -M 20.0 $^ -o dem.geo

dem.obj: dem.msh
	./msh2obj.py $^ -o $@

