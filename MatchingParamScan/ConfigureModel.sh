#!/bin/bash

model_name=$1
config_file="config_${model_name}.sh"

echo "" > $config_file
echo "import model mssm" >> $config_file
echo "define p = g u c d s u~ c~ d~ s~" >> $config_file
echo "define j = p" >> $config_file
echo "generate p p > t1 t1~" >> $config_file
echo "add process p p > t1 t1~ j" >> $config_file
echo "output $model_name" >> $config_file
echo "exit" >> $config_file
