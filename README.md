# cloudhw3
# Spark Assignment 3

This assignment is based on the 3rd chapter of the book - 'Advanced Big Data Analytics with Spark'. You can find a copy of the book here.

In this assignment, you will be required to build a recommendation system using Spark and MLib using a dataset published by AudioScrobbler. This data is 500MB uncompressed and can be downloaded here.

You can glance through the chapter and understand how to build the recommendation system. The chapter will walk you through Scala code; however; you are expected to code in Python. Also, the instructions below will help you run this recommendation system on a single node. We will be releasing instructions on how to run a Spark cluster on AWS EMR soon.

# Setup

You will be using the same setup you used for the Spark mini homework. But, because the data set you will be working with is much larger, you will be required to reserve at least 2.5Gb of memory to run Spark computations. Here are the steps that you need to follow:

Use the same vagrant file that you used in the last assignment which will instantiate an Ubuntu virtual machine for you.
Once we have the machine up and running and you have ssh-ed into it, run the 'ls' command to see the files in this directory. You will see a spark-notebook.py file. Open this file using vi, search 'driver-memory' in this file and update its value to '2536M'. Save and close this file and restart the VM.
Now when you ssh into the machine again, run this script using the command python spark_notebook.py. This will launch PySpark with IPython notebook. The server will be listening on port 8001.
Open your browser and enter the url http://localhost:8001. This will open Jupyter in your browser, following which you can create a notebook and run PySpark commands from it.
Loading the Data

After you have downloaded the AudioScrobbler data, copy-paste it into the vagrant folder locally. This will load the data in your VM at the location /vagrant.
To get this into your home directory in the VM, simply run the command cp -avr /vagrant/audio_data/ /home/vagrant/ Now you can use this data in your notebook.
# Problem

Build a recommendation system in Python on the lines of the one described in chapter 3. You are required to use the same Machine Learning model used in the book so that the results remain consistent across all groups. While the book evaluates how well the model is performing, you are only required to provide top 10 recommendations for a user.
Note: Just so you know what to expect, Spark computations on a data set of this size can take upto 10-15 minutes.
