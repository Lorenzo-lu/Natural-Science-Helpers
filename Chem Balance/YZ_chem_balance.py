import numpy as np;
import gurobipy as gp;
from gurobipy import GRB;
## Read chemical formula
class YZ_ChemFormula:
    def __init__(self):
        ele = ["H" 	,"He" 	,"Li" 	,"Be" 	,"B" 	,"C" 	,"N" 	,"O" 	,"F" 	,"Ne" 	,"Na" 	,"Mg" 	,"Al" 	,"Si" 	,"P" 	,"S" 	,"Cl" 	,"Ar" 	,
"K" 	,"Ca" 	,"Sc" 	,"Ti" 	,"V" 	,"Cr" 	,"Mn" 	,"Fe" 	,"Co" 	,"Ni" 	,"Cu" 	,"Zn" 	,"Ga" 	,"Ge" 	,"As" 	,"Se" 	,"Br" 	,"Kr" 	,"Rb" 	,"Sr" 	,
"Y" 	,"Zr" 	,"Nb" 	,"Mo" 	,"Tc" 	,"Ru" 	,"Rh" 	,"Pd" 	,"Ag" 	,"Cd" 	,"In" 	,"Sn" 	,"Sb" 	,"Te" 	,"I" 	,"Xe" 	,"Cs" 	,"Ba" 	,"La" 	,"Ce" 	,
"Pr" 	,"Nd" 	,"Pm" 	,"Sm" 	,"Eu" 	,"Gd" 	,"Tb" 	,"Dy" 	,"Ho" 	,"Er" 	,"Tm" 	,"Yb" 	,"Lu" 	,"Hf" 	,"Ta" 	,"W" 	,"Re" 	,"Os" ,"Ir" ,"Pt" 	,
"Au" 	,"Hg" 	,"Tl" 	,"Pb" 	,"Bi" 	,"Po" 	,"At" 	,"Rn" 	,"Fr" 	,"Ra" 	,"Ac" 	,"Th" 	,"Pa" 	,"U" 	,"Np" 	,"Pu" 	,"Am" 	];

        self.element_map = set(ele);
        self.num_map = set(["0","1","2","3","4","5","6","7","8","9","."]);
    def Chem2dic(self,chemical:str):
        length = len(chemical);
        start = 0;
        end1 = 1;
        end2 = 2;
        dic = {};
        while start < length:
            
            if (end2 <= length) and (chemical[start:end2] in self.element_map):
                this_element = chemical[start:end2];
                if this_element not in dic:
                    dic[this_element] = 0;
                dic[this_element] += 1;
                start = end2;
                end1 = start + 1;
                end2 = start + 2;
            else:
                if (end1 <= length) and (chemical[start:end1] in self.element_map):
                    this_element = chemical[start:end1];
                    if this_element not in dic:
                        dic[this_element] = 0;
                    dic[this_element] += 1;
                    #dic[this_element] = 1;
                    start = end1;
                    end1 = start + 1;
                    end2 = start + 2;
                #elif (end1 <= length) and (chemical[start:end1] not in self.element_map):
                    #print("Wrong input after ", chemical[:start]);
                    #return False;
                
            
            if start  < length and chemical[start] in self.num_map:
                dic[this_element] -= 1;
                num_index = start;
                while chemical[num_index] in self.num_map:  
                    #print(chemical[num_index])
                    num_index += 1;
                    if num_index >= length:
                        break;
                #print(chemical[start:num_index])
                #if this_element not in dic:
                    #dic[this_element] = float(chemical[start:num_index]);
                #else:
                    #dic[this_element] += float(chemical[start:num_index]);
                dic[this_element] += float(chemical[start:num_index]);
                start = num_index;
                end1 = start + 1;
                end2 = start + 2;  
                
            if start  < length and chemical[start] == "(":
                end = start;
                while chemical[end] != ")":
                    end += 1;
                #print(end)
                sub_dic = self.Chem2dic(chemical[start+1:end]);
                
                start = end + 1;
                end1 = start + 1;
                end2 = start + 2;
                
                if start  < length and chemical[start] in self.num_map:
                    num_index = start;
                    while chemical[num_index] in self.num_map:  
                        #print(chemical[num_index])
                        num_index += 1;
                        if num_index >= length:
                            break;
                
                    n_cluster = float(chemical[start:num_index]);
                    for i in sub_dic:
                        sub_dic[i] *= n_cluster;
                
                    start = num_index;
                    end1 = start + 1;
                    end2 = start + 2;  
                
                for i in sub_dic:
                    if i not in dic:
                        dic[i] = sub_dic[i];
                    else:
                        dic[i] += sub_dic[i];
            
        return dic;

class YZ_ChemBalance(YZ_ChemFormula):
    def __init__(self):
        super(YZ_ChemBalance,self).__init__();
        self.OxRed= False;

        pass;
    def Left(self, Formulas:list):  
        self.chem_left = [];
        self.elements_left = [];
        self.Left_formulas = Formulas;
        for i in Formulas:
            #print(i)
            dic_i = self.Chem2dic(i);
            for ele in dic_i:
                self.elements_left.append(ele);
            self.chem_left.append(dic_i);
        self.elements_left = set(self.elements_left);
    def Right(self,Formulas:list):  
        self.chem_right = [];
        self.elements_right = [];
        self.Right_formulas = Formulas;
        for i in Formulas:
            dic_i = self.Chem2dic(i);
            for ele in dic_i:
                self.elements_right.append(ele);   
            self.chem_right.append(dic_i);
        self.elements_right = set(self.elements_right);
    def Electrovalence(self, change):
        self.electron_constraint = change;
        self.OxRed = True;
        
    def Balance(self, optimizer = "Gurobi"):
        if (len(self.chem_left)==0) or (len(self.chem_right)==0):
            print("Please input the chemicals first!");
            return False;
        for i in self.Left_formulas:
            if i in self.Right_formulas:
                print("The products cannot be the reactants! Please double check the Formulas.");
                return False;
        if len(self.elements_left) != len(self.elements_right):
            print("Elements in reactants and products are not the same!");
            return False;
            
        n_species = len(self.chem_left) + len(self.chem_right);
        self.elements = list(self.elements_left);
        n_elements = len(self.elements);
        self.Coe = np.zeros((n_elements, n_species));
        
        for col in range(len(self.chem_left)):
            for row in range(n_elements):
                ele = self.elements[row];
                if ele in self.chem_left[col]:
                    self.Coe[row,col] = self.chem_left[col][ele];
        for col in range(len(self.chem_right)):
            for row in range(n_elements):
                ele = self.elements[row];
                if ele in self.chem_right[col]:
                    self.Coe[row,col+len(self.chem_left)] = -self.chem_right[col][ele];
        target = np.zeros((n_elements,1));
        if self.OxRed == True:
            self.Coe = np.vstack((self.Coe, self.electron_constraint));
            target = np.vstack((target, np.zeros((len(self.electron_constraint),1))));
        
        size = self.Coe.shape;
        if size[1] > size[0] + 1:
            print("Please add more constraints in electrons!");
            return None;
        #A = self.Coe[:,1:];
        #b = self.Coe[:,0:1];        
        #ans = np.linalg.pinv(A).dot(b);
        
        if optimizer == "SGD":
        #################################
            # SGD
            ans = self.SGD(self.Coe, target);
            ans /= np.min(np.abs(ans));
            ans /= np.sign(ans[0]);
        #################################
        
        elif optimizer == "Gurobi":
        #################################
            #Gurobi
            ans = self.Gurobi(self.Coe, target);
            ans /= np.min(np.abs(ans));
            ans /= np.sign(ans[0]);
        #################################
        #ans = self.SGD(A, b);
        #ans = np.append(np.array([1]), ans);
        
        else:
            print("Wrong optimizer!");
            return None;
        
        equation = "";
        
        
        formulas = self.Left_formulas;
        for i in range(len(formulas)):
            if i > 0:
                equation += "+";
            equation += (" " + "%.2f"%(ans[i])+ " " +formulas[i] + " ");
        equation += "=";
        n_left = i+1; ## the length of the left side!
        #formulas = list(self.Right_formulas);
        formulas = self.Right_formulas;
        for i in range(len(formulas)):
            if i > 0:
                equation += "+";
            equation += (" " + "%.2f"%(ans[i + n_left]) + " "+formulas[i] + " ");
        print(equation);
        return ans;
    
    def SGD(self, A,T):
        #x = np.ones((len(A[0,:]),1));
        #x = np.zeros((len(A[0,:]),1));
        x = np.random.randn(len(A[0,:]),1);
        
        momentum_beta = 0.9;
        lr = 2e-2;
        regu = 1e-1;
        for i in range(int(1e6)):
            '''
            selection = np.random.randint(0, len(A[:,0]), 1)
            Y = A[selection].dot(x);
            dx = A[selection].T.dot(Y-T[selection]);
            
            '''
            Y = A.dot(x);
            dx = A.T.dot(Y-T)/len(Y);
            #print(dx.shape)
            
            if i == 0:
                dx_last = dx;            
            dx_mom = (momentum_beta * dx) + (1-momentum_beta) * dx_last;
            x -= (dx_mom *lr -  regu * np.sign(dx_mom));
            
            #x[np.where(x < 0)] = 1;
            
        return x;
            
    def Gurobi(self, A, T):
        m = gp.Model();        
        m.setParam('OutputFlag', 0);
        x = m.addMVar(len(A[0,:]), vtype= "c");
        m.setObjective(x @(x),GRB.MINIMIZE);
        for i in range(len(A[:,0])):
            m.addConstr(A[i,:] @ x == T[i]);   
        m.addConstr(x[0] == 1);
        m.optimize();
        return x.X;
            
