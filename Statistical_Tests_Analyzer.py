import pandas as pd
import scipy as sc
import numpy as np
import statsmodels as st
import pingouin as pg
import scikit_posthocs as scit





def stat_test(path_of_csv , list_of_groups, subjects = "Independent" ):
    data = pd.read_csv(path_of_csv)
    user_list= list_of_groups
    groups_list = []    
    for i in list_of_groups :
        groups_list.append(data[i])

    no_of_groups = len(groups_list)   
    #parametric checking
    p_values=[]
    for i in groups_list:
        a,b=sc.stats.shapiro(i)
        p_values.append(b)
    all_above = all(x > 0.05 for x in p_values)
    all_below = all(x <= 0.05  for x in p_values)
    if (all_above or all_below)==False :
        print (" the groups are mix of parametric and non parametric , so it's not appropriate to test them")
        
    if min(p_values)>0.05:
        
        #Parametric tests
        if subjects == 'Independent':
            if no_of_groups == 2 :
                a,final_result = sc.stats.ttest_ind(groups_list[0],groups_list[1])
                if final_result > 0.05:
                    print ("the independent t test result shows there is no significant difference")
                    return final_result
                else:
                    print ("the independent t test result shows there is  significant difference")
                    return final_result
            #checking equality of variance
            if  no_of_groups > 2:
                a,levene_result = sc.stats.levene(*groups_list)
                if levene_result>0.05:
                    a,final_result = sc.stats.f_oneway(*groups_list)
                    if final_result > 0.05:
                        print ("the oneway anova result shows there is no significant difference b/n mean of  groups")
                        return final_result
                    #if variances not equal
                    elif final_result <= 0.05:
                        #  Welch's ANOVA in scipy
                        a, welch_anova_result = sc.stats.f_oneway(*groups_list, equal_var=False)  
                        if welch_anova_result > 0.05:
                            print ("the welch anova result shows there is no significant difference")
                            return welch_anova_result
                        elif welch_anova_result <= 0.05:
                            # post hoc tests
                            #Tuckey test
                            combined_groups_data=[]
                            groups_name=[]
                        
                            for i,groups_data in enumerate(groups_list):
                                combined_groups_data.extend(groups_data)
                                groups_name.extend([f"Group_{i+1}"]*len(groups_data))

                            final_result=st.stats.multicomp.pairwise_tukeyhsd(combined_groups_data, groups_name, alpha=0.05)
                            print (f"here is the tukey final result \n  {final_result}") 
                            return 

                            
        if subjects== 'Dependent':
            #checking fist if all groups arrays have equal length
            check=[]
            for i in groups_list:
                check.append(len(i))
            if min(check)==max(check):
                if no_of_groups == 2 :
                    final_result = sc.stats.ttest_rel( groups_list[0],groups_list[1])  
                    if final_result > 0.05:
                        print ("the dependent t test result shows there is no significant difference")
                        return final_result
                    else:
                        print ("the dependent t test result shows there is  significant difference")
                        return final_result
    
                if  no_of_groups > 2 :
                    check=[]
                    for i in groups_list:
                        check.append(len(i))
                    
                    
                    subjects=np.repeat(range(1,min(check)+1),len(groups_list))  #or subjects=np.repeat(range(1,len(group_list[0])+1))
                    #create condition
                    conditions_name=[]
                        
                    for i ,groups_data in enumerate(groups_list):
                         conditions_name.extend([f"Condition_for_G_{i+1}"])
                    conditions_list = np.tile( conditions_name , min(check))
                    #creat score
                    all_score = []
                    
                    for i in range(min(check)):  
                        for each_list in groups_list: 
                    df_for_rm_anova=pd.DataFrame({'subjects':subjects , 'conditions_list':conditions_list , 'all_score':all_score})  
                    rm_anova_final_result = pg.rm_anova(data= df_for_rm_anova , dv='all_score',  within = 'conditions_list',subject='subjects') 
                    
                    if rm_anova_final_result['sphericity'].iloc[0]:
                        p_value_rm_anova_final_result = rm_anova_final_result['p-unc'].iloc[0]
                        correction_used = "uncorrected"
                        if p_value_rm_anova_final_result > 0.05 :
                             print ("the repeated measures ANOVA result shows there is no significant difference")
                        else:
                            post_hoc_test_for_rm_anova = pg.pairwise_tests(data= df_for_rm_anova , dv='all_score',  within = 'conditions_list',subject='subjects',padjust='bonf',parametric=True)
                            print(f"here is the post hoc tests for the dependent groups /n {post_hoc_test_for_rm_anova}")
                    else:
                        p_value_rm_anova_final_result = rm_anova_final_result['p-GG-corr'].iloc[0]
                        correction_used = "Greenhouse-Geisser corrected"
                        if p_value_rm_anova_final_result > 0.05 :
                             print ("the repeated measures ANOVA result shows there is no significant difference")
                        else:
                            post_hoc_test_for_rm_anova = pg.pairwise_tests(data= df_for_rm_anova , dv='all_score',  within = 'conditions_list',subject='subjects',padjust='bonf',parametric=True)
                            print(f"here is the post hoc tests for the dependent groups \n {post_hoc_test_for_rm_anova}")
                     
            else:
                print("the groups you listed have no equal length so can't do the dependent test!")
                return
                
                    
                
                    
                
     
    if min(p_values)<= 0.05:
        # Non Parametric tests
        if subjects== 'Independent':
            if no_of_groups == 2 :
                a,final_result = sc.stats.mannwhitneyu(groups_list[0],groups_list[1])
                if final_result > 0.05:
                    print ("the independent non parametric t test result shows there is no significant difference")
                    return final_result
                else:
                    print ("the independent non parametric  t test result shows there is  significant difference")
                    return final_result
            if  no_of_groups > 2:
                check=[]
                for i in groups_list:
                    check.append(len(i))
                a,kruskal_result = sc.stats.kruskal(*groups_list)
                if kruskal_result > 0.05:
                    print ("the kruskal walis test result shows there is no significant difference")
                    return kruskal_result
                elif kruskal_result <= 0.05:
                    # post hoc tests
                    #Dunn's test with bufferoni correction
                    
                    subjects=np.repeat(range(1,min(check)+1),len(groups_list))  
                    #create condition
                    conditions_name=[]
                        
                    for i ,groups_data in enumerate(groups_list):
                         conditions_name.extend([f"Condition_for_G_{i+1}"])
                    conditions_list = np.tile( conditions_name , min(check))
                    #creat score
                    all_score = []
                    for i in range(min(check)):  
                        for each_list in groups_list:
                            # if i < len(j): 
                             all_score.append(each_list[i])
                    Dunns_df=pd.DataFrame({ 'conditions_list':conditions_list , 'all_score':all_score})  
                    

                    Dunns_final_result=scit.posthoc_dunn(Dunns_df,val_col='all_score',group_col='conditions_list', p_adjust = 'bonferroni')
                    print (f"here is the Dunns test result \n  {Dunns_final_result}") 
                    return 

                            
        if subjects== 'Dependent': 
            check=[]
            for i in groups_list:
                check.append(len(i))
            if min(check)==max(check):
            
                if no_of_groups == 2 :
                    a,final_result = sc.stats.wilcoxon( groups_list[0],groups_list[1])  
                    if final_result > 0.05:
                        print ("the wilcoxon signed rank test result shows there is no significant difference")
                        return final_result
                    else:
                        print ("the wilcoxon signed rank test result shows there is  significant difference")
                        return final_result
    
                if  no_of_groups > 2 :
                    
                    a,friedman_result = sc.stats.friedmanchisquare(*groups_list)
                    if friedman_result > 0.05:
                        print ("the Fried man test result shows there is no significant difference")
                        return friedman_result
                    elif friedman_result <= 0.05:
                        nemanyi_dict = {}
                        for i ,individual_list in enumerate(groups_list):
                            nemanyi_dict.update({f"group_{i+1}" : individual_list}) 
                        nemanyi_dict_df = pd.DataFrame(nemanyi_dict)
                        nemanyi_final_result = scit.posthoc_nemenyi_friedman(nemanyi_dict_df, ) 
                        print (f"here is the nemenyi test result \n  {nemanyi_final_result} ") 
                        return 
                        
                     
            else:
                print("the groups you listed have no equal length so can't do the dependent test!")
                return
                
                        
                
                    
                
    
     
    
                
                    
                
    
     
    