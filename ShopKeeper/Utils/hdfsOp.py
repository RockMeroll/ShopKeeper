from Config import Config
from hdfs import InsecureClient, HdfsError

hdfs_host = Config.MyConfigParser.get("hdfs_config", "hdfs_host")
hdfs_user = Config.MyConfigParser.get("hdfs_config", "hdfs_user")
client = InsecureClient(hdfs_host, user=hdfs_user)
ori_dir = "json/"
drop_dir = "json_used/"

def get_file_paths(dir_path):
    try:
        return client.list(dir_path)
    except HdfsError:
        return []


def delete_file(file_path):
    client.rename(ori_dir + file_path, drop_dir + file_path)
    client.delete(file_path)


def save_to_hdfs(json, file_name):
    with client.write(ori_dir+file_name) as writer:
        writer.write(json)
    print file_name, "Save success"
