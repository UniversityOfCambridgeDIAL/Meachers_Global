from django.shortcuts import render
from axiom.models import Project, Project_buffer
from .models import QrCode
from django.http import HttpResponse
import os
from datetime import datetime
import time
import csv
#import numpy as np

# Create your views here.
#def hello_world(request):
#	return render(request, 'hello_world.html', {})


def project_index(request):
    projects = Project.objects.all()
    buffer = Project_buffer.objects.all()
    return render(request, 'project_index.html', {'projects': projects, 'buffer': buffer})


def project_detail(request, pk):
    fin_all=[]
    project = Project.objects.get(pk=pk)
    x= tim_diff(project.time_in,project.time_out)
    w1=tim_diff(project.w1_start, project.w1_stop)
    w2=tim_diff(project.w2_start, project.w2_stop)
    w3=tim_diff(project.w3_start, project.w3_stop)
    w4=tim_diff(project.w4_start, project.w4_stop)
    w5=tim_diff(project.w5_start, project.w5_stop)
    unload_time_order=x
    fin=chk_work(project.order_id,project.container,unload_time_order,w1,w2,w3,w4,w5)
    #(ids,cont,total,workers,w1x,w2x,w3x,w4x,w5x )
    
#    buffer = Project_buffer.objects.get(order_id='yet2200')
#    project = Project.objects.all()
    context = {
        'project': project,
        'tot_tim':fin[2],
        'w1_t':fin[4],
        'w2_t':fin[5],
        'w3_t':fin[6],
        'w4_t':fin[7],
        'w5_t':fin[8],
         'men':fin[3],
         'tw':fin[9]
#        'buffer': buffer
    }
    return render(request, 'project_detail.html', context)


def home(request):
    if request.method=="POST":
        Url=request.POST['url']
        QrCode.objects.create(url=Url)
        qr_code=QrCode.objects.all()
    else:
        qr_code=None
    return render(request,"home.html",{'qr_code':qr_code})



def createpost(request):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        time.sleep(2)
        if request.method == 'POST':
            if request.POST.get('order_id') and request.POST.get('container'):
                post=Project()
                post.order_id= request.POST.get('order_id')
                post.container= request.POST.get('container')
                post.date_work=request.POST.get('date_work')
                post.time_in=request.POST.get('time_in')
                post.time_out=request.POST.get('time_out')
                post.w1_start=request.POST.get('w1_start')
                post.w2_start=request.POST.get('w2_start')
                post.w3_start=request.POST.get('w3_start')
                post.w4_start=request.POST.get('w4_start')
                post.w5_start=request.POST.get('w5_start')
                post.w1_stop=request.POST.get('w1_stop')
                post.w2_stop=request.POST.get('w2_stop')
                post.w3_stop=request.POST.get('w3_stop')
                post.w4_stop=request.POST.get('w4_stop')
                post.w5_stop=request.POST.get('w5_stop')
                post.supervisor=request.POST.get('supervisor')
                post.product=request.POST.get('product')
                post.packages=request.POST.get('packages')
                post.sku=request.POST.get('sku')
                post.size=request.POST.get('size')
                post.timestamp=dt_string
                post.save()
                return render(request, 'createpost.html')  

        else:
                return render(request,'createpost.html')



def analysis(request):
    labels = []
    data = []
    order = []
    work = []
    w1=[]
    w2=[]
    w3=[]
    w4=[]
    w5=[]
    tw=[]

    queryset = Project_buffer.objects.order_by('-container')
    for orders in queryset:
        labels.append(orders.container)
        data.append(orders.unload_time)
        work.append(orders.workers)
        order.append(orders.order_id)
        w1.append(orders.w1)
        w2.append(orders.w2)
        w3.append(orders.w3)
        w4.append(orders.w4)
        w5.append(orders.w5)
        tw.append(orders.tw)

    return render(request, 'analysis.html', {
        'labels': labels,
        'data': data,
        'work': work,
        'id': order,
        'w1':w1,
        'w2':w2,
        'w3':w3,
        'w4':w4,
        'w5':w5,
        'tw':tw,
    })


def chk_tmfmt(dat):
    if dat=='':
        return '00:00'
    else:
        return dat
    

def tim_diff(d1,d2):
    
    if d1 and d2 == '':
        return 0.0
    else:
        FMT = '%H:%M'
        tdelta = datetime.strptime(chk_tmfmt(d2), FMT) - datetime.strptime(chk_tmfmt(d1), FMT)
        return tdelta.total_seconds()/60



def chk_work(ids,cont,total,w1,w2,w3,w4,w5):
    
    for i in range(len(ids)):
        x=(w1,w2,w3,w4,w5)
        workers=5-x.count(0)
        w1x=(w1/total)*total
        w2x=(w2/total)*total
        w3x=(w3/total)*total
        w4x=(w4/total)*total
        w5x=(w5/total)*total
        tw=w1x+w2x+w3x+w4x+w5x

    return (ids,cont,total,workers,w1x,w2x,w3x,w4x,w5x,tw)




def summary(request):

    fin_all=[]
    Project_buffer.objects.all().delete()

    queryset = Project.objects.order_by('-timestamp')
    for orders in queryset:
        orderids=orders.order_id
        container=orders.container
        x= tim_diff(orders.time_in,orders.time_out)
        w1=tim_diff(orders.w1_start, orders.w1_stop)
        w2=tim_diff(orders.w2_start, orders.w2_stop)
        w3=tim_diff(orders.w3_start, orders.w3_stop)
        w4=tim_diff(orders.w4_start, orders.w4_stop)
        w5=tim_diff(orders.w5_start, orders.w5_stop)
        unload_time_order=x
        fin=chk_work(orderids,container,unload_time_order,w1,w2,w3,w4,w5)
        #print(fin)
        #Project_buffer.objects.all().delete()
        pt=Project_buffer()
        pt.order_id=fin[0]
        pt.container=fin[1]
        pt.unload_time=fin[2]
        pt.workers=fin[3]
        pt.w1=fin[4]
        pt.w2=fin[5]
        pt.w3=fin[6]
        pt.w4=fin[7]
        pt.w5=fin[8]
        pt.tw=fin[9]
        pt.save()
       #print(orders.order_id+"  "+str(x))
       # print(fin)
    buffer = Project_buffer.objects.all()
    return render(request, 'summary.html', {'buffer': buffer})


#def analysis(request):
#
#    unload_time_order=[]
#    orderids=[]
#    w1=[]
#    w2=[]
#    w3=[]
#    w4=[]
#    w5=[]
#    fin=[]
#    
#    queryset = Project.objects.order_by('-timestamp')
#    for orders in queryset:
#        orderids.append(orders.order_id)
#        x= tim_diff(orders.time_in,orders.time_out)
#        w1.append(tim_diff(orders.w1_start, orders.w1_stop))
#        w2.append(tim_diff(orders.w2_start, orders.w2_stop))
#        w3.append(tim_diff(orders.w3_start, orders.w3_stop))
#        w4.append(tim_diff(orders.w4_start, orders.w4_stop))
#        w5.append(tim_diff(orders.w5_start, orders.w5_stop))
#        unload_time_order.append(x)
#        fin.append(chk_work(orderids,unload_time_order,w1,w2,w3,w4,w5))
#
#       #print(orders.order_id+"  "+str(x))
#    print(fin)
#
#    
#    return render(request, 'analysis.html', {
#        'labels': orderids,
#        'data': unload_time_order,
#        'data1': w1,
#    })






def analysis1(request):
    labels = []
    data = []
    diff = []

    queryset = Project.objects.order_by('-supervisor')
    for orders in queryset:
        labels.append(orders.supervisor)
        data.append(orders.order_id)
        s2 = orders.time_out
        s1 = orders.time_in
        FMT = '%H:%M'
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        diff.append(tdelta.total_seconds()/60)
        #print(tdelta.total_seconds()/60)
    print(diff)
    return render(request, 'analysis1.html', {
        'labels': labels,
        'data': diff,
    })


def analysis2(request):
    labels = []
    data = []
    diff = []

    queryset = Project.objects.order_by('-timestamp')
    for orders in queryset:
        labels.append(orders.order_id)
        data.append(orders.packages)
        s2 = orders.time_out
        s1 = orders.time_in
        FMT = '%H:%M'
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        diff.append(tdelta.total_seconds()/60)
        #print(tdelta.total_seconds()/60)

    return render(request, 'analysis2.html', {
        'labels': labels,
        'data': diff,
        'data1': data,
    })


def csv_database_write(request):
    unload_time_order=[]
    orderids=[]
    w1=[]
    w2=[]
    fin=[]
    # Get all data from UserDetail Databse Table
    users = Project.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_database_write.csv"'
    writer = csv.writer(response)
    writer.writerow(['timestamp', 'order-id', 'container_id',  'container_size', 'packages', 'sku', 'unload_time(m)', 'Workers', 'Man hours (mins.)'])

    for user in users:
        orderids.append(user.order_id)
        s2 = user.time_out
        s1 = user.time_in
        FMT = '%H:%M'
        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
        unload_time_order= tdelta.total_seconds()/60
        w1=tim_diff(user.w1_start, user.w1_stop)
        w2=tim_diff(user.w2_start, user.w2_stop)
        w3=tim_diff(user.w3_start, user.w3_stop)
        w4=tim_diff(user.w4_start, user.w4_stop)
        w5=tim_diff(user.w5_start, user.w5_stop)
        fin=chk_work(user.order_id,user.container,unload_time_order,w1,w2,w3,w4,w5)
        #w1= (datetime.strptime(user.w1_stop, FMT) - datetime.strptime(user.w1_start, FMT)).total_seconds()/60
        #w2= (datetime.strptime(user.w2_stop, FMT) - datetime.strptime(user.w2_start, FMT)).total_seconds()/60
        #print(unload_time_order)
        writer.writerow([user.timestamp, user.order_id, user.container, user.size, user.packages, user.sku, unload_time_order, fin[3], fin[9]])
    return response


#def exportcsv(request):
#    unload_time_order=[]
#    orderids=[]
#    w1=[]
#    w2=[]
#    w3=[]
#    w4=[]
#    w5=[]
#    response = HttpResponse(content_type='text/csv')
#    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'
#
#    writer = csv.writer(response)
#    writer.writerow(['first_name', 'last_name', 'phone_number', 'country'])
#    writer.writerow(['Huzaif', 'Sayyed', '+919954465169', 'India'])
#    writer.writerow(['Adil', 'Shaikh', '+91545454169', 'India'])
#    writer.writerow(['Ahtesham', 'Shah', '+917554554169', 'India'])
#
#    return response
    
#    queryset = Project.objects.order_by('-timestamp')
#    for orders in queryset:
#        orderids.append(orders.order_id)
#        s2 = orders.time_out
#        s1 = orders.time_in
#        FMT = '%H:%M'
#        tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
#        unload_time_order.append(tdelta.total_seconds()/60)
#        w1.append((datetime.strptime(orders.w1_stop, FMT) - datetime.strptime(orders.w1_start, FMT)).total_seconds()/60)
#        w2.append((datetime.strptime(orders.w2_stop, FMT) - datetime.strptime(orders.w2_start, FMT)).total_seconds()/60)
#        w3.append((datetime.strptime(orders.w3_stop, FMT) - datetime.strptime(orders.w3_start, FMT)).total_seconds()/60)
#        w4.append((datetime.strptime(orders.w4_stop, FMT) - datetime.strptime(orders.w4_start, FMT)).total_seconds()/60)
#        w5.append((datetime.strptime(orders.w5_stop, FMT) - datetime.strptime(orders.w5_start, FMT)).total_seconds()/60)
#    
        
    





