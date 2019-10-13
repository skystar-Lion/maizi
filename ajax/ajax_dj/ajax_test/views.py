from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ajax_test.models import search
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, 'jq_post.html')

@csrf_exempt
def test(request):
    #content = '{"k1":"n1", "k2":"n2"}'
    content = """
        <note>
        <from>beijing</from>
        <to>hanzhong</to>
        </note>
    """
    response = HttpResponse(content, content_type = 'application/xml; charset=utf-8')
    response.status_code = 200
    return response


@csrf_exempt
def test2(request):
    func_name = request.GET.get('callback')
    temp = "%s(%s)" % (func_name, '{"k1":"n1", "k2":"n2"}')
    return HttpResponse(temp)

@csrf_exempt
def ps(request):
    #print(request.GET.get('search-text'))
    """
    print(request.POST.get('search-text'))
    response = HttpResponse('{"name":"666", "value":"222","password":"12121"}')
    response['Access-Control-Allow-Origin'] = '*'
    return response
    """
    
    request_keyword = request.POST.get('search-text')
    if  request_keyword:
        #先查询数据库，如果当前记录已经存在，则频数+1,否则存入到数据库
        result = search.objects.get(key_word = request_keyword)

        if result:
            result.times += 1
            result.save()
        else:
            record = search(key_word = request_keyword, times = 1)
            record.save()
        #查询数据库匹配的内容，然后以json格式返回
        query_set = search.objects.filter(key_word__regex = '^'+request_keyword).order_by('-times')[:4]
        data = serializers.serialize("json",query_set)
        #print(data)
        response = HttpResponse(data)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    
