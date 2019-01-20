# coding:utf-8


class Mypaginator:
    def __init__(self, totalCount, currentPage, itemsPerPage=10, maxPageNum=7, baseurl='/'):
        #数据总个数
        self.total_count = totalCount
        #当前页
        self.current_page = int(currentPage)
        #每页行数
        self.items_per_page = itemsPerPage
        #最多显示页面
        self.max_page_num = maxPageNum
        self.baseurl = baseurl

    @property
    def start(self):
        return (self.current_page-1) * self.items_per_page

    @property
    def end(self):
        return self.current_page * self.items_per_page

    @property
    def num_pages(self):
        pages = self.total_count % self.items_per_page
        if not pages:
            return self.total_count/self.items_per_page
        return (self.total_count/self.items_per_page)+1

    def page_range(self):
        #print(1)
        if self.num_pages < self.max_page_num:
            return range(1, self.num_pages + 1)
        #print(2)
        part = int(self.max_page_num / 2)
        if self.current_page - part < 1:
            return range(1, self.max_page_num + 1)
        #print(3)
        if self.current_page + part > self.num_pages:
            return range(self.num_pages + 1 - self.max_page_num, self.num_pages + 1)
        #print(4)
        return range(self.current_page - part, self.current_page + part + 1)

    def page_str(self):
        self.baseurl = str(self.baseurl)
        page_list = []
        if not self.num_pages:
            pass
        elif self.num_pages == 1:
            page_list.append('<li class="active"><a href="%s?p=%s">1</a></li>' % (self.baseurl,1))
            #print("elif")
        else:
            #print("else")
            #print("self.baseurl:",self.baseurl)
            page_list.append('<li><a href="%s?p=%s">首页</a></li>'%(self.baseurl,1))
            #print("shouye")
            if self.current_page <= 1:
                page_list.append('<li><a href="%s?p=%s">上一页</a></li>'%(self.baseurl,1))
            else:
                page_list.append('<li><a href="%s?p=%s">上一页</a></li>'%(self.baseurl,self.current_page - 1))
            for i in self.page_range():
                if i == self.current_page:
                    temp = '<li class="active"><a href="%s?p=%s">%s</a></li>' % (self.baseurl,i, i)
                else:
                    temp = '<li><a href="%s?p=%s">%s</a></li>' % (self.baseurl,i, i)
                page_list.append(temp)
            if self.current_page >= self.num_pages:
                page_list.append('<li><a href="%s?p=%s">下一页</a></li>' % (self.baseurl,self.num_pages))
            else:
                page_list.append('<li><a href="%s?p=%s">下一页</a></li>'%(self.baseurl,self.current_page + 1))
            page_list.append('<li><a href="%s?p=%s">尾页</a></li>'%(self.baseurl,self.num_pages))
        #print('page list:',page_list)
        return ''.join(page_list)

