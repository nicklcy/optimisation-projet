set exp_folder_path exp

set exp_list (ls $exp_folder_path)

for exp in $exp_list
    set exp_path $exp_folder_path/$exp
    echo exp: $exp
    python scripts/vis_exp.py --exp-dir $exp_path --no-show
end