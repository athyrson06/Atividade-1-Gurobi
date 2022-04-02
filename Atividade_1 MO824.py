# -*- coding: utf-8 -*-
"""Atividade 1 - semi.ipynb """

# Importa a biblioteca do Gurobi
import gurobipy as gp

#Importa funções relacionadas a geração de números aleatórios
from random import uniform

from random import seed
#Semente que define os números aleatórios gerados
seed(314)

#define a quantidade de clientes que a companhia atende para a instância 
qtd_clientes = 100

#função para geração dos parâmetros aleatórios para a instância do problema baseados no número de clientes
def create_inst(qtd_clientes_J):
    qtd_fabricas_F = round(uniform(qtd_clientes_J, 2 * qtd_clientes_J)) #quantidade de fábricas que a companhia possui
    qtd_maquinas_L = round(uniform(5,10)) #tipos de máquinas que a companhia possui
    qtd_materias_M = round(uniform(5,10)) #tipos de máterias-primas que a companhia possui
    qtd_produtos_P = round(uniform(5,10)) ##tipos de produtos que a companhia produz
    #Dj,p = demanda do cliente j, em toneladas, do produto p;
    D_jp = [[round(uniform(10,20)) for i in range(qtd_clientes_J)] for j in range(qtd_produtos_P)]
    #rm,p,l = quantidade de matéria-prima m, em toneladas, necessária para produzir uma tonelada do produto p na máquina l;
    r_mpl = [[[round(uniform(1,5)) for i in range(qtd_materias_M)] for j in range(qtd_produtos_P)] for k in range(qtd_maquinas_L)]
    # Rm,f = quantidade de matéria-prima m, em toneladas, disponível na fábrica f ;
    R_mf = [[round(uniform(800,1000)) for i in range(qtd_materias_M)] for j in range(qtd_fabricas_F)] 
    # Cl,f = capacidade disponível de produção, em toneladas, da máquina l na fábrica f ;
    C_lf = [[round(uniform(80,100)) for i in range(qtd_maquinas_L)] for j in range(qtd_fabricas_F)]
    # pp,l,f = custo de produção por tonelada do produto p utilizando a máquina l na fábrica f ;
    p_plf = [[[round(uniform(10,100)) for i in range(qtd_produtos_P)] for j in range(qtd_maquinas_L)] for k in range(qtd_fabricas_F)]
    # tp,f,j = custo de transporte por tonelada do produto p partindo da fábrica f até o cliente j;
    t_pfj = [[[round(uniform(10,20)) for i in range(qtd_produtos_P)] for j in range(qtd_fabricas_F)] for k in range(qtd_clientes_J)]
    
    return qtd_fabricas_F, qtd_maquinas_L,qtd_materias_M,  qtd_produtos_P, D_jp, r_mpl,R_mf, C_lf,p_plf,t_pfj;

#chama a função de criação de instância que gera os parâmetros do problema
qtd_fabricas_F, qtd_maquinas_L,qtd_materias_M, qtd_produtos_P, D_jp, r_mpl,R_mf, C_lf,p_plf,t_pfj = create_inst(qtd_clientes)

#Geração de rótulos
clientes = list()
for i in range(qtd_clientes):
    clientes.append("Cliente_{}".format(i + 1))

fabricas = list()
for i in range(qtd_fabricas_F):
    fabricas.append("fabrica_{}".format(i + 1))

maquinas = list()
for i in range(qtd_maquinas_L):
    maquinas.append("maquina_{}".format(i + 1))

materias = list()
for i in range(qtd_materias_M):
    materias.append("materia_{}".format(i + 1))

produtos = list()
for i in range(qtd_produtos_P):
    produtos.append("produto_{}".format(i + 1))

#criação de um dicionário para armazenar as demandas de todos os clientes por todos os produtos 
demandas = dict()
for j in range(qtd_clientes):
    rot_cli = clientes[j]
    for p in range(qtd_produtos_P):  
        rot_pro = produtos[p]
        demandas[rot_cli,rot_pro] = D_jp[p][j]
        
#criação de um dicionário para armazenar cada quantidade de matéria-prima necessária para produzir cada produto em cada máquina
mat_nec = dict()
for m in range(qtd_materias_M):
    rot_mat = materias[m]
    for p in range(qtd_produtos_P):
        rot_pro = produtos[p]
        for l in range(qtd_maquinas_L):
            rot_maq = maquinas[l]
            mat_nec[rot_mat, rot_pro, rot_maq] = r_mpl[l][p][m]

#criação de um dicionário para armazenar as quantidades de cada matéria-prima disponível em cada fábrica
mat_disp = dict()
for m in range(qtd_materias_M):
    rot_mat = materias[m]
    for f in range(qtd_fabricas_F):  
        rot_fab = fabricas[f]
        mat_disp[rot_mat,rot_fab] = R_mf[f][m]
        
#criação de um dicionário para armazenar a capacidade disponível de produção de cada máquina em cada fábrica
cap_prod = dict()
for l in range(qtd_maquinas_L):
    rot_maq = maquinas[l]
    for f in range(qtd_fabricas_F):  
        rot_fab = fabricas[f]
        cap_prod[rot_maq,rot_fab] = C_lf[f][l]
        
#criação de um dicionário para armazenar o custo de produção de cada produto utilizando cada máquina em cada fábrica
cust_prod = dict()
for p in range(qtd_produtos_P):
    rot_pro = produtos[p]
    for l in range(qtd_maquinas_L):
        rot_maq = maquinas[l]
        for f in range(qtd_fabricas_F):  
            rot_fab = fabricas[f]
            cust_prod[rot_pro,rot_maq,rot_fab] = p_plf[f][l][p]

#criação de um dicionário para armazenar o custo de transporte de cada produto partindo de cada fábrica até cada cliente
cust_transp = dict()
for p in range(qtd_produtos_P):
    rot_pro = produtos[p]
    for f in range(qtd_fabricas_F):  
        rot_fab = fabricas[f]
        for j in range(qtd_clientes):
            rot_cli = clientes[j]
            cust_transp[rot_pro,rot_fab, rot_cli] = t_pfj[j][f][p]

#Exibe a quantidade de variáveis do problema se a quantidade de clientes for uito grande
if(qtd_clientes > 500):
    print(len(cust_prod) + len(cust_transp))

#geração do modelo
m = gp.Model()
m.setParam(gp.GRB.Param.OutputFlag, 0)

# Variáveis de decisão
x = m.addVars(produtos, maquinas, fabricas, vtype=gp.GRB.CONTINUOUS) #X_p,m,f
y = m.addVars(produtos, fabricas, clientes, vtype=gp.GRB.CONTINUOUS) #Y,p,f,c

# Função objetivo
m.setObjective(
    gp.quicksum(x[p,l,f] * cust_prod[p,l,f] for p in produtos for l in maquinas for f in fabricas) +
    gp.quicksum(y[p,f,j] * cust_transp[p,f,j] for p in produtos for f in fabricas for j in clientes),
    sense=gp.GRB.MINIMIZE)

#Adição de restrições ao modelo 
for idj, j in enumerate(clientes):
    for idp, p in enumerate(produtos):
        m.addConstr(gp.quicksum(y[p,f,j]  for f in fabricas) == D_jp[idp][idj])

for idf, f in enumerate(fabricas):
    for idm, ma in enumerate(materias):
        for idp, p in enumerate(produtos):
            for idl, l in enumerate(maquinas):
                m.addConstr(gp.quicksum([x[p,l,f] * r_mpl[idl][idp][idm]]) <= R_mf[idf][idm])

for idl, l in enumerate(maquinas):
    for idf, f in enumerate(fabricas):
        m.addConstr(gp.quicksum(x[p,l,f]  for p in produtos) <= C_lf[idf][idl])

for idp, p in enumerate(produtos):
    for idf, f in enumerate(fabricas):
        m.addConstr(gp.quicksum(y[p,f,j]  for j in clientes) == gp.quicksum(x[p,l,f] for l in maquinas))

for idp, p in enumerate(produtos):
    for idf, f in enumerate(fabricas):
        m.addConstr(gp.quicksum(y[p,f,j]  for j in clientes) >= 0)

for idp, p in enumerate(produtos):
    for idf, f in enumerate(fabricas):
        m.addConstr(gp.quicksum(x[p,l,f]  for l in maquinas) >= 0)

#executa o modelo
m.optimize()

#cria e exibe um dicionário de informações do problema da instância
infos = dict()
infos["quant. de clientes"] = qtd_clientes
infos["quant. de varáveis"] = m.NumVars
infos["quant. de restrições"] = m.NumConstrs
infos["sol. objetivo"] = m.objVal
infos["tempo de execução"] = m.runtime

print(infos)