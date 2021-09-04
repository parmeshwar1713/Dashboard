from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import pandas as pd

from django.contrib import messages 
# from tablib import Dataset
import plotly.graph_objects as go

from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.subplots import make_subplots

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import numpy as np
import plotly
from . import plotly_app
from . import plotly_app1
import plotly.express as px
def index1(request):
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
   

    return render(request,"tempt.html",context={'fig':fig})

# def index1(request):
#     return HttpResponse("hey dev")
def simple_uload(request):
    if request.method=='POST':
        # dataset=Dataset()
        new_person=request.FILES['myfile']
        if not new_person.name.endswith('xlsx'):
            messages.info(request,'wrong form')
            return render(request,'exel/new.html')
        # imported_data=dataset.load(new_person.read(),format='xlsx')
        # df=pd.read_excel(new_person)
        global dev12
        dev12=new_person
        d = pd.ExcelFile(new_person)
        df = pd.read_excel(d)
        df.to_excel("test12.xlsx")
        # Quarter
        return render(request, "pl.html", )
    return render(request,'pl.html')
    

    # Document Date
