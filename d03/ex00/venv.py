from importlib.resources import path
import  os

if __name__ == '__main__':
    carrent_dir = os.getcwd()
    env_param = os.environ
    path_env = env_param["PATH"]
    home_dir = env_param["HOME"]
    path_enf_list = path_env.split(":")
    for line in path_enf_list:
        if line.find(home_dir) >= 0:
            if line.find("/bin") >= 0 and line.find("local/bin") < 0:
                print(f"Your current virtual env is {line[0:line.find('/bin')]}")
                break