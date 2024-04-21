set envs_list_path configs/env/basic_env_list
set envs_list (ls $envs_list_path)
set opt_list 'configs/opt/BGD.yaml' 'configs/opt/SGD.yaml'
set opt_list $opt_list 'configs/opt/Adam.yaml'

echo $envs_list

for env in $envs_list
  set full_env_path (echo $envs_list_path/$env)

  set num (string match -r '\d\d?' $env)

  if test $num -lt 7
    set N_list 3 4
  else
    if test $num -lt 9
      set N_list 3 4 5
    else
      set N_list 4 5 6
    end
  end

  for N in $N_list
  set init_tap_times_yaml \"\"
    for opt in $opt_list
      set command 'python scripts/run_exp_basic.py --N' $N \
        '--env' $full_env_path '--opt' $opt '--init-tap-times-yaml' $init_tap_times_yaml
      echo 'Do comamnd:' $command
      eval $command
      set init_tap_times_yaml "exp/"(ls exp/)[-1]"/config.yaml"
    end
  end
end
