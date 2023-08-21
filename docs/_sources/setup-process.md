# Setting up a Python Project

This note details how I set up a Python project on my Mac systems. I will add notes on doing the same setup on WIndows soon!


## Step 1. Create a project directory:

All projects should be contained under a single directory. I use a directory
named **_dev*** on my systems for all active projects:

```{code}
$ mkdir ~/_dev/jupyter-project
$ cd ~/_dev/jupyter-project
```

You should create a project name to help you remember what this project is
about. Do not just use **Project1** or something similar, you will never
remember what that project was about later!

## Step 2. Create the local directories needed:

Most of my Python projects use *Jupeterlab*  for testing code snippets, and
creating documentation. Here are subdirectories I usually create.

```{code}
$ mkdir -p book/images
$ mkdir docs
$ mkdir src
$ touch docs/.nojekyll
```

That last line is needed if you use *GitHub* to publish your notes. This is a
free website for developers who use *GitHub*.  

These directories hold basic
project files:

- book - This is where *Jupyter Notebook* files will be located
	- images - all graphics assets live here
- docs - HTML files end up here by the build process. GitHub can publish these on the web.
- src: This is where *Python source code will be stored

## Step 3. Create the working *Python* environment

These steps create a *Virtual Environment* to isolate this project from others in the development system.

```{code}
$ ~/_sys/PYPROJ/bootstrap.sh
$ make help
$ make pyprep
```

This script copies files from a directory on my system where I keep template files used in many projects. These will be detailed later.

The system I set up for **make** separates a **Makefile** into components related to different tools you might wish to use. The **make help** command displays the availabile commands pre-configured for this setup.

## Step 4. Install *Python* Project Requirements

At this point, review the **requirements.in** file. It has been pre-configured
for a basic *Jupyter* project. You will need to list any *Python* support
libraries you need for this project.

Since I use **make** for many tasks, here is how I install these requirements. (Look at the **mk** directory to see the **Makefile** components that do the real work.

```{code}
$ make pyreqs
```

## 
