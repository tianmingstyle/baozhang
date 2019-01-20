# coding:utf-8

class Pagination:
    def __init__(self, totalCount, currentPage, countItemPerPage=10, maxPages=7):
        self.total_count = totalCount
        try:
            self.current_Page = int(currentPage)
        except Exception as e:
            self.current_Page = 1
        self.count_item_per_page = countItemPerPage
        self.max_page = maxPages


    def start(self):
        return (self.current_Page-1) * self.count_item_per_page

    def end(self):
        return self.current_Page * self.count_item_per_page
    @property
    def numpages(self):
        if self.total_count%self.count_item_per_page:
            return self.total_count/self.count_item_per_page + 1
        return self.total_count/self.count_item_per_page


def index(request):
    totalCount = models.article.objects.count()
    currentPage = request.GET.get('p')
    obj = Pagination(totalCount, currentPage)
    data_list = models.article.objects.all()[obj.start:obj.end]
    return render(request, 'index.html', {'data':data_list})