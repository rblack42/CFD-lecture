# Setup Process

1. Create a project directory:

```{code}
$ mkdir ~/_dev/jupyter-project
$ cd ~/_dev/jupyter-project
```

2. Create the local directories needed:

```{code}
$ mkdir -p book/images
$ mkdir docs
$ mkdir src
$ touch docs/.nojekyll
```

These directories hold basic project files:

- book - This is where *Jupyter Notebook* will work
	- images - all graphics assets live here
- docs - HTML files end up here by the build process
- src: This is where *Python source code will be stored

3. Create the working *Python* environment

These steps create a *Virtual Environment* to isolate this project from others in the development system.

```{code}
$ ~/_sys/PYPROJ/bootstrap.sh
$ make help
$ make pyprep
```

This script copies files from a directory on my system where I keep template files used in many projects. These will be detailed later.

The system I set up for **make** separates a **Makefile** into components related to different tools you might wish to use. The **make help** command displays the availabile commands pre-configured for this setup.

4. Install *Python* Requirements

At this point, review the **requirements.in** file. It has been pre-configured for a *Jypyter* project.

```{code}
$ make pyreqs
```

```{note}
This is a note
```
