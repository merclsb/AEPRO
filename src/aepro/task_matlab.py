# -*- coding: utf-8 -*-

#Preparamos el entorno para poder invocar al modelo desde un script externo
import io
import os 
import sys
import django
import json
import numpy as np
import collections
#Matlab################
out = io.StringIO()
err = io.StringIO()
import matlab.engine as m
###########################
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print (BASE_DIR)
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
# from django.conf import settings
django.setup()

from aepro.models import Analisis, ResultadoCEP, ResultadoFDA


#-----Convert matlab.double array to python array
#For clarification: x.size[i] gives me the size of the matlab.double array. x._data gives an one dimensional array of type:
#array('d', [1.0,2.0,4.0 ... ])
#Therefore it includes a tolist() method to get an actual list, which I needed.
def convert(x):
  c = []
  for _ in range(x.size[1]):
      c.append(x._data[_*x.size[0]:_*x.size[0]+x.size[0]].tolist())
  return c[0]


########desde aqui invocar a MATLAB##############
eng = m.start_matlab() 
pid =int(eng.feature('getpid'))# obtenemos el PID del proceso Matlab, y no el PID del proceso python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR2 = os.path.join(BASE_DIR, "MATLAB/Funcionalv8")
eng.addpath(BASE_DIR2)

analisis = Analisis.objects.get(id_analisis=sys.argv[1])
Fecha_inicial = sys.argv[2]
Fecha_segunda = sys.argv[3]
Fecha_Final = sys.argv[4]
nombre_archivo = os.path.relpath("media/"+analisis.file.name)

#obtener la informacion de la instancia analisis
# id_analisis = analisis.id_analisis
if analisis.periodo=='AÑO':
  pa=1
elif analisis.periodo=='MES':
  pa=2
elif analisis.periodo=='DIA':
  pa=3

for tipo in analisis.tipo_analisis: #['CEP','FDA']
        if tipo == 'CEP':
          val= {'pid':pid,'estado':'run'}
          ResultadoCEP.objects.filter(analisis=sys.argv[1]).update(pid=val)
          a = eng.Analisis_Matlab_TFG_Vectorial(Fecha_inicial,Fecha_segunda,Fecha_Final,pa,nombre_archivo,async=True,nargout=7)
          #function [Datos,Descriptiva,stats_XS, R_XS,RULES_XS, plotdata_IMR,plotdata_IMR_MGR, FinProceso]=Analisis_Matlab_TFG_v2(f1,f2,f3,Tipo_Analisis,Periodo_Analisis,Nombre_archivo,id_analisis)

          #Valores devueltos por vectorial
          """
          Descriptiva,
          x-->Descriptiva_valores, No hace falta
          stats_XS, 
          R_XS,
          RULES_XS, 
          plotdata_IMR,
          plotdata_IMR_MGR,
          FinProceso
          x-->: No se puede plot_data, 
          
          """
          datos=[]
          datos.append([row[1] for row in a.result()[0]])#coger los datos de la segunda columna
 

          # STATS_XS
          dic_stats_XS = {}
          dic_stats_XS['mean'] = convert(a.result()[2]['mean'])#c[0]
          dic_stats_XS['std'] = convert(a.result()[2]['std'])#c[0]
          dic_stats_XS['n'] = convert(a.result()[2]['n'])#c[0]
          dic_stats_XS['range'] = convert(a.result()[2]['range'])#c[0]
          dic_stats_XS['mu'] = a.result()[2]['mu']#c[0]
          dic_stats_XS['sigma'] = a.result()[2]['sigma']#c[0]
          
          #R_XS
          #----R_XS
          dic_r_xs={}
          dic_r_xs['xs'] = a.result()[3]
          dic_r_xs['xs']=convert(dic_r_xs['xs'])
          dic_r_xs['row'] = len(a.result()[3])
          dic_r_xs['col'] = len(a.result()[3][0])

          #RULES_XS
          dic_rules_xs={}
          dic_rules_xs['rules'] = a.result()[4]

          #plotdata_IMR
          dic_imr={}
          dic_imr['pts'] = convert(a.result()[5]['pts'])#c[0]
          dic_imr['cl'] = convert(a.result()[5]['cl'])#c[0]
          dic_imr['lcl'] = convert(a.result()[5]['lcl'])#c[0]
          dic_imr['ucl'] = convert(a.result()[5]['ucl'])#c[0]
          dic_imr['se'] = convert(a.result()[5]['se'])#c[0]
          dic_imr['n'] = convert(a.result()[5]['n'])#c[0]
          dic_imr['ooc'] = convert(a.result()[5]['ooc'])#c[0]

          #plotdata_IMR_IMG
          dic_imr_img={}
          dic_imr_img['pts'] = convert(a.result()[6]['pts'])#c[0]
          dic_imr_img['cl'] = convert(a.result()[6]['cl'])#c[0]
          dic_imr_img['lcl'] = convert(a.result()[6]['lcl'])#c[0]
          dic_imr_img['ucl'] = convert(a.result()[6]['ucl'])#c[0]
          dic_imr_img['se'] = convert(a.result()[6]['se'])#c[0]
          dic_imr_img['n'] = convert(a.result()[6]['n'])#c[0]
          dic_imr_img['ooc'] = convert(a.result()[6]['ooc'])#c[0]


         
          #en valores se gudardan las variables por separado
          valores = {
            "datos": datos,
            "descriptiva": a.result()[1], # {}
            "stats_XS": dic_stats_XS, # {} a.result()[1]
            "r_xs": dic_r_xs,# "R_XS,
            "rules_xs":dic_rules_xs,# RULES_XS" 
            "imr":dic_imr,# "plotdata_IMR"
            "imr_img":dic_imr_img, # "plotdata_IMR_MGR"
            "xbar_nombre_grafica":'Resultado Xbar',
            "xbar_xasix":'x1',
            "xbar_yasix":'y1',
             }


          ResultadoCEP.objects.filter(analisis=sys.argv[1]).update(resultados=valores)
          val= {'pid':os.getpid(),'estado':'finish'}
          ResultadoCEP.objects.filter(analisis=sys.argv[1]).update(pid=val)

        if tipo == 'FDA':
          val= {'pid':pid,'estado':'run'}
          ResultadoFDA.objects.filter(analisis=sys.argv[1]).update(pid=val)
          b = eng.Analisis_Matlab_TFG_Funcional(Fecha_inicial,Fecha_segunda,Fecha_Final,pa,nombre_archivo, async=True,nargout=2)
          #valores devueltos por funcional
 
          c=[] # variable que almacena las curvas
          c_out=[] # variable que almacena las curvas que son outliers
          for i in range (len(b.result()[0][0])):
            c.append([row[i] for row in b.result()[0]])

          if not isinstance(b.result()[1], collections.Iterable):
                 c_out.append(int(b.result()[1]))
          else:
            for j in range (len(b.result()[1][0])):
              c_out.append(int(b.result()[1][0][j]))


          valores = {"x": c,
                     "y": c_out,
                     "nombre_grafica":'Resultado Analisis Funcional',
                     "xasix":'x1',
                     "yasix":'y1',
                }

          ResultadoFDA.objects.filter(analisis=sys.argv[1]).update(resultados=valores)
          val= {'pid':os.getpid(),'estado':'finish'}
          ResultadoFDA.objects.filter(analisis=sys.argv[1]).update(pid=val)

eng.quit()