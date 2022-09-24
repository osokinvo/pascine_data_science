import os
try:
    from pip._internal.operations import freeze
except ImportError:
    from pip.operations import freeze

if __name__ == '__main__':
    carrent_dir = os.getcwd()
    env_param = os.environ
    path_env = env_param["PATH"]
    home_dir = env_param["HOME"]
    path_enf_list = path_env.split(":")
    def_env = False
    for line in path_enf_list:
        if line.find(home_dir) >= 0:
            if line.find("/bin") >= 0 and line.find("local/bin") < 0:
                def_env = True
                if line.find("ghusk") < 0:
                    raise Exception
                break
    if not def_env:
        raise Exception
    x = freeze.freeze()
    f = open("requirements.txt", "w")
    for p in x:
        f.write(p + "\n")
    f.close()