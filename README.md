# PCB TOOLS

This repo aimed to be added as submodule to any PCB project.


Add this repo to PCB project:

```
git submodule add https://github.com/sainquake/pcb-tools scripts/pcb-tools
```

Copy paste `prepare-commit-msg` to `.git\hooks` folder.

Update submodule pcb-tools:

```
cd scripts/pcb-tools/ &&
git pull
```

Add pcb-versions repo to PCB project:

```
git submodule add https://github.com/RaccoonLabHardware/pcb-versions.git scripts/pcb-versions
```

Add this repo to PCB project:
```
cd scripts/pcb-versions/ &&
git pull
```


