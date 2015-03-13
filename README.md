BMinusLSUSY
===========
Getting set up:
---------------
First, download a copy of Madgraph5 either from:
  [https://launchpad.net/madgraph5](https://launchpad.net/madgraph5)

or get it directly using:
```
wget https://launchpad.net/madgraph5/trunk/1.5.0/+download/MadGraph5_v1.5.13.tar.gz
```

install pythia:
```
  cd MadGraph5_v1_5_13
  echo "install pythia-pgs" | ./bin/mg5
```

install MadAnalysis:
```
  cd MadGraph5_v1_5_13
  echo "install MadAnalysis" | ./bin/mg5
```

Run simple sample job:
----------------------
```
# Start madgraph:
./bin/mg5

# import model:
import model mssm

# generate simple process (stop pair production):
generate p p > t1 t1~

# If we want to add processes, we can add them similar to:
add process p p > W+ j, W+ > l+ vl @2
  
# export the process:
output MY_PROCESS

# We can come back to this work by doing the following:
launch MY_PROCESS
```
  
Within madgraph, you can output your history to a file, which may be useful for writing scripts:
```
history my_mg5_cmd.dat
open ./my_mg5_cmd.dat # this lets you view/edit the history file within mg5
```

Go to process folder, and now you can run madgraph + pythia for this setup:
```
./bin/generate_events
```
