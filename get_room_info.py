import re
from urllib import request as req, parse
import json
'''
Host: www.douyu.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Cookie: dy_did=d810bd8dc32fa42451b9c18a00081501; acf_did=d810bd8dc32fa42451b9c18a00081501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1531863410,1531919292,1531923273; smidV2=20180718053656d378cf39c52a61cf4ae6c24b0a8a2f4900c125eb618fa5c50; _dys_refer_action_code=show_page_staydur; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1531923304
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
'''
#
# headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
#
# args_pat = re.compile(r'\$ROOM.args = ({.*})')
# info_pat = re.compile(r'var \$ROOM = ({.*})')
# room_id = '57321'
#
# base_url = 'http://www.douyu.com/'
# url = base_url + room_id
# reqs = req.Request(url=url, headers=headers)
# response = req.urlopen(reqs, timeout=20)
# result = response.read().decode('utf-8')
# room_info = info_pat.findall(result)[0]
# room_info_json = json.loads(room_info)
# room_args = args_pat.findall(result)[0]
# room_args_json = json.loads(room_args)
# server_config = room_args_json['server_config']
# server = parse.unquote(server_config)
# print(server_config)
# print(server)
# server_list = json.loads(server)
# print(server_list[0])
#
# ports_str = ''
# ports = []
# for server in server_list:
#     port = server['port']
#     if port not in ports:
#         str_port = 'tcp.port == ' + port
#         ports_str += str_port + ' || '
#         ports.append(port)
# print(ports_str[:-4])
#


server = "%5B%7B%22ip%22%3A%22119.90.49.110%22%2C%22port%22%3A%228050%22%7D%2C%7B%22ip%22%3A%22119.90.49.107%22%2C%22port%22%3A%228031%22%7D%2C%7B%22ip%22%3A%22119.90.49.91%22%2C%22port%22%3A%228052%22%7D%2C%7B%22ip%22%3A%22119.90.49.110%22%2C%22port%22%3A%228048%22%7D%2C%7B%22ip%22%3A%22119.90.49.86%22%2C%22port%22%3A%228078%22%7D%2C%7B%22ip%22%3A%22119.90.49.105%22%2C%22port%22%3A%228022%22%7D%2C%7B%22ip%22%3A%22119.90.49.88%22%2C%22port%22%3A%228089%22%7D%2C%7B%22ip%22%3A%22119.90.49.103%22%2C%22port%22%3A%228014%22%7D%2C%7B%22ip%22%3A%22119.90.49.95%22%2C%22port%22%3A%228071%22%7D%2C%7B%22ip%22%3A%22119.90.49.108%22%2C%22port%22%3A%228036%22%7D%2C%7B%22ip%22%3A%22119.90.49.105%22%2C%22port%22%3A%228023%22%7D%2C%7B%22ip%22%3A%22119.90.49.106%22%2C%22port%22%3A%228029%22%7D%2C%7B%22ip%22%3A%22119.90.49.86%22%2C%22port%22%3A%228080%22%7D%2C%7B%22ip%22%3A%22119.90.49.107%22%2C%22port%22%3A%228033%22%7D%2C%7B%22ip%22%3A%22119.90.49.101%22%2C%22port%22%3A%228003%22%7D%2C%7B%22ip%22%3A%22119.90.49.104%22%2C%22port%22%3A%228017%22%7D%2C%7B%22ip%22%3A%22119.90.49.101%22%2C%22port%22%3A%228004%22%7D%2C%7B%22ip%22%3A%22119.90.49.95%22%2C%22port%22%3A%228075%22%7D%2C%7B%22ip%22%3A%22119.90.49.94%22%2C%22port%22%3A%228067%22%7D%2C%7B%22ip%22%3A%22119.90.49.88%22%2C%22port%22%3A%228086%22%7D%2C%7B%22ip%22%3A%22119.90.49.109%22%2C%22port%22%3A%228042%22%7D%2C%7B%22ip%22%3A%22119.90.49.109%22%2C%22port%22%3A%228045%22%7D%2C%7B%22ip%22%3A%22119.90.49.94%22%2C%22port%22%3A%228070%22%7D%2C%7B%22ip%22%3A%22119.90.49.94%22%2C%22port%22%3A%228066%22%7D%2C%7B%22ip%22%3A%22119.90.49.109%22%2C%22port%22%3A%228044%22%7D%2C%7B%22ip%22%3A%22119.90.49.109%22%2C%22port%22%3A%228043%22%7D%2C%7B%22ip%22%3A%22119.90.49.95%22%2C%22port%22%3A%228074%22%7D%2C%7B%22ip%22%3A%22119.90.49.88%22%2C%22port%22%3A%228088%22%7D%2C%7B%22ip%22%3A%22175.25.18.123%22%2C%22port%22%3A%228097%22%7D%2C%7B%22ip%22%3A%22119.90.49.93%22%2C%22port%22%3A%228064%22%7D%5D"
server = parse.unquote(server)
print(server)
server_list = json.loads(server)
print(server_list[0])

ports_str = ''
ports = []
for server in server_list:
    port = server['port']
    if port not in ports:
        str_port = 'tcp.port == ' + port
        ports_str += str_port + ' || '
        ports.append(port)
print(ports_str[:-4])