def get(self):
    """获取评论"""
    """
    "1": {
        "id": 1,
        "uid": 132,
        "nic_name": "15110962402",
        "avatar": "https://s1.ax1x.com/2020/09/09/w1qPFU.png",
        "content": "hello",
        "ctime": "2020-09-09 11:08:59",
        "sub_comments": [
            {
            "id": 2,
            "uid": 148,
            "nic_name": "12345678911",
            "avatar": "https://s1.ax1x.com/2020/09/09/w1qPFU.png",
            "content": "python",
            "ctime": "2020-09-09 11:09:52",
            "parent": 1,
            "reply_to": null,
            "reply_user": null
            },
            {
            "id": 3,
            "uid": 149,
            "nic_name": "15110962422",
            "avatar": "https://s1.ax1x.com/2020/09/09/w1qPFU.png",
            "content": "C++",
            "ctime": "2020-09-09 11:10:25",
            "parent": 1,
            "reply_to": "12345678911",
            "reply_user": 148
            },
            {
            "id": 4,
            "uid": 132,
            "nic_name": "15110962402",
            "avatar": "https://s1.ax1x.com/2020/09/09/w1qPFU.png",
            "content": "Go",
            "ctime": "2020-09-09 11:11:03",
            "parent": 1,
            "reply_to": "12345678911",
            "reply_user": 148
            }
        ]
        },
        "5": {
        "id": 5,
        "uid": 149,
        "nic_name": "15110962422",
        "avatar": "https://s1.ax1x.com/2020/09/09/w1qPFU.png",
        "content": "Ruby",
        "ctime": "2020-09-09 11:11:35"
        }
    }
    """
    vid = self.get_query_argument("vid")
    # 查询所有评论
    comments = DBUtil.selectAllComments(vid)
    comment_dic = {}
    for comment in comments:
        # 当前评论的用户
        user = DBUtil.GetUser(userid=comment['uid'])
        if comment['parent']:
            comment_dic[comment['parent']].setdefault('sub_comments', [])
            # 被回复评论的用户
            if comment['reply']:
                reply_com = DBUtil.selectComment(comment['reply'])
                reply_user = DBUtil.GetUser(userid=reply_com['uid'])
            else:
                reply_user = None
            comment_dic[comment['parent']]['sub_comments'].append({
                "id": comment['id'],
                "uid": comment['uid'],
                "nic_name": user['nickname'] or user['username'],
                "avatar": user['imageurl'],
                "content": comment['content'],
                "ctime": comment['create_time'],
                "parent": comment['parent'],
                "reply_to": reply_user['nickname'] or reply_user['username'] if reply_user else None,
                "reply_user": reply_user['id'] or reply_user['id'] if reply_user else None,
            })
        else:
            comment_dic[comment['id']] = {
                "id": comment['id'],
                "uid": comment['uid'],
                "nic_name": user['nickname'] or user['username'],
                "avatar": user['imageurl'],
                "content": comment['content'],
                "ctime": comment['create_time'],
            }
    if comment_dic:
        self.write({'status': 'ok', 'data': comment_dic})
    else:
        self.write({'status': 'error'})

@allow_login
def post(self, username):
    user = DBUtil.GetUser(username=username)
    try:
        vid = self.get_body_argument('vid')
        parent = self.get_body_argument('parent')
        reply = self.get_body_argument('reply')
        content = self.get_body_argument('content')
    except Exception as e:
        return self.write({'status': 'error', 'msg': '参数错误，请检查内容是否完整'})

    comment = {
        'uid': user['id'],
        'parent': parent,
        'reply': reply,
        'content': content,
        'vid': vid,
        'ctime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    res = DBUtil.save_comment(comment)
    if res:
        self.write({'status': 'ok', 'data': comment})
    else:
        self.write({'status': 'error', 'msg': '参水错误，请输入正确内容'})