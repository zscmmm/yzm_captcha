import yaml

# 假设你的 YAML 配置文件名为 config.yaml
yaml_file_path = 'conf/config.yaml'

# 读取 YAML 文件
with open(yaml_file_path, 'r') as file:
    config = yaml.safe_load(file)

gtconf = config['gt']['click']


