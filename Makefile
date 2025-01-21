ifndef DST
$(error DST must be set to openttd source directory)
endif

all:
	python3 badges.py
	grfcodec -d -p1 badges.grf
	sed -i '1,/0C "Default Badges"/d' sprites/badges.nfo
	cat tool.txt sprites/badges.nfo > $(DST)/media/baseset/openttd/badges.nfo
	cp sprites/badges*.png $(DST)/media/baseset/openttd/
